import streamlit as st
import redirect as rd
import pandas as pd
from datetime import datetime
import requests
import json
import time
from requests_toolbelt.multipart.encoder import MultipartEncoder

if 'reference_details' not in st.session_state:
    st.session_state.reference_details = []
if 'show_overlay' not in st.session_state:
    st.session_state.show_overlay = False

HOST_NAME = "http://localhost:8000"

def create_references():
    populate_references_table()
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
                
                # New fields: name, comments, and file uploader
                name = st.text_input('Name', key='name')
                comments = st.text_area('Comments', key='comments')
                uploaded_file = st.file_uploader('Upload File', accept_multiple_files=False, key='ref_file_uploader')
                
                # Submit button for the form
                submitted = st.form_submit_button('Submit')
                if submitted:
                    # Call the function to add a reference with name, comments, and file name
                    add_reference(name, comments, '/Users/devadharshiniravichandranlalitha/Downloads/Question.pdf')
                    # Hide the overlay
                    st.session_state.show_overlay = False
                    # Clear the session state keys if needed
                    st.session_state.pop('name', None)
                    st.session_state.pop('comments', None)
                    st.session_state.pop('file_uploader', None)
                    st.experimental_rerun()

    # Display the table of reference details with 'View', 'Edit', and 'Delete' buttons
    if st.session_state.reference_details:
        st.write('Reference Details:')
        # Create a DataFrame for the table
        df = pd.DataFrame(st.session_state.reference_details)

        # Display column headers
        col_headers = st.columns((1, 1, 1, 1, 1))
        headers = ["S.No", "Name", "Comments", "File Name", "Delete"]
        for col_header, header in zip(col_headers, headers):
            col_header.write(header)

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
                        'File Name': 'test file',
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

def add_reference(name, comments, file_url):
    reference_data = {
        'name': name,
        'comments': comments,
        'user_id': st.session_state.user_id
    }
    print("reference_data=", reference_data)
    add_references_function(reference_data, file_url)

def add_references_function(json_data, file_url):
    create_ref_url = HOST_NAME + "/quick-score/context"
    
    # with open(file_url, 'rb') as pdf_file:
    multipart_data = MultipartEncoder(
        fields = {
            'file': ('answerkey.pdf', open(file_url, 'rb'), 'application/pdf'),
            'context': json.dumps(json_data)
        }
    )   
    headers = {'Content-Type': multipart_data.content_type}  
    
    with st.spinner("Uploading reference details..."):
        st.write("Searching for data...")
        time.sleep(2)
        st.write("Found URL.")
        time.sleep(1)
        st.write("Processing data...")
        time.sleep(1)
        response = requests.post(create_ref_url, data=multipart_data.to_string(), headers=headers)
        st.spinner("Document received.")

    if response.status_code == 200:
        st.success("Reference added successfully.")
        st.experimental_rerun()
    else:
        print("response json=", response.json())
        st.error(f"Failed to add reference. Status code: {response.status_code}")