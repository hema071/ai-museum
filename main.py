import streamlit as st
import engine

def create():
    st.title("Museum AI")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "you are an assistant that answers in short messages and not long ones"}]

    if message := st.chat_input("what would you like to learn? "):
        clean_message = message.strip()
        if clean_message == "":
            print("try again")
        else:
            real_answer = engine.send(clean_message)
            st.session_state.messages.append({"role": "assistant", "content": real_answer})

    for one_message in st.session_state.messages[1:]:
        with st.chat_message(one_message["role"]):
            st.markdown(one_message["content"])


if __name__ == "__main__":
    create()
