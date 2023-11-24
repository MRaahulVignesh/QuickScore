from backend.core.student_core import StudentCore
import streamlit as st
import frontend.redirect as rd
import pandas as pd
import requests
import io

from frontend.side_bar import render_side_bar
from backend.core.answer_core import AnswerCore
from backend.core.answer_core import AnswerCore
import pdfplumber

HOST_NAME = "http://localhost:8000"
STUDENTS_LIST = ["No students to display"] 



def create_evaluations():
    st.session_state.evaluation_details = populate_evaluation_table()
    render_side_bar()
    
    st.title("Evaluations")
    
    if 'evaluation_details' not in st.session_state:
        st.session_state.evaluation_details = []

    if 'show_overlay' not in st.session_state:
        st.session_state.show_overlay = False

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
    
    exam_id = st.session_state.exam_id
    
    answer_core = AnswerCore()
    answer_result = answer_core.get_answers_by_exam_id(exam_id)
    
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
    user_id = st.session_state.user_id
    student_core = StudentCore()
    try:
        student_result = student_core.get_students_by_user_id(user_id=user_id)
    except Exception as error:
        st.error("Could not reterieve the student details")
        
    student_dictionary = {}
    for student in student_result:
        key = f"{student['name']} ({student['roll_no']})"
        value = student['id']
        student_dictionary[key] = value
    return student_dictionary

def remove_evaluation(delete_id):
    answer_core = AnswerCore()
    try:
        answer_core.delete_answer(delete_id)
        st.sucess("Successfully removed the evaluation!!")
        st.experimental_rerun()
    except Exception as error:
        print(error)
        st.error("Cannot remove evaluation!!")
    

def add_evaluation(json_data, file_upload):
    filename = file_upload.name
    answer_core = AnswerCore()

    pdf_data = file_upload.read()

    with pdfplumber.open(io.BytesIO(pdf_data)) as pdf:
        answer_pdf = ""
        for page in pdf.pages:
            answer_pdf += page.extract_text()
            
    with st.spinner("Uploading evaluation details..."):
        answer_core.create_answer(input=json_data, answer_pdf=pdf_data, filename=filename)
        st.success("answer added successfully.")
        st.experimental_rerun()
        
        
def view_evaluation(_id):
    st.session_state.evaluation_id = _id
    rd.go_to_individual_evaluation()