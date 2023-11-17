import streamlit as st
import requests
import redirect as rd


def render_page():
    # App title
    mark_down = """ 
                <h3 style='text-align: center;'>💬 Chat</h3>
                """
    st.markdown(mark_down, unsafe_allow_html=True)
        
    # Store LLM generated responses
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "message": "How may I help you?"}]

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["message"])

    def generate_response(chat_history, message):
        url = "https://api.cohere.ai/v1/chat"

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer ivWV8ybExfUclVP8Nj8X71jziG0YTYFjHlR8CjJs"
        }

        data = {
            "chat_history": chat_history,
            "message": message,
            "connectors": [{"id": "web-search"}]
        }

        response = requests.post(url, json=data, headers=headers)
        print(response.json())
        chat_response = response.json()["text"]

        return chat_response

    # User-provided prompt
    if prompt := st.chat_input(disabled=False):
        st.session_state.messages.append({"role": "user", "message": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(st.session_state.messages, prompt) 
                st.write(response) 
        message = {"role": "assistant", "message": response}
        st.session_state.messages.append(message)