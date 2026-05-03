from openai import OpenAI
import streamlit as st
import sys

# the prepration and the engine


st.title ("Museum AI") # creates my website
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["MY_OPENROUTER_KEY"]
)


# i did a list called messages

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system",
           "content": "you are an assistant that answers in short messages and not long ones"}]



if message := st.chat_input("what would you like to learn? "):
    while True:
        if message == " ":
            print ("empty message")
        else:
            st.session_state.messages.append({"role": "user", "content": message})  # i saved my message as myself
            break

    answer = client.chat.completions.create(model="openai/gpt-4o-mini", messages=st.session_state.messages[-10:])
    answer = answer.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": answer})



for one_message in st.session_state.messages[1:]:
    with st.chat_message(one_message["role"]):
        st.markdown(one_message["content"])