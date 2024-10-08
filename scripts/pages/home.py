import streamlit as st

custom_css = """
<style>
    
    /* Custom style for the user chat message */
    .stChatMessage.eeusbqq4 {
        background-color: #3E7E8C; /* Light blue background */

    }
    
    [data-testid=stSidebarNav] {
        display: none;
    }
    
    [data-testid=stSidebarContent] {
        background-color: #255059;
        color: black;
    }
    
    body {
        color: black;
    }
    
    /* Custom style for the avatar */
    .stChatMessage.st-emotion-cache-4oy321.eeusbqq4 {
        background-color: #A67153;
    }
    
    .stTextInput {
        background-color: #255059;
        padding: 10px;
        color: black;
    }
    
    [data-baseweb=base-input] .st-bc {
        color: black;
        cursor: pointer;
    }
    
    input {
        background-color: #255059;
        padding: 10px;
        color: black;
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

st.markdown(custom_css, unsafe_allow_html=True)

st.sidebar.page_link("pages/chat.py")
st.sidebar.page_link("pages/home.py")

st.title("EasyTalk")
st.session_state.page_link = st.text_input("Podaj proszę adres strony internetowej, z której chcesz uzyskać informacje.")

if st.session_state.page_link:
    st.session_state.messages = []
    st.switch_page("pages/chat.py")
    
    # TEMP
    # with st.spinner('Processing ...'):
    #     st.session_state.messages = []
    #     initial_message = {"role": "user",
    #                        "content": f"You have the following link: {st.session_state.page_link}. Briefly tell me what I can find here."}

    #     result = ollama.chat(model="llama3", messages=[initial_message])
    #     response = result["message"]["content"]

    #     print(f"Model response {response}")

    #     print(f"avatars: {avatars}")
    #     st.session_state.messages.append({"role": "assistant", "content": response})
    #     print(f"Messages 2: {st.session_state.messages}")

    # if st.session_state.messages[0]['content']:
    #     st.switch_page("pages/chat.py")




