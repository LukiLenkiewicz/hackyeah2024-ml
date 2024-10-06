import streamlit as st
from dotenv import load_dotenv
# from scripts folder run the command below
# streamlit run app.py

load_dotenv()


# Define custom CSS for chat message box
custom_css = """
<style>

    body {
        background-color: #D8EBF2;
    }
    
    [data-testid=stSidebarNav] {
        display: none;
    }
    
    
    [data-testid=stSidebarContent] {
        background-color: #255059;
        color: black;
    }


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
    "user": "user", # "../avatars/human.png",
    "assistant": "assistant" # "../avatars/logo.png",
}

st.markdown(custom_css, unsafe_allow_html=True)

st.sidebar.page_link("pages/chat.py")
st.sidebar.page_link("pages/home.py")

if "page_link" not in st.session_state:
    st.switch_page("pages/home.py")