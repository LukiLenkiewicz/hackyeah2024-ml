import streamlit as st
from hackyeah.main import pipeline

custom_css = """
<style>

    /* Custom style for the user chat message */
    .stChatMessage.eeusbqq4 {
        background-color: #3E7E8C; /* Light blue background */
    }
    
    
    
    .st-emotion-cache-11j9wlh a {
        color: #DFEEF4;
        text-decoration: none;
        font-weight: bold;
    }
    
    [data-testid=stSidebarNav] {
        display: none;
    }
    [data-testid=stSidebarContent] {
        background-color: #255059;
        color: black;
    }
    a {
        color: #DFEEF4;
        text-decoration: none;
        font-weight: bold;
    }
    
    a:hover a:visited {
        color: #DFEEF4; 
        text-decoration:none; 
        cursor:pointer;  
        font-weight: bold;
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

st.sidebar.page_link("pages/chat.py")
st.sidebar.page_link("pages/home.py")

st.title("EasyTalk")

print("Page link", st.session_state.page_link)

if not st.session_state.messages:
    with st.chat_message("assistant", avatar=avatars["assistant"]):
        st.markdown(f"Witaj. Jestem inteligentnym asystentem wyszukiwania informacji na stronach internetowych. Zaczniemy od podanej przez Ciebie strony: {st.session_state.page_link}\n\nJak mogę Ci pomóc?")

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=avatars[message["role"]]):
        st.markdown(message['content'])

prompt = st.chat_input("Pomóż mi znaleźć...")

if prompt:
    with st.chat_message("user", avatar=avatars["user"]):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Wyszukuję ..."):
        url, result = pipeline(st.session_state.page_link, prompt)
        response = f"""Pod tym adresem możesz znaleźć potrzebne Ci informacje: {url}   
        {result}"""
        with st.chat_message("assistant", avatar=avatars["assistant"]):
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
