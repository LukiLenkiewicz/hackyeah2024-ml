import streamlit as st
import ollama

# from scripts folder run the command below
# streamlit run app.py

avatars = {
    "user": ".streamlit/avatars/human.png",
    "assistant": ".streamlit/avatars/logo.png",
}

css_classes = {
    "user": "user-container",
    "assistant": "assistant-container",
}

# Define custom CSS for chat message box
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

st.title("EasyTalk")
st.markdown(custom_css, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "Hi, how can I help you?"})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message['content'])

prompt = st.chat_input("I have a problem with ...")

if prompt:

    with st.chat_message("user") as uchat:
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Processing ..."):
        result = ollama.chat(model="llama3", messages=st.session_state.messages)
        response = result["message"]["content"]
        with st.chat_message("assistant"):
            st.markdown(response)
    # response = f"Echoing: {prompt}"
    # with st.chat_message("assistant"):
    #     st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})




