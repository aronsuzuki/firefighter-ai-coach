
import streamlit as st
from openai import OpenAI
from datetime import datetime
import os
import json

st.set_page_config(page_title="CCFD Mindset & Mental Health Coach", page_icon="🧠")

# --- Layout and Branding ---
col1, col2 = st.columns([1, 5])
with col1:
    st.image("CCFD_Patch1.PNG", width=80)
with col2:
    st.markdown("## 🚒 CCFD Mindset & Mental Health Coach")

st.markdown("<hr style='margin-top: 0'>", unsafe_allow_html=True)

st.markdown("High Performers prioritize their mental health. Use the box below to talk about what’s on your mind, or pick something from the mindset toolkit dropdown. You can also guide the tone to match how you want to be coached today.")

# --- Tone Selection (Below chat input) ---
if "selected_tone" not in st.session_state:
    st.session_state.selected_tone = "Conversational"

# --- Mindset Toolkit Selection ---
toolkit_options = {
    "Reset": {
        "🧘 Box Breathing": "Breathe in 4, hold 4, out 4, hold 4 — repeat 4 times.",
        "🧠 Reframe the Thought": "What would the strongest version of you say about this situation?",
        "🚿 Cold Reset": "Splash cold water on your face or take a brisk walk — snap the loop."
    },
    "Refocus": {
        "✅ Celebrate One Win": "Name one thing you did right today — no matter how small.",
        "🎯 Clarify the Mission": "What really matters right now? Who depends on you showing up?",
        "🛠 Control the Controllables": "Focus only on what’s within your influence — drop the rest."
    },
    "Reconnect": {
        "📞 Phone a Brother/Sister": "Call a trusted peer — even if just to vent for 90 seconds.",
        "🗣 Vent with a Goal": "Say what’s frustrating you, then identify what outcome you want.",
        "🧩 Micro-Gratitude": "What’s one thing or person you’re grateful for right now?"
    },
    "Role-Play": {
        "🔥 Crucial Conversation Simulator": "Let’s role-play a high-stakes, high-stress conversation. Start by telling me what happened or what’s on your mind.",
        "🎭 Speak Their Side": "Take 60 seconds to explain what the other person might be thinking or feeling.",
        "🧍 Speak Your Truth": "Now speak your truth with clarity and respect. What do you really need to say?"
    }
}

# Flatten for dropdown
flat_toolkit = [""]  # Default empty option
tool_lookup = {}
for category, tools in toolkit_options.items():
    for label, content in tools.items():
        full_label = f"{category} – {label}"
        flat_toolkit.append(full_label)
        tool_lookup[full_label] = content

selected_tool = st.selectbox("🧰 Mindset Toolkit", flat_toolkit)

if selected_tool:
    st.info(tool_lookup[selected_tool])

# --- Chat Initialization ---
tone_prompts = {
    "Conversational": "Speak casually and supportively, like a trusted peer at the station.",
    "Calm & Clinical": "Maintain a grounded, clinical tone — clear, calm, and supportive.",
    "Tough Love": "Be direct, challenge the user respectfully, and inspire accountability and growth."
}

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "system",
            "content": (
                "You are an AI mindset and mental health coach for firefighters. "
                "You speak like a trusted, seasoned peer — clear, grounded, culturally aware. "
                "Use plain language. Avoid therapy buzzwords. Reference firehouse culture and values. "
                f"{tone_prompts[st.session_state.selected_tone]} "
                "Offer mindset tools and encouragement. When distress is high, recommend breathwork, reframing, or calling a peer. "
                "Always prioritize emotional resilience, mental clarity, and personal accountability."
            )
        }
    ]

# --- Chat Logic ---
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

        # Add follow-up prompt if not present
        if not reply.strip().endswith("?"):
            reply += "

What else is on your mind?"

        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").markdown(reply)

    # Log usage
    os.makedirs("logs", exist_ok=True)
    log_data = {
        "timestamp": str(datetime.now()),
        "tone": st.session_state.selected_tone,
        "tool": selected_tool,
        "input": user_input,
        "output": reply
    }
    with open(f"logs/{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
        json.dump(log_data, f)

# --- Display Chat History (Excluding system message) ---
st.markdown("---")
for msg in st.session_state.chat_history[1:]:
    st.chat_message(msg["role"]).markdown(msg["content"])

# --- Tone Selector (Below chat display) ---
st.session_state.selected_tone = st.selectbox("🎙 Coaching Tone", list(tone_prompts.keys()), index=list(tone_prompts.keys()).index(st.session_state.selected_tone))

# --- Disclaimer ---
st.markdown("---")
st.caption("🚧 This is a demonstration version of the CCFD Mindset & Mental Health Coach. It is a work in progress and not a substitute for professional clinical support.")
