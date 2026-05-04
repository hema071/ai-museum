from openai import OpenAI
import streamlit as st

def send(message_history):
    client = OpenAI(base_url="https://openrouter.ai/api/v1",
                    api_key=st.secrets["MY_OPENROUTER_KEY"])

    answer = client.chat.completions.create(model="openai/gpt-4o-mini",
                                            messages=message_history[-10:])
    answer = answer.choices[0].message.content
    return answer
