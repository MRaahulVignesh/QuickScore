import streamlit as st
import redirect as rd
import pandas as pd
from datetime import datetime
import requests
import json
import time
from requests_toolbelt.multipart.encoder import MultipartEncoder
from side_bar import render_side_bar

HOST_NAME = "http://localhost:8000"
STUDENTS_LIST = ["No students to display"] 

if 'evaluation_details' not in st.session_state:
    st.session_state.evaluation_details = []

if 'show_overlay' not in st.session_state:
    st.session_state.show_overlay = False

def create_evaluations():
    st.session_state.evaluation_details = populate_evaluation_table()
    render_side_bar()
    

    st.title("Evaluations")

    with st.expander("Upload Evaluation Details"):
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
                    add_evaluation(json_data, uploaded_file)
                    # st.session_state.evaluation_details.append({
                    #     # 'Serial No': serial_no,
                    #     'Student Name': student_name,
                    #     'Roll No': 1,
                    #     'Score': 100,
                    #     'Status': "in progress",
                    #     'File Name': uploaded_file.name
                    # })
                    st.session_state.show_overlay = False
                    st.experimental_rerun()
        

    #Display the table of exam details
    if st.session_state.evaluation_details:
        st.markdown("<br>", unsafe_allow_html=True)
        df = pd.DataFrame(st.session_state.evaluation_details)

        # Display column headers
        col_headers = st.columns((1, 1, 1, 1, 1, 1, 0.5, 0.5))
        headers = ["SNo", "Name", "Roll No", "Score", "Status", "File Name", "View", "Delete"]
        for col_header, header in zip(col_headers, headers):
            col_header.markdown(f'<h5 style="color: #4F8BF9;"><strong>{header}</strong></h5></div>', unsafe_allow_html=True)

        # Iterate over the DataFrame to display the table with buttons
        for i, row in df.iterrows():
            cols = st.columns((1, 1, 1, 1, 1, 1, 0.5, 0.5))
            cols[0].write(str(i + 1)) 
            cols[1].write(row['Name'])
            cols[2].write(row['Roll No'])
            cols[3].write(str(row['Score']))
            cols[4].write(row['Status'])
            cols[5].write(row['File Name'])

            # View button (implement functionality as needed)
            view_button = cols[6].button('👁️', key=f"view_{i}")
            if view_button:
                view_evaluation(row['id'])

            # Delete button
            delete_button = cols[7].button('🗑️', key=f"delete_{i}")
            if delete_button:
                remove_evaluation(row['id'])
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
                        'SNo': key+1,
                        'Name': answer["student_name"],
                        'Roll No': answer["student_roll_no"],
                        'Score': answer["score"],
                        'Status': "completed",
                        'File Name': answer["file_name"]
                    }
            modified_answers.append(item)
        return modified_answers


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

def remove_evaluation(delete_id):
     # The URL for the API endpoint
    exams_get_url = HOST_NAME + "/quick-score/answers/" + str(delete_id)

    # Set the appropriate headers for JSON - this is important!
    headers = {'Content-Type': 'application/json'}

    # Send the POST request
    response = requests.delete(exams_get_url, headers=headers)
    print(response)
    # Check if the request was successful
    if response.status_code == 200:
        st.experimental_rerun()
    else:
        print("Delete operation failed")
    st.session_state.evaluation_details = populate_evaluation_table()



def add_evaluation(json_data, file_upload):
    create_evaluation_url = HOST_NAME + "/quick-score/answers"
    
    # with open(file_url, 'rb') as pdf_file:
    multipart_data = MultipartEncoder(
        fields = {
            'file': (file_upload.name, file_upload.getvalue(), 'application/pdf'),
            'answer_data': json.dumps(json_data)
        }
    )   
    headers = {'Content-Type': multipart_data.content_type}  
    with st.spinner("Uploading evaluation details..."):
        response = requests.post(create_evaluation_url, data=multipart_data.to_string(), headers=headers)
        
    if response.status_code == 200:
        st.success("answer added successfully.")
        # Optionally, rerun to refresh the data
        st.experimental_rerun()
    else:
        # print("response json=", response.json())
        st.error(f"Failed to add answer. Status code: {response.status_code}")
        
def view_evaluation(_id):
    print("hello")
    st.session_state.evaluation_id = _id
    rd.go_to_individual_evaluation()