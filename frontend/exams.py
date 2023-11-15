import streamlit as st
from datetime import datetime
import redirect as rd
import pandas as pd

def create_exams_page():
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
    # st.write("Upload the question paper here.")
    # uploaded_file = st.file_uploader("", type=['pdf', 'docx', 'txt'])
    # if uploaded_file is not None and 'uploaded_files' in st.session_state:
    #     # Ensure unique file uploads
    #     if not any(file['Name'] == uploaded_file.name for file in st.session_state['uploaded_files']):
    #         file_info = {
    #             "Type": uploaded_file.type,
    #             "Name": uploaded_file.name,
    #             "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #             "Student Name": "Processing...",
    #             "Percentage": "Processing..."
    #         }
    #         st.session_state['uploaded_files'].append(file_info)
    #         st.write("File Uploaded: ", uploaded_file.name)

  

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
            cols[2].write(row['Date'].strftime("%Y-%m-%d"))  # Format the date
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
                # Remove the selected row from the list of exam details
                del st.session_state.exam_details[i]
                # Update the DataFrame to reflect the deletion and rerender the page
                st.experimental_rerun()