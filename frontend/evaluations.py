import streamlit as st
import redirect as rd
import pandas as pd
from datetime import datetime
import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder

HOST_NAME = "http://localhost:8000"
STUDENTS_LIST = ["No students to display"] 

if 'evaluation_details' not in st.session_state:
    st.session_state.evaluation_details = []

if 'show_overlay' not in st.session_state:
    st.session_state.show_overlay = False

def create_evaluations():
    populate_evaluation_table()
    with st.sidebar:
        st.header("Grade Me")
        if st.button("Exams", key='eval_exam'):
            rd.go_to_exams()
        if st.button("Students", key='eval_students'):
            rd.go_to_students()
        if st.button("Log Out", key='eval_logout'):
            rd.go_to_exams()

    st.title("Evaluations")

    # Button to show the overlay
    if st.button('Upload Evaluation Details'):
        st.session_state.show_overlay = True

    if st.session_state.show_overlay:
        student_dict = get_student_details()
        STUDENTS_LIST = list(student_dict.keys())
        with st.container():
            with st.form(key='evaluation_details_form'):

                print("hello STUDENTS_LIST = ", STUDENTS_LIST)
                # Input fields
                selected_student = st.selectbox('Select Student', STUDENTS_LIST, key='student_name')

                # File uploader
                uploaded_file = st.file_uploader("Choose a file",accept_multiple_files=False, key='uploaded_file_eval')

                # Submit button for the form
                submitted = st.form_submit_button('Submit')
                if submitted and uploaded_file is not None:
                    json_data = {
                        'exam_id': st.session_state.exam_id,
                        'student_id': student_dict[selected_student]
                    }
                    add_evaluation(json_data, '/Users/devadharshiniravichandranlalitha/Downloads/Question.pdf')
                    # st.session_state.evaluation_details.append({
                    #     # 'Serial No': serial_no,
                    #     'Student Name': student_name,
                    #     'Roll No': 1,
                    #     'Score': 100,
                    #     'Status': "in progress",
                    #     'File Name': uploaded_file.name
                    # })
                    st.session_state.show_overlay = False
        

    #Display the table of exam details
    if st.session_state.evaluation_details:
        st.write('Evaluation Details:')
        df = pd.DataFrame(st.session_state.evaluation_details)

        # Display column headers
        col_headers = st.columns((1, 2, 1, 1, 1, 1, 0.5, 0.5))
        headers = ["Serial No", "Student", "Roll No", "Score", "Status", "File Name", "View", "Delete"]
        for col_header, header in zip(col_headers, headers):
            col_header.write(header)

        # Iterate over the DataFrame to display the table with buttons
        for i, row in df.iterrows():
            cols = st.columns((1, 2, 1, 1, 1, 1, 0.5, 0.5))
            cols[0].write(i + 1) 
            cols[1].write(row['Student'])
            cols[2].write(row['Email'])
            cols[3].write(row['Roll No'])
            cols[4].write(row['Status'])
            cols[5].write(row['File Name'])

            # View button (implement functionality as needed)
            view_button = cols[6].button('👁️', key=f"view_{i}")
            if view_button:
                pass

            # Delete button
            delete_button = cols[7].button('🗑️', key=f"delete_{i}")
            if delete_button:
                del st.session_state.evaluation_details[i]
                st.experimental_rerun()


def populate_evaluation_table():
    answers_get_url = HOST_NAME + "/quick-score/answers"
    query_params = {
        'exam_id': st.session_state.exam_id
    }
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.get(answers_get_url, params=query_params, headers=headers)
        if response.status_code == 200:
            answer_result = response.json()
        else:
            st.error(f"Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")

    modified_answers = []
    if len(answer_result) > 0:
        print("answer_result inside pop= ", answer_result)
        for key, answer in enumerate(answer_result):
            print(answer)
            item = {
                        'id': answer["id"],
                        'Serial No': key+1,
                        'Name': answer["name"],
                        'Email': answer["email"],
                        'Roll number': answer["roll_no"],
                        # Store uploaded file info or handle file processing here
                        'Files': 'dummy file'
                    }
            modified_answers.append(item)
        st.session_state.evaluation_details = modified_answers


#retrieve student details
def get_student_details():
    students_get_url = HOST_NAME + "/quick-score/students"
    query_params = {
        'user_id': st.session_state.user_id
    }
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.get(students_get_url, params=query_params, headers=headers)
        if response.status_code == 200:
            
            student_result = response.json()
            
            # student_result = json.loads(student_result)
            print("student_result inside get sd= ", student_result)
            student_dictionary = {}
            for student in student_result:
                print("type of student", type(student))
                key = f"{student['name']} ({student['roll_no']})"
                value = student['id']
                student_dictionary[key] = value
            return student_dictionary
        else:
            st.error(f"Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")

# def remove_evaluation(delete_id):
#      # The URL for the API endpoint
#     exams_get_url = HOST_NAME + "/quick-score/exams/" + str(delete_id)

#     # Set the appropriate headers for JSON - this is important!
#     headers = {'Content-Type': 'application/json'}

#     # Send the POST request
#     response = requests.delete(exams_get_url, headers=headers)
#     print(response)
#     # Check if the request was successful
#     if response.status_code == 200:
#         st.experimental_rerun()
#     else:
#         print("Error in getting the exam details for the user, ", user_id)
#     populate_evaluation_table()

def add_evaluation(json_data, file_url):
    create_evaluation_url = HOST_NAME + "/quick-score/answers"
    
    # with open(file_url, 'rb') as pdf_file:
    multipart_data = MultipartEncoder(
        fields = {
            'file': ('answerkey.pdf', open(file_url, 'rb'), 'application/pdf'),
            'answer_data': json.dumps(json_data)
        }
    )   
    print("multipart_data = ", multipart_data.to_string())
    headers = {'Content-Type': multipart_data.content_type}  
    with st.spinner('Uploading evaluation details...'):
        response = requests.post(create_evaluation_url, data=multipart_data.to_string(), headers=headers)
    if response.status_code == 200:
        st.success("answer added successfully.")
        # Optionally, rerun to refresh the data
        st.experimental_rerun()
    else:
        # print("response json=", response.json())
        st.error(f"Failed to add answer. Status code: {response.status_code}")
