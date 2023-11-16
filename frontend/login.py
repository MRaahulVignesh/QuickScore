# import streamlit as st
# import hashlib


# # Function to hash passwords
# def make_hashes(password):
#     return hashlib.sha256(str.encode(password)).hexdigest()

# # Function to check the hashed password
# def check_hashes(password, hashed_text):
#     # commenting this line for the time being
#     # if make_hashes(password) == hashed_text:
#     if password == hashed_text:
#         return hashed_text
#     return False

# # # Database mockup
# # user_data = {
# #     "e1": ("u1", "p1"),
# #     "email2@example.com": ("username2", "hash_of_password2")
# #     # Add more users as needed
# # }
# # # Example to generate a hash for a plain text password
# # plain_text_password = "p1"
# # hashed_password = hashlib.sha256(plain_text_password.encode()).hexdigest()
# # print("hashed_password",hashed_password)


# # Page Functions
# def login_page():
#     st.title("Login Page")
#     email = st.text_input("Email")
#     password = st.text_input("Password", type='password')
#     if st.button("Login"):
#         hashed_password = make_hashes(password)
#         found_user = user_data.get(email, False)
#         print("found_user", found_user)
#         print("check_hashes(password, found_user[1])=", check_hashes(password, found_user[1]))
#         print("password=", password)
#         print("found_user[1]=", found_user[1])
#         if found_user and check_hashes(password, found_user[1]):
#             st.success(f"Logged In as {found_user[0]}")
#             st.session_state['logged_in'] = True  # Set login state
#             st.session_state['page'] = 'home'  # Redirect to home page
#             # create_homepage()

#             # Perform actions on successful login
#         else:
#             st.error("Incorrect Email/Password")

#     if st.button("Sign Up"):
#         st.session_state['page'] = 'signup'

# def signup_page():
#     st.title("Signup Page")
#     new_name = st.text_input("Enter Full Name", key='new_name')
#     new_email = st.text_input("Enter Email", key='new_email')
#     new_password = st.text_input("Enter Password", type='password', key='new_password')
    
#     if st.button("Create Account"):
#         # Here we store the username along with the hashed password
#         user_data[new_email] = (new_name, make_hashes(new_password))
#         st.success("Account Created Successfully. Please go back to Login.")
#         st.session_state['page'] = 'login'
    
#     if st.button("Back to Login"):
#         st.session_state['page'] = 'login'

# # def main():    
# #     if 'page' not in st.session_state:
# #         st.session_state['page'] = 'login'

# #     if st.session_state['page'] == 'login':
# #         login_page()
# #     elif st.session_state['page'] == 'signup':
# #         signup_page()

# # if __name__ == '__main__':
# #     main()
