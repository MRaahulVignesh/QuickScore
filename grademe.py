import streamlit as st
import pandas as pd
from io import StringIO

# Set the page configuration for the Streamlit app
st.set_page_config(page_title="GradeMe", layout="wide")

# Function to create a custom button with Streamlit
def custom_button(text):
    st.markdown(f"""
    <style>
    div.stButton > button:first-child {{
        background-color: #009688;
        color: white;
        height: 3em;
        border-radius: 5px;
        border: none;
        font-size: 20px;
        font-weight: bold;
        margin: 0.25em;
    }}
    </style>
    """, unsafe_allow_html=True)
    return st.button(text)

# Function to replicate the website design
def create_website():
    # Header section
    # st.image("img1.jpg", use_column_width='always')
    st.title("Grade and Respond")
    st.write("Efficiently grade and provide feedback on student answer papers")
    
    # if custom_button("Upload File Here"):
        # Code to handle file upload
        # Create a file uploader widget
    uploaded_file = st.file_uploader("Choose a file")

    # Check if a file has been uploaded
    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        st.write("Uploaded file is {} bytes long".format(len(bytes_data)))

        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        st.write(stringio.read())

        # To read file as string (if it's a text file):
        string_data = stringio.read()
        st.write(string_data)

        # To read file as CSV or Excel, you can use Pandas:
        if uploaded_file.type == "text/csv":
            df = pd.read_csv(uploaded_file)
            st.write(df)
        elif "excel" in uploaded_file.type:
            df = pd.read_excel(uploaded_file)
            st.write(df)

        # Perform your file processing action here
        # For example, save the file to disk
        with open("saved_file", "wb") as f:
            f.write(bytes_data)
        st.success("File saved")
        # pass
    
    st.write("---")  # Horizontal line

    # Grading Process section
    st.header("Streamline Your Grading Process")
    st.write("With our website, you can easily grade answer papers and provide comprehensive feedback to students. Save time and effort while ensuring accurate grading.")
    
    st.write("---")  # Horizontal line

    # Website Grading section
    st.subheader("Website Grading")
    st.write("See how our website grades answer papers")
    
    if custom_button("Learn More"):
        # Code to handle Learn More action
        pass
    
    st.write("---")  # Horizontal line

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

# Call the function to create the website
create_website()
