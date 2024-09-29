import streamlit as st
from hackyeah.main import pipeline

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
    "user": "human",  # "../avatars/human.png",
    "assistant": "assistant"  # "../avatars/logo.png",
}

st.markdown(custom_css, unsafe_allow_html=True)

st.title("EasyTalk")

print("Page link", st.session_state.page_link)

if not st.session_state.messages:
    with st.chat_message("assistant", avatar=avatars["assistant"]):
        st.markdown(f"You provided me with: {st.session_state.page_link}\nHi, how can I help you?")

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=avatars[message["role"]]):
        st.markdown(message['content'])

prompt = st.chat_input("I have a problem with ...")

if prompt:
    with st.chat_message("user", avatar=avatars["user"]):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Processing ..."):
        url, result =pipeline(st.session_state.page_link, prompt)
        response = f"""URL: {url}   
        {result}"""
        with st.chat_message("assistant", avatar=avatars["assistant"]):
            st.markdown(response)
    # response = f"Echoing: {prompt}"
    # with st.chat_message("assistant"):
    #     st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
