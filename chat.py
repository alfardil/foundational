"""
Streamlit hosted webapp to tryout the functionality.
"""

import atexit
import subprocess
import time

import requests
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

from model.client import LocalLLM
from utils.build import ensure_backend_built

st.set_page_config(page_title="AppleIntelligence Chat", page_icon="🤖")
st.title("AppleIntelligence Chat")


@st.cache_resource
def start_process(binary_path):
    """
    Launches the Swift binary directly.
    """

    process = subprocess.Popen(
        [binary_path, "serve"],
        cwd="./foundational",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    API_URL = "http://localhost:8080/health"

    for i in range(20):
        try:
            requests.get(API_URL)
            print("\nServer is online!")
            break
        except requests.exceptions.ConnectionError:
            time.sleep(1)
    else:
        process.kill()
        raise RuntimeError("Server failed to respond after 20 seconds.")

    def cleanup():
        print("\nTerminating Swift Server...")
        process.terminate()
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()

    atexit.register(cleanup)
    return process


executable_path = ensure_backend_built()
if executable_path:
    try:
        with st.spinner("Waiting for Apple Intelligence to come online..."):
            start_process(executable_path)

    except RuntimeError as e:
        st.error(f"❌ {e}")
        st.stop()


# model
@st.cache_resource
def load_model():
    llm = LocalLLM()
    return llm.get_model()


try:
    model = load_model()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    role = "user" if isinstance(message, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(message.content)

if prompt := st.chat_input("What is your prompt?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append(HumanMessage(content=prompt))

    with st.chat_message("assistant"):

        def stream_generator():
            stream = model.stream(st.session_state.messages)  # context
            for chunk in stream:
                yield chunk.content

        response = st.write_stream(stream_generator())

    st.session_state.messages.append(AIMessage(content=response))
