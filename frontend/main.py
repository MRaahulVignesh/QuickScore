import streamlit as st
import redirect as rd
from students import create_students
from exams import create_exams
from evaluations import create_evaluations
from references import create_references
from individual import create_individual_evaluation_page
import time
import login as login

st.set_page_config(page_title="GradeMe", layout="wide")

st.session_state.user_id = 1

# Initialize session state variables outside the function
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []
if 'exam_details' not in st.session_state:
    st.session_state.exam_details = []
if 'show_overlay' not in st.session_state:
    st.session_state.show_overlay = False

def custom_button(text, on_click=None, key=None):
    button_style = """
        <style>
            div.stButton > button:first-child {
                background-color: #0095ee;
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
    return st.button(text, on_click=on_click, key=key)

def set_bg_hack_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url("https://cdn.pixabay.com/photo/2023/11/17/04/25/04-25-52-168_1280.jpg");
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
    
def create_homepage():
    # set_bg_hack_url()

    with st.container():
        st.title("Grade and Respond")
        st.write(" Efficiently grade and provide feedback on student answer papers")
        if custom_button("Login", on_click=rd.go_to_exams, key="custom_login"):
            pass
        
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
# login page deactivated for testing purposes
if st.session_state['page'] == 'login':
    login.login_page()
elif st.session_state['page'] == 'signup':
    login.signup_page() 


if st.session_state['page'] == 'home':
    create_homepage()
elif st.session_state['page'] == 'students':
    create_students()
elif st.session_state['page'] == 'exams':
    create_exams()
elif st.session_state['page'] == 'evaluations':
    create_evaluations()
elif st.session_state['page'] == 'references':
    create_references()
elif st.session_state['page'] == 'individual':
    create_individual_evaluation_page()

#Display image
    # local_image_path = "bg.png"
    # st.image(local_image_path, caption='', use_column_width=True)


    #Wormhole image - https://cdn.pixabay.com/photo/2020/06/19/22/33/wormhole-5319067_960_720.jpg