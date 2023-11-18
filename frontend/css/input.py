import streamlit as st    
    
def input_css(): 
    custom_css = """
        <style>
            input {
                color: blue;  /* Text color */
                background-color: yellow;  /* Background color */
            }
        </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)