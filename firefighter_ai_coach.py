import streamlit as st
from openai import OpenAI
from datetime import datetime
import os
import json

st.set_page_config(page_title="CCFD Mindset & Mental Health Coach", page_icon="🧠")

# Branding
st.image("CCFD_Patch1.PNG", width=100)
st.title("🚒 CCFD Mindset & Mental Health Coach")

# Instructions
st.markdown("This is your space to check in. Use the box below to talk about what’s on your mind, or pick a quick tool from the dropdown if you need immediate support. You can also guide the tone to match how you want to be coached today.")

# Tone selector
# Initialize chat history
tone = st.selectbox("Select your preferred coaching tone:", ["Conversational", "Calm & Clinical", "Tough Love"])
tone_prompts = {
    "Conversational": "Speak casually and supportively, like a trusted peer at the station.",
    "Calm & Clinical": "Maintain a grounded, clinical tone — clear, calm, and supportive.",
    "Tough Love": "Be direct, challenge the user respectfully, and inspire accountability and growth."
}

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": f"You are an AI mindset and mental health coach for firefighters. {tone_prompts[tone]}"}
    ]

# Micro-Coaching Modules (Grouped by Theme)
st.markdown("### 🧰 Micro-Coaching Toolkit")
theme = st.selectbox("Select a category:", [
    "Reset & Reframe",
    "Build Confidence",
    "Process Conversations",
    "Future Focus"
])

tools_by_theme = {
    "Reset & Reframe": [
        "🧘 Breath + Reframe",
        "🔄 Mindful Reset",
        "🧠 Mental Gear Shift"
    ],
    "Build Confidence": [
        "✅ Celebrate One Win",
        "🔥 Recall a Moment of Pride"
    ],
    "Process Conversations": [
        "🧠 Clear Mind After Miscommunication",
        "🎭 Role-Play a Crucial Conversation"
    ],
    "Future Focus": [
        "🎯 What’s in My Control?",
        "📅 What Would Tomorrow-Me Want?"
    ]
}

tool = st.selectbox("Choose a tool:", tools_by_theme[theme])

tool_responses = {
    "🧘 Breath + Reframe": "Box breathe: Inhale 4, hold 4, exhale 4, hold 4. Then reframe: *What would the strongest version of you say about this moment?*",
    "✅ Celebrate One Win": "What’s one thing you got right today — even if it’s small?",
    "🧠 Clear Mind After Miscommunication": "Reflect: What emotion are you holding? Who benefits if you let it go? Say: *I didn’t know then what I know now. I’ll do better next time.*",
    "🔄 Mindful Reset": "Pause. Look at 5 things near you. Feel 4 things. Hear 3. Smell 2. Breathe 1.",
    "🧠 Mental Gear Shift": "Imagine flipping a switch. Say: *This next moment deserves my full focus.*",
    "🔥 Recall a Moment of Pride": "Think back to a time you were proud on the job. What did that version of you do right?",
    "🎭 Role-Play a Crucial Conversation": "Say your part aloud. Let the coach play the other person. Want to try it?",
    "🎯 What’s in My Control?": "Name one thing you can influence today. Focus on that.",
    "📅 What Would Tomorrow-Me Want?": "Imagine yourself tomorrow. What decision today makes their life easier?"
}

if tool in tool_responses:
    st.info(tool_responses[tool])

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

        # Append a follow-up prompt to continue the convo
        st.chat_message("assistant").markdown("_Need to go deeper on that or want a different perspective?_")

    # Log usage
    os.makedirs("logs", exist_ok=True)
    log_data = {
        "timestamp": str(datetime.now()),
        "tone": tone,
        "tool": tool,
        "input": user_input,
        "output": reply
    }
    with open(f"logs/{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
        json.dump(log_data, f)

# Display chat history
for msg in st.session_state.chat_history[1:]:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").markdown(msg["content"])

# Footer disclaimer
tone_prompts = {
    "Conversational": "Speak casually and supportively, like a trusted peer at the station.",
    "Calm & Clinical": "Maintain a grounded, clinical tone — clear, calm, and supportive.",
    "Tough Love": "Be direct, challenge the user respectfully, and inspire accountability and growth."
}
st.markdown("---")
st.caption("🚧 This is a demonstration version of the CCFD Mindset & Mental Health Coach. It is a work in progress and not a substitute for professional clinical support.")
