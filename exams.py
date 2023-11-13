import streamlit as st
from datetime import datetime
import redirect as rd


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
            # The form inside the overlay
            with st.form(key='exam_details_form'):
                # Input fields
                name = st.text_input('Name')
                date = st.date_input('Date', value=datetime.today())
                total_score = st.text_input('Total Score')
                
                # Submit button for the form
                submitted = st.form_submit_button('Submit')
                if submitted:
                    # Hide the overlay
                    st.session_state.show_overlay = False
                    # Store the submitted values in the session state
                    st.session_state.exam_details.append({
                        'Name': name,
                        'Date': date,
                        'Total Score': total_score
                    })
                    # Clear the input fields after submission
                    st.session_state['name'] = ""
                    st.session_state['date'] = datetime.today()
                    st.session_state['total_score'] = ""

    # Display the table of exam details
    if st.session_state.exam_details:
        st.write('Exam Details:')
        st.table(st.session_state.exam_details)

