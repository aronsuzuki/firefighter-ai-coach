
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
st.markdown("**Values: Pride, Passion & Professionalism**")

# Tone selector
tone = st.selectbox("Select your preferred coaching tone:", ["Peer-like", "Calm Coach", "Direct Coach"])
tone_prompts = {
    "Peer-like": "Speak like a seasoned firefighter peer. Use casual, relatable language.",
    "Calm Coach": "Use a calm, reflective tone. Focus on emotional awareness and gentle redirection.",
    "Direct Coach": "Be direct and challenge the user to take ownership and reflect with accountability."
}

# Start chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": f"You are an AI mental health and mindset coach for firefighters. {tone_prompts[tone]}"}
    ]

# Micro-Coaching Modules
st.markdown("### 🧰 Need a quick reset?")
selected_tool = st.selectbox("Choose a mindset tool:", [
    "None",
    "🧘 60-second breath + reframe",
    "✅ One win from today",
    "🧠 Clear your mind after poor communication"
])

if selected_tool == "🧘 60-second breath + reframe":
    st.info("**Try this:** Breathe in 4 seconds, hold 4, out 4, hold 4 (Box Breathing). Then reframe: *What would the most resilient version of you say about this moment?*")
elif selected_tool == "✅ One win from today":
    st.info("**Try this:** What is one small thing you did right today? Say it out loud. No win is too small.")
elif selected_tool == "🧠 Clear your mind after poor communication":
    st.info("**Coach’s advice:** You can’t go back and redo that moment — but you *can* choose what story you carry forward. Ask yourself:\n- What did I learn?\n- What emotion am I holding onto?\n- Who does it serve if I let it go?\n\n**Close your eyes, exhale, and say:** *That version of me didn’t know what I know now. I can do better next time.*")

# User input
user_input = st.text_input("What's on your mind today?", key="user_input")
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.spinner("Coach is thinking..."):
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.chat_history,
            temperature=0.7
        )
        ai_reply = response.choices[0].message.content
        st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
        st.markdown("**🧠 Coach:** " + ai_reply)

    # Log usage
    log_data = {
        "timestamp": str(datetime.now()),
        "tone": tone,
        "tool_used": selected_tool,
        "input": user_input,
        "response": ai_reply
    }
    os.makedirs("logs", exist_ok=True)
    with open(f"logs/{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
        json.dump(log_data, f)

# Display full chat (scrollable)
if st.checkbox("Show full session transcript"):
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"**👤 You:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.markdown(f"**🧠 Coach:** {msg['content']}")
