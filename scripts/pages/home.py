import streamlit as st
import ollama

custom_css = """
<style>

    /* Custom style for the user chat message */
    .stChatMessage.eeusbqq4 {
        background-color: #3E7E8C; /* Light blue background */

    }

    /* Custom style for the avatar */
    .stChatMessage.st-emotion-cache-4oy321.eeusbqq4 {
        background-color: #A67153;
    }

    [data-baseweb=textarea] {
        color: black;
        border: 1px solid #024059;
    }

    [type=textarea] {
        color: black;
        caret-color: black;
    }

    #easytalk {
        color: black;
    }

    .stSpinner {
        color: black;
    }

    header {
        color: black;
    }

</style>
"""

avatars = {
    "user": "user",  # "../avatars/human.png",
    "assistant": "assistant"  # "../avatars/logo.png",
}

st.markdown(custom_css, unsafe_allow_html=True)
st.title("EasyTalk")
st.session_state.page_link = st.text_input("Enter a website link")

if st.session_state.page_link:

    with st.spinner('Processing ...'):
        st.session_state.messages = []
        initial_message = {"role": "user",
                           "content": f"You have the following link: {st.session_state.page_link}. Briefly tell me what I can find here."}

        result = ollama.chat(model="llama3", messages=[initial_message])
        response = result["message"]["content"]

        print(f"Model response {response}")

        print(f"avatars: {avatars}")
        st.session_state.messages.append({"role": "assistant", "content": response})
        print(f"Messages 2: {st.session_state.messages}")

    if st.session_state.messages[0]['content']:
        st.switch_page("pages/chat.py")




