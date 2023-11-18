import streamlit as st
import requests
import redirect as rd


def render_page(data):
    documents = build_documents(data)

    # App title
    mark_down = """ 
                <hr>
                <h3 style='text-align: center;'>💬 Chat <p style="text-align: center; color: #f8bc64;"> powered by Cohere Coral</p></h3>
                
                """
    st.markdown(mark_down, unsafe_allow_html=True)
        
    # Store LLM generated responses
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "message": "Ask me about this evaluation?"}]

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
        context_message = f"""
            User's Question: {message}
            Context: Current question in discussion is {st.session_state.carousel_index+1}. 
            whenever the user is asking without context, this is the question they is refering to.
        """
        data = {
            "chat_history": chat_history,
            "message": context_message,
            "documents": documents,
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

def build_documents(data):
    json_docs = data["evaluation_details"]
    
    snippet = ""
    for i in range(len(json_docs)):
        current_set = json_docs[i]
        text = f"""
                 Question {i+1}.: 
                    {current_set["question"]}

                    Student Answer for the above question: 
                        {current_set["student_answer"]}
                    Bot's Justification for marks given for the above question:
                        {current_set["justification"]}
                    Correct Answer for the above question:
                        {current_set["answer_key"]}
                    Marks given for student's answer for the above question:
                        {current_set["marks"]}
        """
        snippet+=text
    snippet = f"""Total Marks given for the evaluation: {data["score"]}
    
    """ + snippet
    
    documents = [{
        "title": "Evaluation Details",
        "snippet": snippet
    }]
    return documents
        
    