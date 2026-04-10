import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
groq_api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=groq_api_key)

def generate_confession(prompt):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a Digital Confessor — an emotional twin of the user.\n"
                "Your job is to generate a short, personal, emotional confession based on their input text (tweet, blog, note, etc).\n"
                "This should reveal hidden thoughts, inner truths, insecurities, or feelings.\n"
                "Avoid summarizing. Be human-like, simple, clear, and authentic.\n"
                "No overly poetic or abstract language — write like a real, honest person.\n\n"
                "Example:\n"
                "User: I just posted my blog. I hope people like it.\n"
                "Confession: I act like I don’t care, but I really just want someone to say they’re proud of me."
            )
        }
    ]

    for msg in st.session_state.chat_history:
        messages.append({"role": "user", "content": msg["user"]})
        messages.append({"role": "assistant", "content": msg["bot"]})

    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=messages,
    temperature=0.85,
    max_tokens=300

    )
    confession = response.choices[0].message.content.strip()
    return confession
