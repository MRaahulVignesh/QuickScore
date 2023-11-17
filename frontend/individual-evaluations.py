import streamlit as st
import chat

st.set_page_config(layout="wide")

with st.sidebar:
    st.title("Grade Me")
    if st.button("Exams"):
        rd.go_to_exams()
    if st.button("Students"):
        rd.go_to_students()
    if st.button("Evaluations"):
        rd.go_to_evaluations()
    if st.button("Log Out"):
        rd.go_to_exams()
    
    
# Sample data for the carousel
carousel_items = [
    {
        "question": "What is the capital of France?",
        "student_answer": "Paris",
        "marks": "5/5",
        "justification": "The answer is correct and well-justified."
    },
    {
        "question": "What is the boiling point of water?",
        "student_answer": "100 degrees Celsius",
        "marks": "5/5",
        "justification": "Correct answer. The student accurately stated the boiling point of water at standard atmospheric pressure."
    },
    {
        "question": "Who wrote 'To Kill a Mockingbird'?",
        "student_answer": "Harper Lee",
        "marks": "5/5",
        "justification": "Correct. The student correctly identified the author of the novel."
    },
    {
        "question": "Solve for x: 2x + 3 = 9",
        "student_answer": "x = 3",
        "marks": "5/5",
        "justification": "The solution is correct. The student showed good algebraic skills."
    },
    {
        "question": "What is the largest planet in our Solar System?",
        "student_answer": "Jupiter",
        "marks": "5/5",
        "justification": "Correct answer. The student correctly identified Jupiter as the largest planet."
    }
]


def display_info(data):
    markdown_template = f"""
    <style>
        .text-box {{
            border: 1px solid #999;
            border-radius: 5px;
            padding: 10px;
            margin: 10px 0;
            background-color: #f0f0f0;
        }}
    </style>
    <style>
        .scrollable-container {{
            height: 325px; /* Fixed height */
            overflow-y: scroll; /* Make it scrollable */
            border: 1px solid #ccc; /* Optional border */
            padding: 10px;
            margin-bottom: 20px; /* Space between containers */
        }}
    </style>
    <h3 style='text-align: center;'> Answer Set </h3>
    <div class="text-box scrollable-container">
        <div style="font-family: sans-serif;">
            <h6 style="color: #4F8BF9;">Question</h2>
            <p style="color: #000;">{data["question"]}</p>
            <h6 style="color: #4F8BF9;">Student Answer</h2>
            <p style="color: #000;">{data["student_answer"]}</p>
            <h6 style="color: #4F8BF9;">Marks</h2>
            <p style="color: #000;"><b>{data["marks"]}</b></p>
            <h6 style="color: #4F8BF9;">Justification</h2>
            <p style="color: #000;">{data["justification"]}</p>
        </div>
    </div>
    """
    st.markdown(markdown_template, unsafe_allow_html=True)
    
# Initialize session state variables if they don't exist
if 'carousel_index' not in st.session_state:
    st.session_state.carousel_index = 0  # Starting index

# Function to handle carousel movement
def next_item():
    st.session_state.carousel_index = (st.session_state.carousel_index + 1) % len(carousel_items)

def prev_item():
    st.session_state.carousel_index = (st.session_state.carousel_index - 1) % len(carousel_items)

# Main layout

# Layout for carousel controls
col1, col2, col3 = st.columns([2, 10, 2])

# Previous Button
with col1:
    prev_button = st.button("Previous", on_click=prev_item)
    student_name = "Raahul Vignesh"
    student_roll = "111231231"
    st.write("\n\n\n\n\n\n\n\n\n\n\n\n")
    markdown_template1 = f"""
        <div style="font-family: sans-serif;  padding: 10px; border-radius: 10px; border: 1px solid #cccccc; margin: 10px 0;">
            <h6 style="color: #f8bc64; font-size: 16px;">Student Details</h6>
            <p style="font-size: 14px;"><strong>Name:</strong>
            <br style="line-height:0.5px;" />
            <span>{student_name}</span>
            <br style="line-height:0.5px;" />
            <br style="line-height:0.5px;" />
            <strong>Roll No:</strong>
            <br style="line-height:0.5px;" />
            <span>{student_roll}</span>
            </p>
        </div>
    """

    st.markdown(markdown_template1, unsafe_allow_html=True)

# Carousel text
with col2:
    display_info(carousel_items[st.session_state.carousel_index])
    # st.write(carousel_items[st.session_state.carousel_index], anchor='center')

# Next Button
with col3:
    next_button = st.button("Next    ", on_click=next_item)
    score = 4
    total_question_marks = 5
    total_student_marks = 9
    total_marks = 10
    st.write("\n\n\n\n\n\n\n\n\n\n\n\n")
    markdown_template1 = f"""
        <div style="font-family: sans-serif;  padding: 10px; border-radius: 10px; border: 1px solid #cccccc; margin: 10px 0;">
            <h6 style="color: #f8bc64; font-size: 16px;">Scoring</h6>
            <p style="font-size: 14px;">Qust. Score:
            <br style="line-height:0.5px;" />
            <span><strong>{score}/{total_question_marks}</strong></span>
            <br style="line-height:0.5px;" />
            <br style="line-height:0.5px;" />
            Exam Score:
            <br style="line-height:0.5px;" />
            <span><strong>{total_student_marks}/{total_marks}</strong></span>
            </p>
        </div>
    """
    st.markdown(markdown_template1, unsafe_allow_html=True)
    

chat.render_page()
