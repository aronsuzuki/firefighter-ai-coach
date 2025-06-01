import streamlit as st
from openai import OpenAI
from datetime import datetime
import os
import json

st.set_page_config(page_title="CCFD Mindset & Mental Health Coach", page_icon="🧠")

# Layout: Logo and Title
col1, col2 = st.columns([1, 4])
with col1:
    st.image("CCFD_Patch1.PNG", width=80)
with col2:
    st.title("CCFD Mindset & Mental Health Coach")

st.markdown("---")

# Instructions
st.markdown("High Performers prioritize their mental health. Use the box below to talk about what’s on your mind, or pick something from the mindset toolkit. You can also guide the tone to match how you want to be coached today.")

# Initialize session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Tone selector below input
user_input = st.chat_input("How you doin'? What’s on your mind?")
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

tone = st.selectbox("Preferred tone:", ["Conversational", "Calm & Clinical", "Tough Love"], index=None, placeholder="Choose your coaching tone...")

tone_prompts = {
    "Conversational": "Speak casually and supportively, like a trusted peer at the station.",
    "Calm & Clinical": "Maintain a grounded, clinical tone — clear, calm, and supportive.",
    "Tough Love": "Be direct, challenge the user respectfully, and inspire accountability and growth."
}

# Only proceed if tone is selected
if tone:
    base_prompt = (
        "You are an AI mindset and mental health coach for firefighters. "
        "You speak like a trusted, seasoned peer — clear, grounded, culturally aware. "
        "Use plain language. Avoid therapy buzzwords. Reference firehouse culture when helpful. "
        f"{tone_prompts[tone]} "
        "Offer mindset tools and encouragement. When distress is high, recommend breathing or grounding. "
        "Always prioritize emotional resilience, mental clarity, and personal accountability."
    )

    if not any(msg["role"] == "system" for msg in st.session_state.chat_history):
        st.session_state.chat_history.insert(0, {"role": "system", "content": base_prompt})

    with st.spinner("Coach is thinking..."):
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.chat_history,
            temperature=0.7
        )
        reply = response.choices[0].message.content.strip()
        reply += "\n\nWant to keep going on this, or dive into a tool from the mindset kit?"
        st.session_state.chat_history.append({"role": "assistant", "content": reply})

# Display chat
st.markdown("---")
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Disclaimer at bottom
st.markdown("---")
st.caption("🚧 This is a demonstration version of the CCFD Mindset & Mental Health Coach. It is a work in progress and not a substitute for professional clinical support.")