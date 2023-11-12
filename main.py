import streamlit as st
import pandas as pd

# Set the page configuration for the Streamlit app
st.set_page_config(page_title="GradeMe", layout="wide")

# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

# Function to navigate to the dashboard
def go_to_dashboard():
    st.session_state['page'] = 'dashboard'

# Function to navigate to the upload page
def go_to_upload():
    st.session_state['page'] = 'upload'

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
    
    if custom_button("Get Started", on_click=go_to_upload):
        pass  # The button click will change the session state to 'upload'

    st.write("---")

    st.header("Streamline Your Grading Process")
    st.write("With our website, you can easily grade answer papers and provide comprehensive feedback to students. Save time and effort while ensuring accurate grading.")

    st.write("---")

    st.subheader("Website Grading")
    st.write("See how our website grades answer papers")

    if custom_button("Learn More"):
        pass  # Placeholder for 'Learn More' button action

    st.write("---")

    st.subheader("FAQ")
    st.write("Common questions")

    # ... (rest of your FAQ expanders)

def create_dashboard():
    # st.sidebar.header("Grade Me")
    # st.sidebar.button("New Scan", on_click=go_to_upload)
    # st.sidebar.button("My Scans", on_click=go_to_dashboard)
    # st.sidebar.button("Shared With Me")
    # st.sidebar.button("Recent Scans")
    # st.sidebar.button("Text Compare")
    # Sidebar
    with st.sidebar:
        st.header("Grade Me")
        if st.button("New Scan"):
            go_to_upload()
        # Correctly assigning the on_click parameter
        if st.button("My Scans"):
            go_to_dashboard()
    st.title("My Scans")

    # Placeholder data for the table
    data = {
        "Type": ["pdf", "pdf"],
        "Name": ["Yuvarej Selvam - Mid 1 Answer paper.pdf", "Sample-report.pdf"],
        "Date": ["Nov 11, 2023", "Nov 11, 2023"],
        "AI Content Detected": ["No", "Yes"],
        "Plagiarism Score": ["0%", "43%"],
    }
    df = pd.DataFrame(data)
    
    st.table(df)

def create_upload_page():

        # Sidebar
    with st.sidebar:
        st.header("Grade Me")
        if st.button("New Scan"):
            go_to_upload()
        # Correctly assigning the on_click parameter
        if st.button("My Scans"):
            go_to_dashboard()

            
    st.title("Upload")
    st.write("Upload the question paper here.")
    uploaded_file = st.file_uploader("", type=['pdf', 'docx', 'txt'])
    if uploaded_file is not None:
        # Handle the uploaded file
        st.write("File Uploaded: ", uploaded_file.name)

# Main app logic
if st.session_state['page'] == 'home':
    create_homepage()
elif st.session_state['page'] == 'dashboard':
    create_dashboard()
elif st.session_state['page'] == 'upload':
    create_upload_page()

