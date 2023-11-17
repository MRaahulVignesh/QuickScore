import streamlit as st
import redirect as rd
import pandas as pd
from datetime import datetime
import requests

if 'reference_details' not in st.session_state:
    st.session_state.reference_details = []
if 'show_overlay' not in st.session_state:
    st.session_state.show_overlay = False

HOST_NAME = "http://localhost:8000"

def create_references():
    # populate_references_table()

    with st.sidebar:
        st.header("Grade Me")
        if st.button("Exams", key='ref_exams'):
            rd.go_to_exams()
        if st.button("Students", key='ref_students'):
            rd.go_to_students()
        if st.button("References", key='ref_references'):
            rd.go_to_references()
        if st.button("Log Out", key='ref_logout'):
            rd.go_to_exams()

    st.title("References")

    # Initialize a session state variable for storing exam details
    if 'reference_details' not in st.session_state:
        st.session_state.reference_details = []

    # Overlay toggle
    if 'show_overlay' not in st.session_state:
        st.session_state.show_overlay = False

    # Button to show the overlay
    if st.button('Upload Reference Details'):
        st.session_state.show_overlay = True

    # The overlay layout
    if st.session_state.show_overlay:
        with st.container():
            with st.form(key='reference_details_form'):
                # Automatically generate the next serial number
                serial_no = len(st.session_state.reference_details) + 1
                # Display the serial number to the user
                st.write(f"Serial No: {serial_no}")
                
                # New fields: name, comments, and file uploader
                name = st.text_input('Name', key='name')
                comments = st.text_area('Comments', key='comments')
                uploaded_file = st.file_uploader('Upload File', accept_multiple_files=False, key='ref_file_uploader')
                
                # Submit button for the form
                submitted = st.form_submit_button('Submit')
                if submitted:
                    # Call the function to add a reference with name, comments, and file name
                    add_reference(name, comments, uploaded_file)
                    # Hide the overlay
                    st.session_state.show_overlay = False
                    # Clear the session state keys if needed
                    st.session_state.pop('name', None)
                    st.session_state.pop('comments', None)
                    st.session_state.pop('file_uploader', None)

    # Display the table of reference details with 'View', 'Edit', and 'Delete' buttons
    if st.session_state.reference_details:
        st.write('Reference Details:')
        # Create a DataFrame for the table
        df = pd.DataFrame(st.session_state.reference_details)

        # Display column headers
        col_headers = st.columns((1, 2, 2, 2, 2, 1, 1))
        headers = ["Serial No", "Name", "Comments", "File Name", "Action"]
        for col_header, header in zip(col_headers, headers):
            col_header.write(header)

        # Iterate over the DataFrame to display the table with buttons
        for i, row in df.iterrows():
            reference_id = row["reference_id"]
            cols = st.columns((1, 2, 2, 2, 2, 1, 1))
            cols[0].write(row['Serial No'])
            cols[1].write(row['Name'])
            cols[2].write(row['Comments'])
            cols[3].write(row['File Name'])
            if cols[4].button('Delete', key=reference_id):
                delete_reference(reference_id)
                st.experimental_rerun()
                
def populate_references_table():

    # The URL for the API endpoint
    references_get_url = HOST_NAME + "/quick-score/references"
    query_params = {
        'user_id': st.session_state.user_id
    }
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.get(references_get_url, params=query_params, headers=headers)
        if response.status_code == 200:
            reference_result = response.json()
        else:
            st.error(f"Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        reference_result = []
        

    modified_references = []
    if len(reference_result) > 0:
        for key, reference in enumerate(reference_result):
            print(reference)
            item = {
                        'Serial No': key + 1,
                        'Name': reference["name"],
                        'Email': reference["email"],
                        'Roll Number': reference["roll_no"],
                        'reference_id': reference["id"]
                    }
            modified_references.append(item)
        st.session_state.reference_details = modified_references
    
def delete_reference(reference_id):

    # The URL for the API endpoint
    reference_delete_url = HOST_NAME + "/quick-score/references/" + str(reference_id) 

    # Set the appropriate headers for JSON - this is important!
    headers = {'Content-Type': 'application/json'}

    # Send the POST request
    response = requests.delete(reference_delete_url, headers=headers)
    print(response)
    # Check if the request was successful
    if response.status_code == 200:
        st.session_state.reference_details = [
            reference for reference in st.session_state.reference_details if reference['reference_id'] != reference_id
        ]
        st.experimental_rerun()
    else:
        print(f"Failed to delete reference record. Status code: {response.status_code}")

def add_reference(name, email, roll_number):
    # The URL for the API endpoint to add a reference
    reference_add_url = HOST_NAME + "/quick-score/references" 

    # The data you want to send with the POST request
    reference_data = {
        'name': name,
        'email': email,
        'roll_no': roll_number,
        'user_id': st.session_state.user_id
    }

    # Set the appropriate headers for JSON
    headers = {'Content-Type': 'application/json'}

    # Send the POST request
    response = requests.post(reference_add_url, json=reference_data, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        st.success("Reference added successfully.")
        st.experimental_rerun()
    else:
        st.error(f"Failed to add reference. Status code: {response.status_code}")
