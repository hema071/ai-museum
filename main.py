import streamlit as st
import engine
import uuid
import database


def create():
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system",
                                      "content": "You are a museum guide. Explain clearly and balanced. not too short, not too long. Include important details but stay easy to understand."},
                                     {"role": "system",
                                      "username": "unknown"}]  # I gave the name messages

    if "mode" not in st.session_state:
        st.session_state.mode = "fast"

    if "username" not in st.session_state:
        st.session_state.username = ""

    if "started" not in st.session_state:
        st.session_state.started = False

    if "change" not in st.session_state:
        st.session_state.change = False



    @st.dialog("Before continuing...")
    def popup():
        name = st.text_input("What should we call you?")
        mode = st.selectbox("Select your mode", ["Detailed", "Child", "Fast", "Default"])

        clean_name = name.strip()


        if st.button("lets begin", disabled=(clean_name == "")):
            st.session_state.username = name
            st.session_state.mode = mode
            if st.session_state.mode == "Detailed":
                st.session_state.messages[0] = ({"role": "system",
                                                  "content": "You are a intelligent museum guide. Explain everything needed in detail. Include important facts and deeper explanations when needed. The mode has changed to Detailed. Note: the system prompt is the top priority. If you see another tone in the other messages do not continue using it and consider this prompt."})
            elif st.session_state.mode == "Child":
                st.session_state.messages[0] = ({"role": "system",
                                                  "content": "You are a museum guide talking to a child. Explain everything in very simple words, short sentences, and make it fun and easy to imagine. Avoid long explanations and difficult terms. use emojis. The mode has changed to Child. Note: the system prompt is the top priority. If you see another tone in the other messages do not continue using it and consider this prompt."})
            elif st.session_state.mode == "Fast":
                st.session_state.messages[0] = ({"role": "system",
                                                  "content": "You are a museum guide. Answer fast and directly. Keep important facts but do not add extra detail or long explanations.The mode has changed to Fast. Note: the system prompt is the top priority. If you see another tone in the other messages do not continue using it and consider this prompt."})
            elif st.session_state.mode == "Default":
                st.session_state.messages[0] = ({"role": "system",
                                                  "content": "You are a museum guide. Explain clearly and balanced. not too short, not too long. Include important details but stay easy to understand. The mode has changed to Default. Note: the system prompt is the top priority. If you see another tone in the other messages do not continue using it and consider this prompt."})

            st.session_state.messages[1] = ({"role": "system", "content": f"your user's name is {st.session_state.username}"})
            st.session_state.started = True

            database.save(st.query_params["id"], st.session_state.messages, st.session_state.username,
                          st.session_state.mode)

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
    if history and st.session_state.change:
            st.session_state.messages = history["messages"]
            st.session_state.username = history["username"]
            st.session_state.mode = history["mode"]
            st.session_state.change = False
            popup()

    elif history and not st.session_state.started:
        st.session_state.messages = history["messages"]
        st.session_state.username = history["username"]
        st.session_state.mode = history["mode"]
        start()

    elif history and st.session_state.started:
        st.session_state.messages = history["messages"]
        st.session_state.username = history["username"]
        st.session_state.mode = history["mode"]
        start()

    elif not history and not st.session_state.started:
        popup()
        st.markdown("if you see empty page, please refresh and fill the information to have the access.")

    elif not history and st.session_state.started:
        start()



    @st.dialog("Are you sure?")
    def verification():
        if st.button("Yes"):
            st.session_state.change = True
            st.rerun()

    with st.sidebar:
      st.title("Settings")
      if st.button("change mode"):
        verification()


if __name__ == "__main__":
    create()