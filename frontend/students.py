import streamlit as st
import redirect as rd
import pandas as pd
from datetime import datetime
import requests

if 'student_details' not in st.session_state:
    st.session_state.student_details = []
if 'show_overlay' not in st.session_state:
    st.session_state.show_overlay = False

HOST_NAME = "http://localhost:8000"

def create_students():
    populate_students_table()
    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            padding-top: 0rem;
        }
        .css-18e3th9 {
            padding: 0.25rem 1rem;
            text-align: center;
        }
        .stButton>button {
            width: 100%;  /* Make the buttons use the full width */
            border-radius: 5px;  /* Optional: Rounds the corners of the buttons */
            margin-bottom: 10px;  /* Adds space between the buttons */
            background-color: #C0C9CB;
        }
        /* Style for profile image */
        .profile-img {
            border-radius: 50%;
            width: 50px;
            height: 50px;
        }
        /* Style for welcome message */
        .welcome-msg {
            color: white;
            font-weight: bold;
            font-size: 24px;
            margin-top: 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    with st.sidebar:
        st.markdown("""
            <div style="text-align: center;">
                <img class="profile-img" src="https://i.ibb.co/jrpb6Xd/profile1.png" alt="Profile icon">
                <p class="welcome-msg">Welcome Author</p>
            </div>
            """, unsafe_allow_html=True)
        if st.button("Exams", key='stu_exams'):
            rd.go_to_exams()
        if st.button("Students", key='stu_students'):
            rd.go_to_students()
        if st.button("References", key='stu_references'):
            rd.go_to_references()
        if st.button("Log Out", key='stu_logout'):
            rd.go_to_exams()

    st.title("Students")

    # Initialize a session state variable for storing exam details
    if 'student_details' not in st.session_state:
        st.session_state.student_details = []

    # Overlay toggle
    if 'show_overlay' not in st.session_state:
        st.session_state.show_overlay = False

    # Button to show the overlay
    if st.button('Upload Student Details'):
        st.session_state.show_overlay = True

    # The overlay layout
    if st.session_state.show_overlay:
        with st.container():
            with st.form(key='student_details_form'):
                name = st.text_input('Name', key='name')
                email = st.text_input('Email', key='email')
                roll_number = st.text_input('Roll Number', key='roll_number')
                # Submit button for the form
                submitted = st.form_submit_button('Submit')
                if submitted:
                    # Call the function to add a student
                    add_student(st.session_state.name, st.session_state.email, st.session_state.roll_number)
                    st.session_state.show_overlay = False
                    st.session_state.pop('name', None)
                    st.session_state.pop('email', None)
                    st.session_state.pop('roll_number', None)
                    # st.experimental_rerun()

    # Display the table of student details with 'View', 'Edit', and 'Delete' buttons
    if st.session_state.student_details:
        st.write('Student Details:')
        # Create a DataFrame for the table
        df = pd.DataFrame(st.session_state.student_details)

        # Display column headers
        col_headers = st.columns((1, 1, 1, 1, 0.5, 0.5))
        headers = ["S.No", "Name", "Email", "Roll Number", "Edit", "Delete"]
        for col_header, header in zip(col_headers, headers):
            col_header.write(header)

        # Iterate over the DataFrame to display the table with buttons
        for i, row in df.iterrows():
            student_id = row["student_id"]
            cols = st.columns((1, 1, 1, 1, 0.5, 0.5))
            cols[0].write(str(row['S.No']))
            cols[1].write(row['Name'])
            cols[2].write(row['Email'])
            cols[3].write(row['Roll Number'])

            # Action buttons
            if cols[4].button('✏️', key=f"edit_{i}"):
                # Implement edit logic
                pass
            if cols[5].button('🗑️', key=student_id):
                delete_student(student_id)
                st.experimental_rerun()
                
def populate_students_table():

    # The URL for the API endpoint
    students_get_url = HOST_NAME + "/quick-score/students"
    query_params = {
        'user_id': st.session_state.user_id
    }
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.get(students_get_url, params=query_params, headers=headers)
        if response.status_code == 200:
            student_result = response.json()
        else:
            st.error(f"Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        student_result = []
        

    modified_students = []
    if len(student_result) > 0:
        for key, student in enumerate(student_result):
            print(student)
            item = {
                        'S.No': key + 1,
                        'Name': student["name"],
                        'Email': student["email"],
                        'Roll Number': student["roll_no"],
                        'student_id': student["id"]
                    }
            modified_students.append(item)
        st.session_state.student_details = modified_students
    
def delete_student(student_id):

    # The URL for the API endpoint
    student_delete_url = HOST_NAME + "/quick-score/students/" + str(student_id) 

    # Set the appropriate headers for JSON - this is important!
    headers = {'Content-Type': 'application/json'}

    # Send the POST request
    response = requests.delete(student_delete_url, headers=headers)
    print(response)
    # Check if the request was successful
    if response.status_code == 200:
        st.session_state.student_details = [
            student for student in st.session_state.student_details if student['student_id'] != student_id
        ]
        st.experimental_rerun()
    else:
        print(f"Failed to delete student record. Status code: {response.status_code}")
        

def add_student(name, email, roll_number):
    # The URL for the API endpoint to add a student
    student_add_url = HOST_NAME + "/quick-score/students" 

    # The data you want to send with the POST request
    student_data = {
        'name': name,
        'email': email,
        'roll_no': roll_number,
        'user_id': st.session_state.user_id
    }

    # Set the appropriate headers for JSON
    headers = {'Content-Type': 'application/json'}

    # Send the POST request
    response = requests.post(student_add_url, json=student_data, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        st.success("Student added successfully.")
        # Optionally, rerun to refresh the data
        st.experimental_rerun()
    else:
        st.error(f"Failed to add student. Status code: {response.status_code}")
