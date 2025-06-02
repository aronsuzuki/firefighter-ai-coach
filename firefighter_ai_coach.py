
import streamlit as st
from openai import OpenAI
from datetime import datetime
import os
import json

st.set_page_config(page_title="CCFD Mindset & Mental Health Coach", page_icon="🧠")

# Header and layout
col1, col2 = st.columns([1, 5])
with col1:
    st.image("CCFD_Patch1.PNG", width=90)
with col2:
    st.markdown("## CCFD Mindset & Mental Health Coach")
st.markdown("---")
st.markdown("You’re in control here. This chat doesn’t report anything or judge you.")

# Mindset Toolkit (last approved version)
toolkit_options = {
    "Reset Your Mindset": [
        "Box Breathing (4-4-4-4)",
        "Reframe the Moment",
        "Pause & Reset"
    ],
    "Build Resilience": [
        "One Win Today",
        "Next 3 Hours Plan",
        "Name Your Strength"
    ],
    "Navigate Tough Conversations": [
        "Crucial Conversation Role-Play",
        "Own Your Part",
        "What They Might Be Feeling"
    ]
}

selected_tool_category = st.selectbox("🧰 Mindset Toolkit", [""] + list(toolkit_options.keys()))
selected_tool = None
if selected_tool_category:
    selected_tool = st.selectbox("Select a Tool", [""] + toolkit_options[selected_tool_category])

# Tone selector
tone = st.selectbox("Preferred Tone:", ["Conversational", "Calm & Clinical", "Tough Love"])
tone_prompts = {
    "Conversational": "Speak casually and supportively, like a trusted peer at the station.",
    "Calm & Clinical": "Maintain a grounded, clinical tone — clear, calm, and supportive.",
    "Tough Love": "Be direct, challenge the user respectfully, and inspire accountability and growth."
}

# Keyword to follow-up mapping
keyword_prompt_map = {
    "stress": "Want to try a quick breathing exercise to reset?",
    "fatigue": "Rest’s important. Do you think this is physical, emotional, or both?",
    "burned out": "Do you feel like your tank is running low lately?",
    "anger": "Have you figured out what’s underneath the anger?",
    "anxious": "Want to slow things down for a second? I can guide you through it.",
    "drinking": "Would talking to someone like a sponsor or visiting a meeting help?",
    "gambling": "Is this something you feel is starting to take control?",
    "drugs": "Are you feeling like it's harder to stop lately?",
    "family": "What’s been the hardest part about the family situation?",
    "wife": "Want to talk about what happened with her?",
    "husband": "Want to talk about what happened with him?",
    "divorce": "That’s never easy. Want to get into it?",
    "conflict": "Is this something you’ve talked out with them yet?",
    "shift": "Is this something that’s tied to the last shift or been building up?",
    "trauma": "Is this something that stuck with you after a call?",
    "call": "Want to unpack what happened on that call?",
    "mistake": "What would the most accountable version of you say about it?",
    "overwhelmed": "Would a quick mindset tool help lighten the mental load?",
    "sponsor": "When’s the last time you checked in with them?",
    "rehab": "Are you considering going back, or just trying to stay steady?",
}

# System prompt
tone_prompt = tone_prompts[tone]
system_prompt = (
    f"You are an AI mindset and mental health coach for firefighters. "
    f"You speak like a trusted, seasoned peer — clear, grounded, gritty, and culturally fluent. "
    f"Use plain, direct language. Skip therapy jargon. Speak to the realities of the job — firehouse culture, shift work fatigue, and critical incident stress. "
    f"{tone_prompt} "
    f"Give perspective, encouragement, and practical tools. When someone is overwhelmed, recommend breathwork, grounding techniques, or a quick mindset tool. "
    f"Always coach toward emotional strength, clarity under pressure, and personal accountability. "
    f"Remind firefighters that adversity builds toughness. Hard calls, conflict, and failure are reps for mental growth and increased grit."
)

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "system", "content": system_prompt}]

# Chat input
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
        reply = response.choices[0].message.content.strip()

        # Check for keyword-based follow-up
        lower_input = user_input.lower()
        follow_up = None
        for keyword, prompt in keyword_prompt_map.items():
            if keyword in lower_input:
                follow_up = prompt
                break

        if follow_up:
            reply += f"

{follow_up}"
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").markdown(reply)

# Line separator
st.markdown("---")

# Display chat messages
for msg in st.session_state.chat_history[1:]:
    role = msg["role"]
    content = msg["content"]
    st.chat_message(role).markdown(content)

# Disclaimer
st.markdown("---")
st.caption("🚧 This is a demonstration version of the CCFD Mindset & Mental Health Coach. It is a work in progress and not a substitute for professional clinical support.")
