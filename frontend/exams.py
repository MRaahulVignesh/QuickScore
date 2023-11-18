import streamlit as st
from datetime import datetime
from evaluations import create_evaluations
import redirect as rd
import pandas as pd
import requests
import time
from components.button import custom_button
from css.input import input_css
from side_bar import render_side_bar
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder


HOST_NAME = "http://localhost:8000"
REFERENCES_LIST = ["No students to display"]  

def create_exams():
    input_css()
    populate_table()
    render_side_bar()
    st.title("Exams")

    # # Button to show the overlay
    # if custom_button("Upload Exam Details!", "btn1", "background-color: blue; color: white; border-radius: 5px; border: none; padding: 10px 20px;"):
    #     st.session_state.show_overlay = True

    # The overlay layout
    context_dict = get_references_details()
    REFERENCES_LIST = list(context_dict.keys())
    with st.expander("Upload Exam Details"):
        with st.container():
            with st.form(key='exam_details_form'):
                name = st.text_input('Name', key='name')
                conducted_date = str(st.date_input('Date', value=datetime.today(), key='conducted_date'))
                description = st.text_input('Description', key='description')
                total_marks = st.number_input('Total Score', key='total_marks')
                selected_reference = st.selectbox('Select Reference', REFERENCES_LIST, key='references_name')
                # File uploader
                uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=False, key='file_uploader')
                if selected_reference is not None:
                    context_id = context_dict[selected_reference]
                else:
                    context_id = None
                # Submit button for the form
                submitted = st.form_submit_button('Submit')
                if submitted:
                    json_data = {
                        "name": name,
                        "conducted_date": conducted_date,
                        "description": description,
                        "total_marks": total_marks,
                        "user_id": st.session_state.user_id,
                        "context_id": context_id
                    }
                    print("json_data = ", json_data)

                    add_exam(json_data, uploaded_files)
                    # Hide the overlay
                    st.session_state.show_overlay = False
                    st.session_state.pop('name', None)
                    st.session_state.pop('conducted_date', None)
                    st.session_state.pop('description', None)
                    st.session_state.pop('total_marks', None)
                    st.session_state.pop('context_id', None)
                    st.experimental_rerun()

    # Display the table of exam details with 'Edit', 'View', and 'Delete' buttons
    if st.session_state.exam_details:
        st.markdown("<br>", unsafe_allow_html=True)
        # Create a DataFrame for the table
        df = pd.DataFrame(st.session_state.exam_details)

        # Display column headers
        col_headers = st.columns((1, 1, 1, 1, 1, 1, 0.5, 0.5, 0.5))
        headers = ["S.No", "Name", "Date", "Description", "Total Score", "Files", "View", "Edit", "Delete"]
        for col_header, header in zip(col_headers, headers):
            col_header.markdown(f'<h5 style="color: #4F8BF9;"><strong>{header}</strong></h5></div>', unsafe_allow_html=True)

        # Iterate over the DataFrame to display the table with buttons
        for i, row in df.iterrows():
            exam_id = row['id']
            cols = st.columns((1, 1, 1, 1, 1, 1, 0.5, 0.5, 0.5))
            cols[0].write(str(i + 1))
            cols[1].write(row['Name'])
            cols[2].write(row['Date'])  # Format the date
            cols[3].write(row['Description'])
            cols[4].write(str(row['Total Score']))
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
                        'S.No': key+1,
                        'Name': exam["name"],
                        'Date': exam["conducted_date"],
                        'Description': exam["description"],
                        'Total Score': exam["total_marks"],
                        # Store uploaded file info or handle file processing here
                        'Files': exam["file_name"]
                    }
            modified_exams.append(item)
        st.session_state.exam_details = modified_exams
def get_references_details():
    references_get_url = HOST_NAME + "/quick-score/context"
    query_params = {
        'user_id': st.session_state.user_id
    }
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.get(references_get_url, params=query_params, headers=headers)
        if response.status_code == 200:
            reference_result = response.json()

            reference_dictionary = {}
            for reference in reference_result:
                key = reference['name']
                value = reference['id']
                reference_dictionary[key] = value
            return reference_dictionary
        
        else:
            st.error(f"Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
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
def add_exam(json_data, file_upload):

    create_exam_url = HOST_NAME + "/quick-score/exams"
    
    # with open(file_url, 'rb') as pdf_file:
    multipart_data = MultipartEncoder(
        fields = {
            # 'file': ('answerkey.pdf', open(file_url, 'rb'), 'application/pdf'),
            'file': (file_upload.name, file_upload.getvalue(), 'application/pdf'),
            'exam': json.dumps(json_data)
        }
    )   
    headers = {'Content-Type': multipart_data.content_type}  
    
    with st.spinner("Uploading exam details..."):
        response = requests.post(create_exam_url, data=multipart_data.to_string(), headers=headers)
        st.spinner("Document received.")

    if response.status_code == 200:
        st.success("Student added successfully.")
        # Optionally, rerun to refresh the data
        st.experimental_rerun()
    else:
        print("response json=", response.json())
        st.error(f"Failed to add exam. Status code: {response.status_code}")