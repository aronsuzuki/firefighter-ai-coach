
import streamlit as st
from openai import OpenAI
from datetime import datetime
import os
import json

st.set_page_config(page_title="CCFD Mindset & Mental Health Coach", page_icon="🧠")

# Branding
st.image("CCFD_Patch1.PNG", width=100)
st.title("🚒 CCFD Mindset & Mental Health Coach")
st.caption("Responding with Integrity • Serving with Compassion")
st.markdown("**Pride, Passion & Professionalism**")

# Tone selector
tone = st.selectbox("Select your preferred coaching tone:", ["Conversational", "Calm & Clinical", "Tough Love"])
tone_prompts = {
    "Conversational": "Speak casually and supportively, like a trusted peer at the station.",
    "Calm & Clinical": "Maintain a grounded, clinical tone — clear, calm, and supportive.",
    "Tough Love": "Be direct, challenge the user respectfully, and inspire accountability and growth."
}

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": f"You are an AI mindset and mental health coach for firefighters. You have received training on the IAFF Peer Support. You understand the value of self-care and viewing challenges with a growth-mindset. You draw examples from stoicism.  {tone_prompts[tone]}"}
    ]

# Micro-Coaching Modules
st.markdown("### 🧰 Quick Coaching Tool")
selected_tool = st.selectbox("Choose a tool to help right now:", [
    "None",
    "🧘 Breath + Reframe",
    "✅ Celebrate One Win",
    "🧠 Clear Mind After Miscommunication"
])

if selected_tool == "🧘 Breath + Reframe":
    st.info("Box breathe: Inhale 4, hold 4, exhale 4, hold 4. Then reframe: *What would the strongest version of you say about this moment?*")
elif selected_tool == "✅ Celebrate One Win":
    st.info("What’s one thing you got right today — even if it’s small?")
elif selected_tool == "🧠 Clear Mind After Miscommunication":
    st.info("Reflect: What emotion are you holding? Who benefits if you let it go? Say: *I didn’t know then what I know now. I’ll do better next time.*")

# User input
user_input = st.chat_input("How you doin? What’s on your mind?")
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.spinner("Coach is thinking..."):
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.chat_history,
            temperature=0.7
        )
        reply = response.choices[0].message.content
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").markdown(reply)

    # Log usage
    os.makedirs("logs", exist_ok=True)
    log_data = {
        "timestamp": str(datetime.now()),
        "tone": tone,
        "tool": selected_tool,
        "input": user_input,
        "output": reply
    }
    with open(f"logs/{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
        json.dump(log_data, f)

# Display conversation
for msg in st.session_state.chat_history[1:]:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").markdown(msg["content"])

# Footer disclaimer
st.markdown("---")
st.caption("🚧 This is a demonstration version of the CCFD Mindset & Mental Health Coach. It is a work in progress and not a substitute for professional clinical support.")
