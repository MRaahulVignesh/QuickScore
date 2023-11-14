import streamlit as st
import redirect as rd
import pandas as pd
from datetime import datetime


if 'student_details' not in st.session_state:
    st.session_state.student_details = []
if 'show_overlay' not in st.session_state:
    st.session_state.show_overlay = False
def create_students_page():
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
            cols = st.columns((1, 2, 2, 2, 1, 1, 1))
            cols[0].write(row['Serial No'])
            cols[1].write(row['Name'])
            cols[2].write(row['Email'])
            cols[3].write(row['Roll Number'])

            # Action buttons
            if cols[4].button('View', key=f"view_{i}"):
                # Implement view logic
                pass
            if cols[5].button('Edit', key=f"edit_{i}"):
                # Implement edit logic
                pass
            if cols[6].button('Delete', key=f"delete_{i}"):
                # Remove the selected row from the list of student details
                st.session_state.student_details.pop(i)
                # Rerender the page to reflect changes
                st.experimental_rerun()