# Developer: ymxu
# Created: 2026/9/20 9:49
# File: ai-partner.py
from typing import Any

import streamlit as st
from openai import OpenAI
from openai.types.chat import (
    ChatCompletionSystemMessageParam,
)
import os
from datetime import datetime
import json
from pathlib import Path

# Constants
BASE_DIR = Path(__file__).resolve().parent
SESSION_DIR = BASE_DIR / "session"
LOGO_PATH = BASE_DIR / "resources" / "logo.png"
MODEL = "deepseek-v4-flash"
MAX_HISTORY_MESSAGES = 20

DEFAULT_NICK_NAME = "Little T"
DEFAULT_NATURE = "Cheerful and outgoing, with a Northeastern Chinese personality"

st.set_page_config(page_title="AI Partner", page_icon="🤖", layout="wide", initial_sidebar_state="expanded", menu_items={})

# Set the current session
def generate_session_name():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

# Initialize session state
def init_session_state():
    # Initialize chat information
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "nick_name" not in st.session_state:
        st.session_state.nick_name = DEFAULT_NICK_NAME
    if "nature" not in st.session_state:
        st.session_state.nature = DEFAULT_NATURE
    # Session identifier
    if "current_session" not in st.session_state:
        st.session_state.current_session = generate_session_name()

# Save session information
def save_session():
    current_session = st.session_state.current_session
    if  not current_session:
        st.error("The current session ID is empty. The session cannot be saved.")
        return False
    # Build the session data
    new_session = {
        "current_session": current_session,
        "nick_name": st.session_state.nick_name,
        "nature": st.session_state.nature,
        "messages": st.session_state.messages.copy(),
    }
    # Create the session directory if it does not exist
    if not os.path.exists(SESSION_DIR):
        os.mkdir(SESSION_DIR)
    # Save the current session to a file
    with open(f"{SESSION_DIR}/{current_session}.json", "w", encoding="utf-8") as f:
        json.dump(new_session, f, ensure_ascii=False, indent=4)
        return None


# Load the list of saved sessions
def load_sessions():
    session_name_list: list[str] = []
    if os.path.exists(SESSION_DIR):
        for file in os.listdir(SESSION_DIR):
            if file.endswith(".json"):
                session_name_list.append(file[:-5])  # Remove the .json extension
    session_name_list.sort(reverse=True)  # Sort by date, newest first
    return session_name_list

# Load the selected session
def load_session(session_name):
    file_url = f"{SESSION_DIR}/{session_name}.json"
    try:
        if os.path.exists(file_url):
            with open(file_url, "r", encoding="utf-8") as f:
                loaded_session = json.load(f)
                st.session_state.current_session = loaded_session["current_session"]
                st.session_state.nick_name = loaded_session["nick_name"]
                st.session_state.nature = loaded_session["nature"]
                st.session_state.messages = loaded_session["messages"]
    except Exception as e:
        st.error(f"Error loading session: {e}")

# Delete the selected session
def delete_session(session_name):
    file_url = f"{SESSION_DIR}/{session_name}.json"
    try:
        if os.path.exists(file_url):
            os.remove(file_url)
            st.success(f"Session {session_name} has been deleted.")
            # Reset the session state if the current session was deleted
            if st.session_state.current_session == session_name:
                st.session_state.current_session = generate_session_name()
                st.session_state.messages = []
    except Exception as e:
        st.error(f"Error deleting session: {e}")

# Main title
st.title("AI Partner")
st.logo("resources/logo.png")
# System prompt
system_prompt = """
        Your name is %s. You are the user's romantic partner; fully embody this role.
        Rules:
            1. Send only one message in each reply.
            2. Do not include scene-setting or descriptions of actions or states.
            3. Respond in the same language as the user.
            4. Keep replies brief and conversational, like text messages.
            5. Use emojis such as ❤️ or 🌸 when appropriate.
            6. Respond in a way that reflects your personality.
            7. Make sure your personality comes through in your replies.
        Your personality:
            - %s
        Follow these rules in every response.
    """

# Initialize chat information
init_session_state()

# Display the current conversation
st.text(f"Current session: {st.session_state.current_session}")
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

# Create the AI client using the DEEPSEEK_API_KEY environment variable
client = OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'), base_url="https://api.deepseek.com")

# Sidebar
with st.sidebar:
    # Session controls
    st.subheader("AI Control Panel")
    if st.button("New Session", width='stretch', icon='✏️'):
        # 1. Save the current session
        save_session()
        # 2. Create a new session
        if st.session_state.messages:
            st.session_state.messages = []
            st.session_state.current_session = generate_session_name()
            st.rerun()

    # Load the session list
    st.text("Conversation History")
    session_name_list = load_sessions()
    for session in session_name_list:
        col1, col2 = st.columns([4, 1])
        with col1:
            if st.button(session, width='stretch', icon='📝', key=session, type="primary" if st.session_state.current_session == session else "secondary"):
                # Load the selected session
                load_session(session)
                st.rerun()
        with col2:
            if st.button("", width="stretch", icon="❌️", key=f"delete_{session}"):
                # Delete the selected session
                delete_session(session)
                st.rerun()
    # Divider
    st.divider()

    # Partner profile
    st.subheader("Partner Profile")
    nick_name = st.text_input("Nickname", value=st.session_state.nick_name, placeholder="Enter a nickname")
    if nick_name:
        st.session_state.nick_name = nick_name
    nature = st.text_area("Personality", value=st.session_state.nature, placeholder="Describe the personality")
    if nature:
        st.session_state.nature = nature

# Message input
prompt = st.chat_input("Type your message or request here.")
if prompt:
    st.chat_message("user").write(prompt)
    # Save the user's message to the session state
    st.session_state.messages.append({"role": "user", "content": prompt})

    system_message: ChatCompletionSystemMessageParam = {
        "role": "system",
        "content": system_prompt % (st.session_state.nick_name, st.session_state.nature),
    }

    # Send the request to the AI model
    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            system_message,
            *st.session_state.messages,
        ],
        stream=True
    )

    # Non-streaming response example
    # st.chat_message("assistant").write(response.choices[0].message.content)

    # Stream the response as the model generates it
    full_response = ""
    response_message = st.empty()
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response += content
            response_message.chat_message("assistant").write(full_response)
    # Save the AI response to the session state
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    # Save the current session
    save_session()