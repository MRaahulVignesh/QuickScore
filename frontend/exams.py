import streamlit as st
from datetime import datetime
from evaluations import create_evaluations
import redirect as rd
import pandas as pd
import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder

HOST_NAME = "http://localhost:8000"

def create_exams():

    populate_table()

    with st.sidebar:
        st.header("Grade Me")
        if st.button("Exams", key='exam_exams'):
            rd.go_to_exams()
        if st.button("Students", key='exam_students'):
            rd.go_to_students()
        if st.button("References", key='exam_references'):
            rd.go_to_references()
        if st.button("Log Out", key='exam_logout'):
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
                conducted_date = str(st.date_input('Date', value=datetime.today(), key='conducted_date'))
                description = st.text_input('Description', key='description')
                total_marks = st.number_input('Total Score', key='total_marks')

                # File uploader
                uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=False, key='file_uploader')

                # Submit button for the form
                submitted = st.form_submit_button('Submit')
                if submitted:
                    json_data = {
                        "name": name,
                        "conducted_date": conducted_date,
                        "description": description,
                        "total_marks": total_marks,
                        "user_id": st.session_state.user_id
                    }
                    print("json_data = ", json_data)

                    add_exam(json_data, '/Users/devadharshiniravichandranlalitha/Downloads/Question_new.pdf')
                    # Hide the overlay
                    st.session_state.show_overlay = False

    # Display the table of exam details with 'Edit', 'View', and 'Delete' buttons
    if st.session_state.exam_details:
        st.write('Exam Details:')
        # Create a DataFrame for the table
        df = pd.DataFrame(st.session_state.exam_details)

        # Display column headers
        col_headers = st.columns((1, 1, 1, 1, 1, 1, 0.5, 0.5, 0.5))
        headers = ["Serial No", "Name", "Date", "Description", "Total Score", "Files", "View", "Edit", "Delete"]
        for col_header, header in zip(col_headers, headers):
            col_header.write(header)

        # Iterate over the DataFrame to display the table with buttons
        for i, row in df.iterrows():
            exam_id = row['id']
            cols = st.columns((1, 1, 1, 1, 1, 1, 0.5, 0.5, 0.5))
            cols[0].write(i + 1)  # Adjust index if necessary
            cols[1].write(row['Name'])
            cols[2].write(row['Date'])  # Format the date
            cols[3].write(row['Description'])
            cols[4].write(row['Total Score'])
            cols[5].write(row['Files'])

            # View button (you'll need to implement what 'View' should do)
            view_button = cols[6].button('👁️', key=f"view_{i}")
            if view_button:
                st.session_state.exam_id = exam_id
                # create_evaluations(exam_id)
                rd.go_to_evaluations()

            # Edit button (you'll need to implement what 'Edit' should do)
            edit_button = cols[7].button('✏️', key=f"edit_{i}")
            if edit_button:
                pass

            # Delete button
            delete_button = cols[8].button('🗑️', key=f"delete_{i}")
            if delete_button:
                remove_exam(exam_id)
                st.experimental_rerun()

def populate_table():
    exams_get_url = HOST_NAME + "/quick-score/exams"
    query_params = {
        'user_id': st.session_state.user_id
    }
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.get(exams_get_url, params=query_params, headers=headers)
        if response.status_code == 200:
            exam_result = response.json()
            # ... [process and update session state]
        else:
            st.error(f"Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")

    modified_exams = []
    if len(exam_result) > 0:
        for key, exam in enumerate(exam_result):
            print(exam)
            item = {
                        'id': exam["id"],
                        'Serial No': key+1,
                        'Name': exam["name"],
                        'Date': exam["conducted_date"],
                        'Description': exam["description"],
                        'Total Score': exam["total_marks"],
                        # Store uploaded file info or handle file processing here
                        'Files': 'dummy file'
                    }
            modified_exams.append(item)
        st.session_state.exam_details = modified_exams

def remove_exam(delete_id):
     # The URL for the API endpoint
    exams_get_url = HOST_NAME + "/quick-score/exams/" + str(delete_id)

    # Set the appropriate headers for JSON - this is important!
    headers = {'Content-Type': 'application/json'}

    # Send the POST request
    response = requests.delete(exams_get_url, headers=headers)
    print(response)
    # Check if the request was successful
    if response.status_code == 200:
        st.experimental_rerun()
    else:
        print("Error in getting the exam details for the user, ", user_id)
    populate_table()

def add_exam(json_data, file_url):
    create_exam_url = HOST_NAME + "/quick-score/exams"
    
    # with open(file_url, 'rb') as pdf_file:
    multipart_data = MultipartEncoder(
        fields = {
            'file': ('answerkey.pdf', open(file_url, 'rb'), 'application/pdf'),
            'exam': json.dumps(json_data)
        }
    )   
    headers = {'Content-Type': multipart_data.content_type}  
    
    with st.spinner("Uploading exam details..."):
        st.write("Searching for data...")
        time.sleep(2)
        st.write("Found URL.")
        time.sleep(1)
        st.write("Processing data...")
        time.sleep(1)

        response = requests.post(create_exam_url, data=multipart_data.to_string(), headers=headers)
        
        # Update the spinner label
        st.spinner("Document received.")

    if response.status_code == 200:
        st.success("Student added successfully.")
        # Optionally, rerun to refresh the data
        st.experimental_rerun()
    else:
        print("response json=", response.json())
        st.error(f"Failed to add exam. Status code: {response.status_code}")

