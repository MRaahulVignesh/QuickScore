import streamlit as st
import redirect as rd
import pandas as pd
from datetime import datetime


if 'evaluation_details' not in st.session_state:
    st.session_state.evaluation_details = []
if 'show_overlay' not in st.session_state:
    st.session_state.show_overlay = False
def create_evaluations():
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

    st.title("Evaluations")

    # Initialize a session state variable for storing exam details
    if 'evaluation_details' not in st.session_state:
        st.session_state.evaluation_details = []

    # Overlay toggle
    if 'show_overlay' not in st.session_state:
        st.session_state.show_overlay = False

    # Button to show the overlay
    if st.button('Upload Evaluation Details'):
        st.session_state.show_overlay = True

    # The overlay layout
    if st.session_state.show_overlay:
        with st.container():
            with st.form(key='evaluation_details_form'):
                # Input fields with default values from session_state
                # Input fields
                # Automatically generate the next serial number
                serial_no = len(st.session_state.evaluation_details) + 1
                # Display the serial number to the user
                st.write(f"Serial No: {serial_no}")
                student_name = st.text_input('Name', key='student_name')
                roll_number = st.text_input('Roll Number', key='roll_number')
                score = st.text_input('Score', key='score')

                # Submit button for the form
                submitted = st.form_submit_button('Submit')
                if submitted:
                    # Store the submitted values in the session state
                    st.session_state.evaluation_details.append({
                        'Serial No': serial_no,
                        'Name': student_name,
                        'Roll Number': roll_number,
                        'Score': score
                    })
                    # Hide the overlay
                    st.session_state.show_overlay = False
        

    # Display the table of exam details
    if st.session_state.evaluation_details:
        st.write('Evaluation Details:')
        df = pd.DataFrame(st.session_state.evaluation_details)
        # Convert DataFrame to HTML and use st.markdown to display it, without the index
        st.markdown(df.to_html(index=False), unsafe_allow_html=True)