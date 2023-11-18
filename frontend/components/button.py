import streamlit as st


def custom_button(text, key, button_style):
    
    button_html = f'<button type="button" class="css-1cpxqw2 edgvbvh1" style="{button_style}">{text}</button>'
    st.markdown(button_html, unsafe_allow_html=True)

    # Detecting if the button is clicked
    if st.session_state.get(key, False):
        st.session_state[key] = False
        return True
    else:
        return False