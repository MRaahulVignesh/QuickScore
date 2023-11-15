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

def create_students_page():
    populate_students_table()

    with st.sidebar:
        st.header("Grade Me")
        if st.button("Exams"):
            rd.go_to_exams()
        if st.button("Students"):
            rd.go_to_students()
        if st.button("Evaluations"):
            rd.go_to_evaluations()
        if st.button("Log Out"):
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
                # Automatically generate the next serial number
                serial_no = len(st.session_state.student_details) + 1
                # Display the serial number to the user
                st.write(f"Serial No: {serial_no}")
                name = st.text_input('Name', key='name')
                email = st.text_input('Email', key='email')
                roll_number = st.text_input('Roll Number', key='roll_number')
                # Submit button for the form
                submitted = st.form_submit_button('Submit')
                if submitted:
                    # Store the submitted values in the session state
                    st.session_state.student_details.append({
                        'Serial No': len(st.session_state.student_details) + 1,
                        'Name': st.session_state.name,
                        'Email': st.session_state.email,
                        'Roll Number': st.session_state.roll_number
                    })
                    # Hide the overlay
                    st.session_state.show_overlay = False
                    # Clear the session state keys if needed
                    st.session_state.pop('name', None)
                    st.session_state.pop('email', None)
                    st.session_state.pop('roll_number', None)

    # Display the table of student details with 'View', 'Edit', and 'Delete' buttons
    if st.session_state.student_details:
        st.write('Student Details:')
        # Create a DataFrame for the table
        df = pd.DataFrame(st.session_state.student_details)

        # Display column headers
        col_headers = st.columns((1, 2, 2, 2, 2))
        headers = ["Serial No", "Name", "Email", "Roll Number", "Action"]
        for col_header, header in zip(col_headers, headers):
            col_header.write(header)

        # Iterate over the DataFrame to display the table with buttons
        for i, row in df.iterrows():
            cols = st.columns((1, 2, 2, 2, 1, 1))
            cols[0].write(row['Serial No'])
            cols[1].write(row['Name'])
            cols[2].write(row['Email'])
            cols[3].write(row['Roll Number'])

            # Action buttons
            if cols[4].button('Edit', key=f"edit_{i}"):
                # Implement edit logic
                pass
            if cols[5].button('Delete', key=f"delete_{i}"):
                # Remove the selected row from the list of student details
                st.session_state.student_details.pop(i)
                # Rerender the page to reflect changes
                st.experimental_rerun()

def populate_students_table():

    # The URL for the API endpoint
    students_get_url = HOST_NAME + "/quick-score/students"
    user_id = st.session_state.user_id

    # The data you want to send with the POST request
    query_params = {
        'user_id': user_id
    }

    # Set the appropriate headers for JSON - this is important!
    headers = {'Content-Type': 'application/json'}

    # Send the POST request
    response = requests.get(students_get_url, params=query_params, headers=headers)
    print(response)
    # Check if the request was successful
    if response.status_code == 200:
        student_result = response.json()
    else:
        print("Error in getting the student details for the user, ", user_id)
        student_result = []
        

    modified_students = []
    if len(student_result) > 0:
        for key, student in enumerate(student_result):
            print(student)
            item = {
                        'Serial No': key + 1,
                        'Name': student["name"],
                        'Email': student["email"],
                        'Roll Number': student["roll_no"]
                    }
            modified_students.append(item)
        st.session_state.student_details = modified_students