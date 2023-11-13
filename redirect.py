import streamlit as st
def go_to_students():
    st.session_state['page'] = 'students'

# Function to navigate to the upload page
def go_to_exams():
    st.session_state['page'] = 'exams'

def go_to_evaluations():
    st.session_state['page'] = 'evaluations'