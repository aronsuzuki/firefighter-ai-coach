import streamlit as st
from openai import OpenAI
from datetime import datetime
import os
import json

st.set_page_config(page_title="CCFD Mindset & Mental Health Coach", page_icon="🧠")

col1, col2 = st.columns([1, 6])
with col1:
    st.image("CCFD_Patch1.PNG", width=80)
with col2:
    st.markdown("## CCFD Mindset & Mental Health Coach")

st.markdown("---")

st.markdown("High Performers prioritize their mental health. Use the box below to talk about what’s on your mind, or pick something from the mindset toolkit. You can also guide the tone to match how you want to be coached today.")

toolkit_options = {
    "Reset": ["🧘 Breathwork", "🚿 Mental Rinse", "🧯Get Out of Your Head"],
    "Refocus": ["✅ Celebrate a Win", "🎯 What's in Your Control?", "🛠️ Shift Perspective"],
    "Rebuild": ["🧠 Clear Miscommunication", "❤️ Repair with Teammate", "💬 Roleplay a Crucial Conversation"]
}

flat_tool_list = [""] + [f"{cat} > {tool}" for cat, tools in toolkit_options.items() for tool in tools]
selected_tool = st.selectbox("🧰 Mindset Toolkit", flat_tool_list)

tool_texts = {
    "Reset > 🧘 Breathwork": "Try box breathing: Inhale 4, hold 4, exhale 4, hold 4 — repeat 3 times.",
    "Reset > 🚿 Mental Rinse": "Visualize stress washing off like water in the shower. Say: 'That call is done. I'm back here now.'",
    "Reset > 🧯Get Out of Your Head": "Shift your attention — name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste.",
    "Refocus > ✅ Celebrate a Win": "What's one thing you got right today, no matter how small?",
    "Refocus > 🎯 What's in Your Control?": "Name 3 things you *can* control right now — even if they’re small.",
    "Refocus > 🛠️ Shift Perspective": "Ask: How would the strongest version of me see this situation?",
    "Rebuild > 🧠 Clear Miscommunication": "Ask yourself: What emotion am I holding? Who benefits if I let it go?",
    "Rebuild > ❤️ Repair with Teammate": "A quick repair can go a long way. Try: 'That didn’t land right. Can we reset?'",
    "Rebuild > 💬 Roleplay a Crucial Conversation": "Visualize the hard talk. What needs to be said, and how would calm, clear you say it?"
}

if selected_tool in tool_texts:
    st.info(tool_texts[selected_tool])

tone = st.selectbox("Coaching Tone", ["Conversational", "Calm & Clinical", "Tough Love"])
tone_prompts = {
    "Conversational": "Speak casually and supportively, like a trusted peer at the station.",
    "Calm & Clinical": "Maintain a grounded, clinical tone — clear, calm, and supportive.",
    "Tough Love": "Be direct, challenge the user respectfully, and inspire accountability and growth."
}

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("How you doin? What’s on your mind?")
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    system_prompt = f"""
You are an AI mindset and mental health coach for firefighters.
You speak like a trusted, seasoned peer — clear, grounded, gritty, and culturally fluent.
Use plain, direct language. Skip therapy jargon. Speak to the realities of the job — firehouse culture, shift work fatigue, and critical incident stress.
{tone_prompt}
Give perspective, encouragement, and practical tools. When someone is overwhelmed, recommend breathwork, grounding techniques, or a quick mindset tool.
Always coach toward emotional strength, clarity under pressure, and personal accountability.
Remind firefighters that adversity builds toughness. Hard calls, conflict, and failure are reps for mental growth and increased grit.
""".replace("{tone_prompt}", tone_prompts[tone])
    with st.spinner("Coach is thinking..."):
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": system_prompt}] + st.session_state.chat_history,
            temperature=0.7
        )
        reply = response.choices[0].message.content.strip()
        st.session_state.chat_history.append({"role": "assistant", "content": reply})

for msg in st.session_state.chat_history:
    st.chat_message(msg["role"]).markdown(msg["content"])

st.markdown("---")
st.caption("🚧 This is a demonstration version of the CCFD Mindset & Mental Health Coach. It is a work in progress and not a substitute for professional clinical support.")
