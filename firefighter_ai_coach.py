
import streamlit as st
from openai import OpenAI
from datetime import datetime
import os
import json

st.set_page_config(page_title="CCFD Mindset & Mental Health Coach", page_icon="🧠")

# Branding
col1, col2 = st.columns([1, 4])
with col1:
    st.image("CCFD_Patch1.PNG", width=90)
with col2:
    st.markdown("## CCFD Mindset & Mental Health Coach")

st.markdown("---")
st.markdown("You’re in control here. This chat doesn’t report anything or judge you. Use the box below to talk about what’s on your mind, or pick something from the mindset toolkit dropdown. You can also guide the tone to match how you want to be coached today.")

# Tone selector (bottom of page, above disclaimer)
tone = st.selectbox("Preferred Coaching Tone:", ["Conversational", "Calm & Clinical", "Tough Love"])
tone_prompts = {
    "Conversational": "Speak casually and supportively, like a trusted peer at the station.",
    "Calm & Clinical": "Maintain a grounded, clinical tone — clear, calm, and supportive.",
    "Tough Love": "Be direct, challenge the user respectfully, and inspire accountability and growth."
}

# System prompt
system_prompt = (
    f"You are an AI mindset and mental health coach for firefighters. "
    f"You speak like a trusted, seasoned peer — clear, grounded, gritty, and culturally fluent. "
    f"Use plain, direct language. Skip therapy jargon. Speak to the realities of the job — firehouse culture, shift work fatigue, and critical incident stress. "
    f"{tone_prompts[tone]} "
    f"Give perspective, encouragement, and practical tools. When someone is overwhelmed, recommend breathwork, grounding techniques, or a quick mindset tool. "
    f"Always coach toward emotional strength, clarity under pressure, and personal accountability. "
    f"Remind firefighters that adversity builds toughness. Hard calls, conflict, and failure are reps for mental growth and increased grit."
)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": system_prompt}
    ]

# Mindset Toolkit Dropdown
toolkit_options = {
    "Reset": ["🧘 Controlled Breathing", "🧠 Reframe the Moment", "🧊 Cold Shift Reset"],
    "Refocus": ["✅ Celebrate One Win", "📋 Tactical Gratitude", "🔄 Control What You Can"],
    "Communicate": ["📣 Hard Talk Rehearsal", "🧭 Reconnect to Mission", "🧼 Clear the Residue"]
}
toolkit_menu = st.selectbox("🧰 Mindset Toolkit (Optional)", [""] + [f"{cat}: {tool}" for cat in toolkit_options for tool in toolkit_options[cat]])

# Micro-coaching display
if toolkit_menu and ":" in toolkit_menu:
    category, tool = toolkit_menu.split(": ", 1)
    tool_responses = {
        "🧘 Controlled Breathing": "Box breathe: Inhale 4, hold 4, exhale 4, hold 4. Repeat for 3 rounds.",
        "🧠 Reframe the Moment": "Ask yourself: What would the strongest version of me say about this situation?",
        "🧊 Cold Shift Reset": "Step outside, reset posture, take 3 breaths. Let the station noise fade for a moment.",
        "✅ Celebrate One Win": "What’s one thing you handled well today — no matter how small? Say it.",
        "📋 Tactical Gratitude": "Name one thing you’re grateful for in the last 24 hours. Tactical mindset reset.",
        "🔄 Control What You Can": "Identify what’s in your control right now. Act there.",
        "📣 Hard Talk Rehearsal": "Say it here first. Type what you *wish* you could say in that tough conversation.",
        "🧭 Reconnect to Mission": "Why did you take this job? What still matters about that today?",
        "🧼 Clear the Residue": "Say this aloud: 'That moment happened. I learned. It’s behind me.'"
    }
    st.info(tool_responses.get(tool.strip(), ""))

# Input field for user message
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
        st.session_state.chat_history.append({"role": "assistant", "content": reply})

    # Save interaction log
    os.makedirs("logs", exist_ok=True)
    log_data = {
        "timestamp": str(datetime.now()),
        "tone": tone,
        "tool": toolkit_menu,
        "input": user_input,
        "output": reply
    }
    with open(f"logs/{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
        json.dump(log_data, f)

# Display full conversation (skipping initial system message)
st.markdown("---")
for msg in st.session_state.chat_history[1:]:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Disclaimer footer
st.markdown("---")
st.caption("🚧 This is a demonstration version of the CCFD Mindset & Mental Health Coach. It is a work in progress and not a substitute for professional clinical support.")
