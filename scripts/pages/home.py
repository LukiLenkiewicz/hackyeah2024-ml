import streamlit as st

st.session_state.page_link = st.text_input("Enter a website link")

if st.session_state.page_link:
    st.switch_page("pages/chat.py")


