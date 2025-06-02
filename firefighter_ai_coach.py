
import streamlit as st
from openai import OpenAI
from datetime import datetime
import os
import json

st.set_page_config(page_title="CCFD Mindset & Mental Health Coach", page_icon="🧠")

# Branding: logo and header in two columns
col1, col2 = st.columns([1, 4])
with col1:
    st.image("CCFD_Patch1.PNG", width=80)
with col2:
    st.title("🚒 CCFD Mindset & Mental Health Coach")
st.markdown("---")

# Instructions
st.markdown("You’re in control here. This chat doesn’t report anything or judge you.")
st.markdown("Use the box below to talk about what’s on your mind, or pick something from the mindset toolkit. You can also guide the tone to match how you want to be coached today.")

# Initialize tone prompt and selector
tone_prompts = {
    "Conversational": "Speak casually and supportively, like a trusted peer at the station.",
    "Calm & Clinical": "Maintain a grounded, clinical tone — clear, calm, and supportive.",
    "Tough Love": "Be direct, challenge the user respectfully, and inspire accountability and growth."
}
if "tone" not in st.session_state:
    st.session_state.tone = "Conversational"
tone = st.selectbox("Select your preferred coaching tone:", list(tone_prompts.keys()), index=list(tone_prompts.keys()).index(st.session_state.tone))
st.session_state.tone = tone

# Mindset Toolkit (Nested Categories)
tool_options = {
    "Reset": {
        "🧘 Just Breathe": "Try box breathing: Inhale 4, hold 4, exhale 4, hold 4. Repeat for 4 rounds.",
        "🧠 Clear a Mental Loop": "Ask: What's one thing I need to let go of to move forward today?",
        "🧹 Ground + Move On": "Feel your feet. Look around. Label 5 things you can see. Then ask: What's my next move?"
    },
    "Refocus": {
        "🎯 One Win Today": "What’s one thing you handled well today, no matter how small?",
        "🔍 What’s in My Control?": "List what you can control. Let go of the rest.",
        "📣 Reframe the Story": "If you told the strongest version of you how this went down, what would you say?"
    },
    "Re-engage": {
        "🎤 Role-Play a Crucial Conversation": "Imagine you're about to address a high-stakes situation. What needs to be said? What matters most?",
        "🤝 Repair + Rebuild": "What part do you own in that tension? What would 'stepping up' look like here?",
        "🧭 Decide + Commit": "What’s one decision you’ve been avoiding? What’s the cost of not acting?"
    }
}
tool_categories = list(tool_options.keys())
tool_selection = st.selectbox("🧰 Mindset Toolkit", [""] + [f"{cat} - {tool}" for cat in tool_categories for tool in tool_options[cat]])

# Display selected tool info
if tool_selection and " - " in tool_selection:
    cat, tool = tool_selection.split(" - ", 1)
    st.info(tool_options[cat][tool])

# Session state setup
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# System prompt
system_prompt = (
    f"You are an AI mindset and mental health coach for firefighters. "
    f"You speak like a trusted, seasoned peer — clear, grounded, gritty, and culturally fluent. "
    f"Use plain, direct language. Skip therapy jargon. Speak to the realities of the job — firehouse culture, shift work fatigue, and critical incident stress. "
    f"{tone_prompts[tone]} "
    f"Give perspective, encouragement, and practical tools. When someone is overwhelmed, recommend breathwork, grounding techniques, or a quick mindset tool. "
    f"Always coach toward emotional strength, clarity under pressure, and personal accountability. "
    f"Remind firefighters that adversity builds toughness. Hard calls, conflict, and failure are reps for mental growth and increased grit. "
    f"End each response with a related follow-up question to keep the conversation going."
)
st.session_state.chat_history = [{"role": "system", "content": system_prompt}] + st.session_state.chat_history

# Chat input
user_input = st.chat_input("How you doin? What’s on your mind?")
if user_input:
    st.chat_message("user").markdown(user_input)
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

    # Log the exchange
    os.makedirs("logs", exist_ok=True)
    with open(f"logs/{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
        json.dump({
            "timestamp": str(datetime.now()),
            "tone": tone,
            "tool": tool_selection,
            "input": user_input,
            "output": reply
        }, f)

# Display prior conversation
for msg in st.session_state.chat_history[1:]:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").markdown(msg["content"])

# Footer disclaimer
st.markdown("---")
st.caption("🚧 This is a demonstration version of the CCFD Mindset & Mental Health Coach. It is a work in progress and not a substitute for professional clinical support.")
