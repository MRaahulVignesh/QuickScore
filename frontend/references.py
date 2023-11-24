import streamlit as st
import frontend.redirect as rd
import pandas as pd
from frontend.side_bar import render_side_bar
from backend.core.context_core import ContextCore
import tempfile
from langchain.document_loaders import PyPDFLoader


def create_references():
    populate_references_table()
    render_side_bar()

    st.title("References")

    # Initialize a session state variable for storing exam details
    if 'reference_details' not in st.session_state:
        st.session_state.reference_details = []

    if 'is_expanded' not in st.session_state:
        st.session_state['is_expanded'] = False

    # The overlay layout
    with st.expander("Upload Reference Details", expanded=st.session_state['is_expanded']):
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
                    st.session_state['is_expanded'] = False
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
    user_id = st.session_state["user_id"]
    reference_core = ContextCore()
    try:
        reference_result = reference_core.get_contexts_by_user_id(user_id)
    except Exception as error:
        st.error("Could not populate references!")
        
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
    reference_core = ContextCore()
    try:
        reference_core.delete_context(reference_id)
    except Exception as error:
        st.error("Delete Operation Failed")
    st.session_state.reference_details = [
            reference for reference in st.session_state.reference_details if reference['id'] != reference_id
        ]
    st.experimental_rerun()


def add_reference(name, comments, uploaded_file):
    user_id = st.session_state["user_id"]
    reference_data = {
        'name': name,
        'comments': comments,
        'user_id': user_id
    }
    add_references_function(reference_data, uploaded_file)

def add_references_function(json_data, uploaded_file):
    
    reference_core = ContextCore()
    
    context_pdf = None
        
    with st.spinner("Uploading Reference details..."):
        with tempfile.NamedTemporaryFile(delete=True) as temp_file:

            file_contents = uploaded_file.read()

            temp_file.write(file_contents)
            temp_file.flush()

            temp_file_path = temp_file.name
            
            loader = PyPDFLoader(temp_file_path)
            context_pdf = loader.load()
        
        try:
            reference = reference_core.create_context(input=json_data, filename=uploaded_file.name, context_pdf=context_pdf)
            st.success("Reference added successfully.")
        except Exception as error:
            print(error)
            st.error("Failed to add reference.")
        
