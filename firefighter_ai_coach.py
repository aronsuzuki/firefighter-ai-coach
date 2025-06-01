
import streamlit as st
from openai import OpenAI
from datetime import datetime
import os
import json

st.set_page_config(page_title="CCFD Mindset & Mental Health Coach", page_icon="🧠")

# Branding section with side-by-side layout
col1, col2 = st.columns([1, 5])
with col1:
    st.image("CCFD_Patch1.PNG", width=80)
with col2:
    st.markdown("### 🚒 CCFD Mindset & Mental Health Coach")
    st.caption("Responding with Integrity • Serving with Compassion")
    st.markdown("**Pride, Passion & Professionalism**")

st.markdown("High Performers prioritize their mental health. Use the box below to talk about what’s on your mind, or pick something from the mindset toolkit dropdown. You can also guide the tone to match how you want to be coached today.")

# Tone selector (placed below input later)
tone_prompts = {
    "Conversational": "Speak casually and supportively, like a trusted peer at the station.",
    "Calm & Clinical": "Maintain a grounded, clinical tone — clear, calm, and supportive.",
    "Tough Love": "Be direct, challenge the user respectfully, and inspire accountability and growth."
}

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Micro-Coaching Toolkit
st.markdown("### 🧰 Mindset Toolkit")

toolkit_categories = {
    "Reset": {
        "🌬️ Just Breathe": "Take a moment to pause. Breathe in for 4, hold for 4, exhale for 4, hold for 4. Do this three times.",
        "✅ Celebrate One Win": "What’s one thing you got right today — even if it’s small?",
        "🧠 Clear Mind After Miscommunication": "What emotion are you holding? Who benefits if you let it go? Say: *I didn’t know then what I know now. I’ll do better next time.*"
    },
    "Refocus": {
        "🧭 Big Picture Check": "Zoom out. Will this matter in a week, a year, or ten years?",
        "🧱 Brick by Brick": "Progress happens one brick at a time. What’s the next small step?",
        "🧑‍🚒 Firefighter Mental Reboot": "You’ve reset after harder calls. Use the same skill now: decompress, debrief (even silently), and redirect your energy."
    },
    "Role Play": {
        "🗣️ Practice a Tough Talk": "Describe the high-stakes convo you’re facing. I’ll play the other person so you can test your words.",
        "🚨 Responding to a Heated Call": "Let’s walk through a recent high-stress call. How would you de-escalate it now?",
        "🧑‍🤝‍🧑 Supporting a Struggling Crewmember": "Role-play checking in with someone showing signs of burnout or personal struggle."
    }
}

selected_category = st.selectbox("Pick a toolkit category:", list(toolkit_categories.keys()))
selected_tool = st.selectbox("Choose a tool to use right now:", list(toolkit_categories[selected_category].keys()))

if selected_tool:
    st.info(toolkit_categories[selected_category][selected_tool])

# User input
user_input = st.chat_input("How you doin? What’s on your mind?")
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.spinner("Coach is thinking..."):
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        system_prompt = (
            "You are an AI mindset and mental health coach for firefighters. "
            "You speak like a trusted, seasoned peer — clear, grounded, culturally aware. "
            "Use plain language. Avoid therapy buzzwords. Reference firehouse culture, tough calls, and team dynamics. "
            f"{tone_prompts[st.session_state.get('tone', 'Conversational')]} "
            "Offer mindset tools and encouragement. When distress is high, recommend simple next steps. "
            "Always prioritize emotional resilience, mental clarity, and personal accountability."
        )

        full_chat = [{"role": "system", "content": system_prompt}] + st.session_state.chat_history
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=full_chat,
            temperature=0.7
        )
        reply = response.choices[0].message.content
        st.session_state.chat_history.append({"role": "assistant", "content": reply})

        st.chat_message("assistant").markdown(reply)

        # Log usage
        os.makedirs("logs", exist_ok=True)
        log_data = {
            "timestamp": str(datetime.now()),
            "tone": st.session_state.get("tone", "Conversational"),
            "tool_category": selected_category,
            "tool": selected_tool,
            "input": user_input,
            "output": reply
        }
        with open(f"logs/{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
            json.dump(log_data, f)

# Display chat history
st.markdown("---")
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").markdown(msg["content"])

# Tone selection below chat input
st.selectbox("Select your preferred coaching tone:", list(tone_prompts.keys()), key="tone")

# Footer disclaimer
st.markdown("---")
st.caption("🚧 This is a demonstration version of the CCFD Mindset & Mental Health Coach. It is a work in progress and not a substitute for professional clinical support.")
