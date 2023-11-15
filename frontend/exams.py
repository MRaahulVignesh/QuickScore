import streamlit as st
from datetime import datetime
import redirect as rd
import pandas as pd
import requests

HOST_NAME = "http://localhost:8000"

def create_exams_page():
    
    populate_table()

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

    st.title("Exams")

    # Button to show the overlay
    if st.button('Upload Exam Details'):
        st.session_state.show_overlay = True

    # The overlay layout
    if st.session_state.show_overlay:
        with st.container():
            with st.form(key='exam_details_form'):
                # Input fields
                # Automatically generate the next serial number
                serial_no = len(st.session_state.exam_details) + 1
                # Display the serial number to the user
                st.write(f"Serial No: {serial_no}")
                name = st.text_input('Name', key='name')
                date = st.date_input('Date', value=datetime.today(), key='date')
                total_score = st.text_input('Total Score', key='total_score')
                
                # File uploader
                uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=True, key='file_uploader')
                
                # Submit button for the form
                submitted = st.form_submit_button('Submit')
                if submitted:
                    # Hide the overlay
                    st.session_state.show_overlay = False
                    # Store the submitted values in the session state
                    st.session_state.exam_details.append({
                        'id': serial_no,
                        'Serial No': serial_no,
                        'Name': name,
                        'Date': date,
                        'Total Score': total_score,
                        # Store uploaded file info or handle file processing here
                        'Files': ', '.join(file.name for file in uploaded_files) if uploaded_files else 'No files'
                    })

    # Display the table of exam details with 'Edit', 'View', and 'Delete' buttons
    if st.session_state.exam_details:
        st.write('Exam Details:')
        # Create a DataFrame for the table
        df = pd.DataFrame(st.session_state.exam_details)

        # Display column headers
        col_headers = st.columns((1, 2, 1, 1, 2, 2))
        headers = ["Serial No", "Name", "Date", "Total Score", "Files", "Action"]
        for col_header, header in zip(col_headers, headers):
            col_header.write(header)

        # Iterate over the DataFrame to display the table with buttons
        for i, row in df.iterrows():
            cols = st.columns((1, 2, 1, 1, 1, 1, 1, 1))
            cols[0].write(i + 1)  # Adjust index if necessary
            cols[1].write(row['Name'])
            cols[2].write(row['Date'])  # Format the date
            cols[3].write(row['Total Score'])
            cols[4].write(row['Files'])

            # View button (you'll need to implement what 'View' should do)
            view_button = cols[5].button('View', key=f"view_{i}")
            if view_button:
                # Implement what should happen when 'View' is clicked
                pass

            # Edit button (you'll need to implement what 'Edit' should do)
            edit_button = cols[6].button('Edit', key=f"edit_{i}")
            if edit_button:
                # Implement what should happen when 'Edit' is clicked
                pass

            # Delete button
            delete_button = cols[7].button('Delete', key=f"delete_{i}")
            if delete_button:
                # print("look here")
                # for i in range(len(st.session_state.exam_details)):
                #     print(st.session_state.exam_details[i])
                # remove_exam(st.session_state.exam_details[i]["id"])
                # populate_table()
                # Remove the selected row from the list of exam details
                del st.session_state.exam_details[i]
                # Update the DataFrame to reflect the deletion and rerender the page
                st.experimental_rerun()

def populate_table():

    # The URL for the API endpoint
    exams_get_url = HOST_NAME + "/quick-score/exams"
    user_id = st.session_state.user_id

    # The data you want to send with the POST request
    query_params = {
        'user_id': user_id
    }

    # Set the appropriate headers for JSON - this is important!
    headers = {'Content-Type': 'application/json'}

    # Send the POST request
    response = requests.get(exams_get_url, params=query_params, headers=headers)
    print(response)
    # Check if the request was successful
    if response.status_code == 200:
        exam_result = response.json()
    else:
        print("Error in getting the exam details for the user, ", user_id)
        exam_result = []
        

    modified_exams = []
    if len(exam_result) > 0:
        for key, exam in enumerate(exam_result):
            print(exam)
            item = {
                        'id': exam["id"],
                        'Serial No': key+1,
                        'Name': exam["name"],
                        'Date': exam["conducted_date"],
                        'Total Score': exam["total_marks"],
                        # Store uploaded file info or handle file processing here
                        'Files': 'dummy file'
                    }
            modified_exams.append(item)
        st.session_state.exam_details = modified_exams

def remove_exam(delete_id):
     # The URL for the API endpoint
    exams_get_url = HOST_NAME + "/quick-score/exams"
    user_id = st.session_state.user_id

    # The data you want to send with the POST request
    query_params = {
        'user_id': user_id
    }

    # Set the appropriate headers for JSON - this is important!
    headers = {'Content-Type': 'application/json'}

    # Send the POST request
    response = requests.delete(exams_get_url, params=query_params, headers=headers)
    print(response)
    # Check if the request was successful
    if response.status_code == 200:
        exam_result = response.json()
    else:
        print("Error in getting the exam details for the user, ", user_id)
        exam_result = []
        

    modified_exams = []
    if len(exam_result) > 0:
        for key, exam in enumerate(exam_result):
            print(exam)
            item = {
                        'id': exam["id"],
                        'Serial No': key+1,
                        'Name': exam["name"],
                        'Date': exam["conducted_date"],
                        'Total Score': exam["total_marks"],
                        # Store uploaded file info or handle file processing here
                        'Files': 'dummy file'
                    }
            modified_exams.append(item)
        st.session_state.exam_details = modified_exams
