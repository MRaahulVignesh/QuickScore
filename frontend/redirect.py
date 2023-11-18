import streamlit as st
def go_to_students():
    st.session_state['page'] = 'students'

def go_to_exams():
    st.session_state['page'] = 'exams'

def go_to_evaluations():
    st.session_state['page'] = 'evaluations'

def go_to_login():
    st.session_state['page'] = 'login'

def go_to_references():
    st.session_state['page'] = 'references'