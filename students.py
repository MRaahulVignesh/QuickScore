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
    # Sample list of student names for the dropdown
    # student_names = [f"Student {i+1}" for i in range(10)]

    # # Display a table with the uploaded files
    # if 'uploaded_files' in st.session_state and st.session_state['uploaded_files']:
    #     df = pd.DataFrame(st.session_state['uploaded_files'])

    #     # Display column headers
    #     st.write('Type', 'Name', 'Date', 'Student Name', 'Percentage', 'Select Student')

    #     # Iterate over each row to display the data and dropdown
    #     for index, row in df.iterrows():
    #         cols = st.columns(6)  # Adjust the number of columns if necessary
    #         for i, col in enumerate(cols[:-1]):  # Loop through all columns except the last one
    #             col.write(row[i])
            
    #         # Dropdown in the last column
    #         selected_student = cols[-1].selectbox(
    #             "",
    #             student_names,
    #             key=f"dropdown_{index}"  # Unique key for each dropdown
    #         )
    # else:
    #     st.write("No files uploaded yet.")


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
            # The form inside the overlay
            with st.form(key='student_details_form'):
                # Input fields
                name = st.text_input('Name')
                date = st.date_input('Date', value=datetime.today())
                total_score = st.text_input('Total Score')
                
                # File uploader
                uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=True, key='file_uploader_students')
                
                # Submit button for the form
                submitted = st.form_submit_button('Submit')
                if submitted:
                    # Hide the overlay
                    st.session_state.show_overlay = False
                    # Store the submitted values in the session state
                    st.session_state.student_details.append({
                        'Name': name,
                        'Date': date,
                        'Total Score': total_score,
                        # Store uploaded file info or handle file processing here
                        'Files': ', '.join(file.name for file in uploaded_files) if uploaded_files else 'No files'
                    })
                    # Clear the input fields after submission
                    st.session_state['name'] = ""
                    st.session_state['date'] = datetime.today()
                    st.session_state['total_score'] = ""

    # Display the table of exam details
    if st.session_state.student_details:
        st.write('Student Details:')
        st.table(st.session_state.student_details)