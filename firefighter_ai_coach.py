import streamlit as st
from openai import OpenAI
from datetime import datetime
import os
import json

st.set_page_config(page_title="CCFD Mindset & Mental Health Coach", page_icon="🧠")

# Header
col1, col2 = st.columns([1, 5])
with col1:
    st.image("CCFD_Patch1.PNG", width=100)
with col2:
    st.title("🚒 CCFD Mindset & Mental Health Coach")
st.markdown("---")
st.markdown("High Performers prioritize their mental health. Use the box below to talk about what’s on your mind, or pick something from the mindset toolkit dropdown. You can also guide the tone to match how you want to be coached today.")

# Tone selector
tone = st.selectbox("Select your preferred coaching tone:", ["Conversational", "Calm & Clinical", "Tough Love"])
tone_prompts = {
    "Conversational": "Speak casually and supportively, like a trusted peer at the station.",
    "Calm & Clinical": "Maintain a grounded, clinical tone — clear, calm, and supportive.",
    "Tough Love": "Be direct, challenge the user respectfully, and inspire accountability and growth."
}

# Mindset toolkit
toolkit = {
    "Reset": {
        "🧘 Breath + Reframe": "Box breathe: Inhale 4, hold 4, exhale 4, hold 4. Then reframe: *What would the strongest version of you say about this moment?*",
        "🌲 Step Outside": "Fresh air can reset your nervous system. Step away for 2 minutes.",
        "🛑 Name it to Tame it": "Label what you’re feeling out loud. Naming the emotion can reduce its power."
    },
    "Reframe": {
        "✅ Celebrate One Win": "What’s one thing you got right today — even if it’s small?",
        "📊 Progress over Perfection": "Focus on how far you’ve come, not how far you have to go.",
        "🛤️ Stay in Your Lane": "Let go of what’s outside your control. Refocus on your responsibilities."
    },
    "Reengage": {
        "📞 Phone a Teammate": "Connection beats isolation. Text or call a trusted teammate.",
        "📓 Write it Out": "Jot down what’s looping in your head. Writing helps clear your mind.",
        "🧠 Clear Mind After Miscommunication": "What emotion are you holding? Who benefits if you let it go? Say: *I didn’t know then what I know now. I’ll do better next time.*"
    },
    "Role-Play": {
        "🎭 Crucial Conversation": "Let’s practice a tough conversation. Who’s it with, and what’s the goal?"
    }
}

category = st.selectbox("Mindset Toolkit (Select a category):", [""] + list(toolkit.keys()))
tool_choice = ""
if category:
    tool_choice = st.selectbox("Choose a tool:", [""] + list(toolkit[category].keys()))
    if tool_choice:
        st.info(toolkit[category][tool_choice])

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input and AI response
user_input = st.chat_input("How you doin? What’s on your mind?")
if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Add a single system prompt dynamically only during the request
    system_prompt = {
        "role": "system",
        "content": f"You are an AI mindset and mental health coach for firefighters. {tone_prompts[tone]}"
    }

    with st.spinner("Coach is thinking..."):
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[system_prompt] + st.session_state.chat_history,
            temperature=0.7
        )
        reply = response.choices[0].message.content
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").markdown(reply)

    # Logging
    os.makedirs("logs", exist_ok=True)
    log_data = {
        "timestamp": str(datetime.now()),
        "tone": tone,
        "tool": tool_choice,
        "input": user_input,
        "output": reply
    }
    with open(f"logs/{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
        json.dump(log_data, f)

# Display history
st.markdown("---")
for msg in st.session_state.chat_history:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Disclaimer
st.caption("🚧 This is a demonstration version of the CCFD Mindset & Mental Health Coach. It is a work in progress and not a substitute for professional clinical support.")