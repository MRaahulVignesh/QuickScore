import streamlit as st
import redirect as rd
from students import create_students_page
from exams import create_exams_page
from evaluations import create_evaluations
import time
# import login as login
# Set the page configuration for the Streamlit app
st.set_page_config(page_title="GradeMe", layout="wide")
st.session_state.user_id = 1

#background image test
page_bg_img = '''
<style>
body {
background-image: url("/Users/devadharshiniravichandranlalitha/Documents/lablab/Cohere grade me/QuickScore/frontend/bg-quick-score.png");
background-size: cover;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)

# Initialize session state variables outside the function
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []

if 'exam_details' not in st.session_state:
    st.session_state.exam_details = []
if 'show_overlay' not in st.session_state:
    st.session_state.show_overlay = False
# Initialize session state for page navigation

# if 'uploaded_files' not in st.session_state:
#     st.session_state['uploaded_files'] = []


# Function to create a custom button with Streamlit
def custom_button(text, on_click=None):
    button_style = """
        <style>
            div.stButton > button:first-child {
                background-color: #009688;
                color: white;
                height: 3em;
                border-radius: 5px;
                border: none;
                font-size: 20px;
                font-weight: bold;
                margin: 0.25em;
            }
        </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)
    return st.button(text, on_click=on_click)

def create_homepage():
    st.title("Grade and Respond")
    st.write("Efficiently grade and provide feedback on student answer papers")
    # with st.status("Downloading data...", expanded=True) as status:
    #     st.write("Searching for data...")
    #     time.sleep(2)
    #     st.write("Found URL.")
    #     time.sleep(1)
    #     st.write("Downloading data...")
    #     time.sleep(1)
    #     status.update(label="Download complete!", state="complete", expanded=False)
    # with st.spinner('Uploading exam details...'):
    #     time.sleep(25)
    if custom_button("Get Started", on_click=rd.go_to_exams):
            pass  # The button click will change the session state to 'upload'

    st.write("---")

    st.header("Streamline Your Grading Process")
    st.write("With our website, you can easily grade answer papers and provide comprehensive feedback to students. Save time and effort while ensuring accurate grading.")

    st.write("---")

    # FAQ section
    st.subheader("FAQ")
    st.write("Common questions")
    
    # You can use st.expander to create dropdowns for each FAQ
    faq1 = st.expander("How does the website grade the answer paper?")
    faq1.write("The website uses an algorithm to analyze the content of the answer paper and assign a grade based on predefined criteria.")
    
    faq2 = st.expander("What factors are considered when grading the paper?")
    faq2.write("The website considers factors such as accuracy, clarity, organization, and use of supporting evidence when grading the paper.")
    
    faq3 = st.expander("Can the website provide feedback on specific areas for improvement?")
    faq3.write("Yes, the website provides detailed feedback on areas where the student can improve their answer, including suggestions for further research or examples to support their arguments.")
    
    faq4 = st.expander("Is the grading process automated or manual?")
    faq4.write("The grading process is automated, but it is designed to mimic the evaluation process of a human grader as closely as possible.")





# Main app logic
#login page deactivated for testing purposes
# if 'page' not in st.session_state:
#         st.session_state['page'] = 'login'
# if st.session_state['page'] == 'login':
#     login.login_page()
# elif st.session_state['page'] == 'signup':
#     login.signup_page() 

if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

if st.session_state['page'] == 'home':
    create_homepage()
elif st.session_state['page'] == 'students':
    create_students_page()
elif st.session_state['page'] == 'exams':
    create_exams_page()
elif st.session_state['page'] == 'evaluations':
    create_evaluations()