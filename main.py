from openai import OpenAI
import streamlit as st

# i created my website

st.title("Museum AI")

# i connected the car engine
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=st.secrets["MY_OPENROUTER_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "you are an assistant that answers in short messages and not long ones"}]

    # i created the text box and the sending system

if message := st.chat_input("what would you like to learn? "):
    clean_message = message.strip()
    if clean_message == "":
        print("try again")

        # i created the sending to engine system

    else:
        st.session_state.messages.append({"role": "user", "content": clean_message})  # i saved my message as myself
        answer = client.chat.completions.create(model="openai/gpt-4o-mini",
                                                messages=st.session_state.messages[-10:])
        answer = answer.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": answer})

            # i prevented the disappearance

    for one_message in st.session_state.messages[1:]:
       with st.chat_message(one_message["role"]):
         st.markdown(one_message["content"])





