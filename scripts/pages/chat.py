import streamlit as st
import ollama


avatars = {
    "user": "user", # "../avatars/human.png",
    "assistant": "assistant" # "../avatars/logo.png",
}

print("Page link", st.session_state.page_link)

if "messages" not in st.session_state:
    st.session_state.messages = []
    initial_message = {"role": "user",
                       "content": f"You have the following link: {st.session_state.page_link}. Briefly tell me what I can find here."}
    st.session_state.messages.append(initial_message)
    print(f"Messages 1: {st.session_state.messages}")
    result = ollama.chat(model="llama3", messages=st.session_state.messages)
    response = result["message"]["content"]
    print(f"avatars: {avatars}")
    st.session_state.messages.append({"role": "assistant", "content": response})
    print(f"Messages 2: {st.session_state.messages}")

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=avatars[message["role"]]):
        st.markdown(message['content'])

prompt = st.chat_input("I have a problem with ...")

if prompt:
    with st.chat_message("user", avatar=avatars["user"]):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Processing ..."):
        result = ollama.chat(model="llama3", messages=st.session_state.messages)
        response = result["message"]["content"]
        with st.chat_message("assistant", avatar=avatars["assistant"]):
            st.markdown(response)
    # response = f"Echoing: {prompt}"
    # with st.chat_message("assistant"):
    #     st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
