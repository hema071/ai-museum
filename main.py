import streamlit as st
import engine
import uuid
import database




def create():

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {}] # I gave the name messages


    if "mode" not in st.session_state:
        st.session_state.mode = "fast"

    if "username" not in st.session_state:
        st.session_state.username = ""

    if "started" not in st.session_state:
        st.session_state.started = False





    @st.dialog ("Before continuing...")
    def popup():
        st.title("Before continuing...")
        name = st.text_input("What should we call you?")
        mode = st.selectbox("Select your mode", ["Detailed", "Child", "Fast", "Default"])

        if st.button ("lets begin"):
            st.session_state.username = name
            st.session_state.mode = mode
            if st.session_state.mode == "Detailed":
                st.session_state.messages.append ({"role": "system", "content": "you are an intelligent museum guide and your mission is to explain to the user everything they ask about detailed."})
            elif st.session_state.mode == "Child":
                st.session_state.messages.append ({"role": "system", "content": "you are an intelligent museum guide and your mission is explaining everything your user asks about in a simple and fun way. Your user is a child and you need to explain to them in an entertaining, simple and easy way."})
            elif st.session_state.mode == "Fast":
                st.session_state.messages.append ({"role": "system", "content": "you are an intelligent museum guide and your mission is explaining everything your user asks about quickly and using only short messages. you must not skip any important details"})
            elif st.session_state.mode == "Default":
                st.session_state.messages.append ({"role": "system", "content": "you are an intelligent museum guide and your mission is explaining everything your user asks about in a normal way. not too long, not too short and you must not skip any important details"})

            st.session_state.messages.append ({"role": "system", "content": f"your user's name is {st.session_state.username}"})
            st.session_state.started = True
            st.rerun()

    if not st.session_state.started:
        popup()





    st.title("Museum AI")




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

    st.markdown(f"Save this link to get back to the chat later: https://mainpy-dn3dqs3bybdka5ibq52eam.streamlit.app/?id={st.query_params["id"]}")
    for one_message in st.session_state.messages[2:]:
        with st.chat_message(one_message["role"]):
            st.markdown(one_message["content"])



if __name__ == "__main__":
    create()