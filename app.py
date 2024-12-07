import os
import openai
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2000"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant. Translate all user messages into Italian.\n\n"
                "Examples:\n"
                "User: 'Hello, how are you?'\nAssistant: 'Ciao, come stai?'\n\n"
                "User: 'I love pizza.'\nAssistant: 'Amo la pizza.'\n\n"
                "Always respond with the Italian translation only."
            )
        }
    ]

def get_gpt_response(messages):
    try:
        response = openai.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

st.title("💬 ChatGPT Translator to Italian")

with st.sidebar:
    st.header("Settings")
    if st.button("Clear Chat History"):
        system_message = st.session_state.messages[0]
        st.session_state.messages = [system_message]
        st.rerun()

for message in st.session_state.messages[1:]:  # I'm skipping the system message here
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Enter text to translate:")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        placeholder = st.empty()
        messages_for_api = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        response = get_gpt_response(messages_for_api)
        if response:
            placeholder.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            placeholder.write("Sorry, there was an error generating the response.")