import streamlit as st
import redirect as rd

def render_side_bar():
    
    with st.sidebar:
        st.markdown(
        """
        <style>
        .st-emotion-cache-6qob1r {
            background-color: #0095ee;
        }
        .sidebar .sidebar-content {
            padding-top: 0rem;
            text-align: center;
            background-color: #C0C9CB !important;
        }
        .css-18e3th9 {
            padding: 0.25rem 1rem;
            text-align: center;
            background-color: #f0f0f0;
        }
        .stButton>button {
            width: 80%;  /* Make the buttons use the full width */
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
        st.markdown("""
            <div style="text-align: center;">
                <img class="profile-img" src="https://i.ibb.co/jrpb6Xd/profile1.png" alt="Profile icon">
                <p class="welcome-msg">Welcome Author</p>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("Exams", key='exam_exams'):
            rd.go_to_exams()
        if st.button("Students", key='exam_students'):
            rd.go_to_students()
        if st.button("References", key='exam_references'):
            rd.go_to_references()
        if st.button("Log Out", key='exam_logout'):
            rd.go_to_exams()