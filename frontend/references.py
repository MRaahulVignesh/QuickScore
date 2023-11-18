import streamlit as st
import redirect as rd
import pandas as pd
from datetime import datetime
import requests
import json
from side_bar import render_side_bar
import time
from requests_toolbelt.multipart.encoder import MultipartEncoder

if 'reference_details' not in st.session_state:
    st.session_state.reference_details = []
if 'show_overlay' not in st.session_state:
    st.session_state.show_overlay = False

HOST_NAME = "http://localhost:8000"

def create_references():
    populate_references_table()
    render_side_bar()

    st.title("References")

    # Initialize a session state variable for storing exam details
    if 'reference_details' not in st.session_state:
        st.session_state.reference_details = []

    # Overlay toggle
    if 'show_overlay' not in st.session_state:
        st.session_state.show_overlay = False

    # The overlay layout
    with st.expander("Upload Reference Details"):
        with st.container():
            with st.form(key='reference_details_form'):
                
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
                    st.experimental_rerun()

    # Display the table of reference details with 'View', 'Edit', and 'Delete' buttons
    if st.session_state.reference_details:

        st.markdown("<br>", unsafe_allow_html=True)
        # Create a DataFrame for the table
        df = pd.DataFrame(st.session_state.reference_details)

        # Display column headers
        col_headers = st.columns((1, 1, 1, 1, 1))
        headers = ["S.No", "Name", "Comments", "File Name", "Delete"]
        for col_header, header in zip(col_headers, headers):
            col_header.markdown(f'<h5 style="color: #4F8BF9;"><strong>{header}</strong></h5></div>', unsafe_allow_html=True)
            # col_header.write(header)

        # Iterate over the DataFrame to display the table with buttons
        for i, row in df.iterrows():
            reference_id = row["id"]
            cols = st.columns((1, 1, 1, 1, 1))
            cols[0].write(str(row['S.No']))
            cols[1].write(row['Name'])
            cols[2].write(row['Comments'])
            cols[3].write(row['File Name'])
            if cols[4].button('🗑️', key=reference_id):
                delete_reference(reference_id)
                st.experimental_rerun()



def populate_references_table():

    # The URL for the API endpoint
    references_get_url = HOST_NAME + "/quick-score/context"
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
                        'S.No': key + 1,
                        'Name': reference["name"],
                        'Comments': reference["comments"],
                        'File Name': reference["file_name"],
                        'id': reference["id"]
                    }
            modified_references.append(item)
        st.session_state.reference_details = modified_references
    
def delete_reference(reference_id):

    # The URL for the API endpoint
    reference_delete_url = HOST_NAME + "/quick-score/context/" + str(reference_id) 

    # Set the appropriate headers for JSON - this is important!
    headers = {'Content-Type': 'application/json'}

    # Send the POST request
    response = requests.delete(reference_delete_url, headers=headers)
    print(response)
    # Check if the request was successful
    if response.status_code == 200:
        st.session_state.reference_details = [
            reference for reference in st.session_state.reference_details if reference['id'] != reference_id
        ]
        st.experimental_rerun()
    else:
        print(f"Failed to delete reference record. Status code: {response.status_code}")

def add_reference(name, comments, file_bytes):
    reference_data = {
        'name': name,
        'comments': comments,
        'user_id': st.session_state.user_id
    }
    add_references_function(reference_data, file_bytes)

def add_references_function(json_data, file_bytes):
    create_ref_url = HOST_NAME + "/quick-score/context"
    
    # with open(file_url, 'rb') as pdf_file:
    multipart_data = MultipartEncoder(
        fields = {
            'file': (file_bytes.name, file_bytes, 'application/pdf'),
            'context': json.dumps(json_data)
        }
    )   
    headers = {'Content-Type': multipart_data.content_type}  
    
    with st.spinner("Uploading reference details..."):
        response = requests.post(create_ref_url, data=multipart_data.to_string(), headers=headers)

    if response.status_code == 200:
        st.success("Reference added successfully.")
        st.experimental_rerun()
    else:
        print("response json=", response.json())
        st.error(f"Failed to add reference. Status code: {response.status_code}")