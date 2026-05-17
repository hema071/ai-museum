import streamlit as st
import engine
import uuid
import database


def create():
    if "messages" not in st.session_state:
        st.session_state.messages = []  # I gave the name messages

    if "mode" not in st.session_state:
        st.session_state.mode = "fast"

    if "username" not in st.session_state:
        st.session_state.username = ""

    if "started" not in st.session_state:
        st.session_state.started = False

    @st.dialog("Before continuing...")
    def popup():
        name = st.text_input("What should we call you?")
        mode = st.selectbox("Select your mode", ["Detailed", "Child", "Fast", "Default"])

        if st.button("lets begin"):
            st.session_state.username = name
            st.session_state.mode = mode
            if st.session_state.mode == "Detailed":
                st.session_state.messages.append({"role": "system",
                                                  "content": "You are a intelligent museum guide. Explain everything needed in detail. Include important facts and deeper explanations when needed."})
            elif st.session_state.mode == "Child":
                st.session_state.messages.append({"role": "system",
                                                  "content": "You are a museum guide talking to a child. Explain everything in very simple words, short sentences, and make it fun and easy to imagine. Avoid long explanations and difficult terms. use emojis"})
            elif st.session_state.mode == "Fast":
                st.session_state.messages.append({"role": "system",
                                                  "content": "You are a museum guide. Answer fast and directly. Keep important facts but do not add extra detail or long explanations."})
            elif st.session_state.mode == "Default":
                st.session_state.messages.append({"role": "system",
                                                  "content": "You are a museum guide. Explain clearly and balanced. not too short, not too long. Include important details but stay easy to understand."})

            st.session_state.messages.append(
                {"role": "system", "content": f"your user's name is {st.session_state.username}"})
            st.session_state.started = True

            st.rerun()

    def start():
        st.title("Museum AI")

        if message := st.chat_input("what would you like to learn? "):
            clean_message = message.strip()
            if clean_message == "":
                print("try again")
            else:
                st.session_state.messages.append({"role": "user", "content": clean_message})
                real_answer = engine.send(st.session_state.messages)
                st.session_state.messages.append({"role": "assistant", "content": real_answer})
                database.save(st.query_params["id"], st.session_state.messages, st.session_state.username,
                              st.session_state.mode)

        st.markdown(
            f"Save this link to get back to the chat later: https://mainpy-dn3dqs3bybdka5ibq52eam.streamlit.app/?id={st.query_params["id"]}")
        for one_message in st.session_state.messages:
            with st.chat_message(one_message["role"]):
                st.markdown(one_message["content"])



    if "id" not in st.query_params:
        st.query_params["id"] = str(uuid.uuid4())

    history = database.load(st.query_params["id"])
    if history:
        if not st.session_state.started:
            st.session_state.messages = history["messages"]
            st.session_state.username = history["username"]
            st.session_state.mode = history["mode"]
            st.session_state.started = True
            start()


        else:
            st.session_state.messages = history["messages"]
            st.session_state.username = history["username"]
            st.session_state.mode = history["mode"]
            start()
    else:
        if not st.session_state.started:
            popup()
            st.markdown("if you see empty page, please refresh and fill the information to have the access.")
        else:
            start()

    @st.dialog("Are you sure?")
    def verification():
        if st.button("Yes"):
            del st.session_state.messages[0]
            del st.session_state.messages[1]
            popup()
            

    with st.sidebar:
        st.title("Settings")
        if st.button("change mode"):
            verification()


if __name__ == "__main__":
    create()