import streamlit as st
import engine
import uuid
import database




def create():
    st.title("Museum AI")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "you are an assistant that answers in short messages and not long ones"}]

        if "id" not in st.query_params:
            st.query_params["id"] = str(uuid.uuid4())
            st.rerun()
        else:
            history = database.load(st.query_params["id"])
            if history:
                st.session_state.messages = history



    if message := st.chat_input("what would you like to learn? "):
        clean_message = message.strip()
        if clean_message == "":
            print("try again")
        else:
            st.session_state.messages.append({"role": "user", "content": clean_message})
            real_answer = engine.send(st.session_state.messages)
            st.session_state.messages.append({"role": "assistant", "content": real_answer})
            database.save(st.query_params["id"], st.session_state.messages)


    for one_message in st.session_state.messages[1:]:
        with st.chat_message(one_message["role"]):
            st.markdown(f"Save this link to get back to the chat later: https://mainpy-dn3dqs3bybdka5ibq52eam.streamlit.app/?id={ st.query_params["id"]}")
            st.markdown(one_message["content"])



if __name__ == "__main__":
    create()