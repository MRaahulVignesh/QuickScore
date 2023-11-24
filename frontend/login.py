import streamlit as st
import hashlib
import frontend.redirect as rd
from frontend.exams import  create_exams
from backend.core.user_core import UserCore
import requests

# Function to hash passwords
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# Function to check the hashed password
def check_hashes(password, hashed_text):
    # commenting this line for the time being
    # if make_hashes(password) == hashed_text:
    if password == hashed_text:
        return hashed_text
    return False

# # Database mockup
user_data = {
    "e1": ("u1", "p1"),
    "email2@example.com": ("username2", "hash_of_password2")
    # Add more users as needed
}
# # Example to generate a hash for a plain text password
plain_text_password = "p1"
hashed_password = hashlib.sha256(plain_text_password.encode()).hexdigest()


def is_logged_in():
    return st.session_state.get('logged_in', False)

# Page Functions
def login_page():

    if is_logged_in():
        # st.success(f"Logged In as {st.session_state['user_name']}")
        st.session_state['page'] = 'exams'
        return

    st.title("Login Page")
    email = st.text_input("Email")
    password = st.text_input("Password", type='password')
    if st.button("Login", key='login'):
        try:
            user_core = UserCore()
            login_result = user_core.authenticate_user(email, password)
            if login_result is not None:
                st.session_state['user_id'] = login_result['user_id']
                st.session_state['username'] = login_result['name']
                st.session_state['logged_in'] = True
                st.experimental_rerun()
        except Exception as error:
            print(error)
            st.error("Login Error!!")
            
        # hashed_password = make_hashes(password)
        found_user = user_data.get(email, False)
        if found_user and check_hashes(password, found_user[1]):
            st.session_state['logged_in'] = True  # Set login state
            st.session_state['user_name'] = found_user[0]  # Store user name
            st.success(f"Logged In as {found_user[0]}")
            # login_page()  # Set the page to 'exams'
        else:
            st.error("Incorrect Email/Password")

    if st.button("Sign Up"):
        st.session_state['page'] = 'signup'

def signup_page():
    st.title("Signup Page")
    new_name = st.text_input("Enter Full Name", key='new_name')
    new_email = st.text_input("Enter Email", key='new_email')
    new_password = st.text_input("Enter Password", type='password', key='new_password')
    
    if st.button("Create Account"):
        user_core = UserCore()
        signup_result = user_core.create_user(new_name, new_email, new_password)
        # signup_result = perform_backend_create_user(new_name, new_email, new_password)

        if signup_result is not None:
            st.success("Account Created Successfully. Please go back to Login.")
            st.session_state['page'] = 'login'
        
    if st.button("Back to Login"):
        st.session_state['page'] = 'login'

def perform_backend_login(email, password):
    
    url = "http://localhost:8000/quick-score/users/login"
    data = {'email': email, 'password': password}

    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error login: {response.status_code}")
        return None
    
def perform_backend_create_user(name, email, password):
    url = "http://localhost:8000/quick-score/users"
    data = {'email': email, 'password': password, 'name': name}

    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Could not create user!!")
        return None

# def main():    
#     if 'page' not in st.session_state:
#         st.session_state['page'] = 'login'

#     if st.session_state['page'] == 'login':
#         login_page()
#     elif st.session_state['page'] == 'signup':
#         signup_page()

# if __name__ == '__main__':
#     main()
