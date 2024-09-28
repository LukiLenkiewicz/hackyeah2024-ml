import streamlit as st
# import ollama

# from scripts folder run the command below
# streamlit run app.py

st.title("EasyTalk")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("I have a problem with ...")
if prompt:

    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # result = ollama.chat(model="llama3", messages=st.session_state.messages)
    # response = result["message"]["content"]
    # with st.chat_message("assistant"):
    #     st.markdown(response)
    response = f"Echoing: {prompt}"
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})




