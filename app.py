import streamlit as st
from core import generate_confession

# Setup
st.set_page_config(page_title="Digital Twin Confessor", layout="centered")

import base64

def set_bg_from_local(image_path):
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
    """, unsafe_allow_html=True)

# Call the function with your image path
set_bg_from_local("download.jpg")


# Load custom CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Hide Streamlit menu/footer
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Session state init
if "page" not in st.session_state:
    st.session_state.page = "intro"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def go_to_chat():
    st.session_state.page = "chat"

# -------------------- Page 1: Intro --------------------
if st.session_state.page == "intro":
    st.markdown("<div class='big-title'>Digital Twin Confessor</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-text'>Let your digital self confess what your real self hides. Dive into an emotional reflection experience powered by AI.</div>", unsafe_allow_html=True)

    # Centered button using columns
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    with col3:
        if st.button("Get Started", key="start-btn"):
            go_to_chat()

# -------------------- Page 2: Chat Page --------------------
# -------------------- Page 2: Chat Page --------------------
elif st.session_state.page == "chat":
    st.title("💬 Talk to Your Digital Twin 🚀")

    # Show entire chat history
    if st.session_state.chat_history:
        for chat in st.session_state.chat_history:
            st.markdown(
                f"<div class='chat-bubble user'><b>You:</b> {chat['user']}</div>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<div class='chat-bubble bot'><b>Twin:</b> {chat['bot']}</div>",
                unsafe_allow_html=True
            )

    # Input field always available below messages
    user_input = st.text_input("What's on your mind?", key="user_input")

    if st.button("Send", key="send-btn") and user_input.strip() != "":
        with st.spinner("Your twin is thinking..."):
            try:
                bot_reply = generate_confession(user_input)
                if bot_reply:
                    st.session_state.chat_history.append({"user": user_input, "bot": bot_reply})
                    st.rerun()  # Refresh to show new messages
                else:
                    st.warning("Sorry, I couldn't generate a reply.")
            except Exception as e:
                st.error(f"Something went wrong: {e}")
