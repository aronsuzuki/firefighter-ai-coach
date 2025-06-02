
import streamlit as st
from openai import OpenAI
from datetime import datetime
import os
import json

st.set_page_config(page_title="CCFD Mindset & Mental Health Coach", page_icon="🧠")

# Layout: Logo and Header in two columns
col1, col2 = st.columns([1, 6])
with col1:
    st.image("CCFD_Patch1.PNG", width=80)
with col2:
    st.markdown("## CCFD Mindset & Mental Health Coach")
st.markdown("---")
st.markdown("You’re in control here. This chat doesn’t report anything or judge you.")

# Define tone prompts
tone_prompts = {
    "Conversational": "Speak casually and supportively, like a trusted peer at the station.",
    "Calm & Clinical": "Maintain a grounded, clinical tone — clear, calm, and supportive.",
    "Tough Love": "Be direct, challenge the user respectfully, and inspire accountability and growth."
}

# Mindset Toolkit dropdown
toolkit_options = {
    "Reset": [
        "🧘 Breathwork Reset",
        "🧠 Clear After Miscommunication",
        "💭 Let It Go Visualization"
    ],
    "Refocus": [
        "🎯 Back to the Mission",
        "✅ One Win from Today",
        "🪬 What's in My Control?"
    ],
    "Relationships": [
        "❤️ Repair a Misstep",
        "🧍 When You’re Irritated",
        "👥 Hard Conversation Roleplay"
    ]
}

# Flatten toolkit menu for single select
toolkit_menu = [""]  # default blank
for category, tools in toolkit_options.items():
    for tool in tools:
        toolkit_menu.append(f"{category} — {tool}")

selected_tool = st.selectbox("🧰 Mindset Toolkit", toolkit_menu)

if selected_tool:
    if "Breathwork" in selected_tool:
        st.info("Box breathe: Inhale 4, hold 4, exhale 4, hold 4. Repeat 3 rounds.")
    elif "Clear After Miscommunication" in selected_tool:
        st.info("Ask: What emotion am I holding? Who benefits if I let it go? Say: *I’ll do better next time.*")
    elif "Let It Go" in selected_tool:
        st.info("Visualize releasing the weight. Say: *That’s not mine to carry anymore.*")
    elif "Back to the Mission" in selected_tool:
        st.info("Ask: What matters most right now? Anchor back to your role and values.")
    elif "One Win" in selected_tool:
        st.info("Name one thing you got right today — big or small.")
    elif "What’s in My Control" in selected_tool:
        st.info("Draw a circle. Inside: things you influence. Outside: what you release.")
    elif "Repair a Misstep" in selected_tool:
        st.info("Say: *That didn’t land how I wanted. Here’s what I meant.*")
    elif "When You’re Irritated" in selected_tool:
        st.info("Pause. Ask: *What story am I telling myself?* Reset before reacting.")
    elif "Hard Conversation Roleplay" in selected_tool:
        st.info("Type the situation. I’ll walk you through how to prepare and respond like a pro.")

st.markdown("---")

# Tone Selector (below input box, just above disclaimer)
tone = st.selectbox("Select your preferred coaching tone:", list(tone_prompts.keys()))

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Keyword-triggered follow-ups
keyword_followups = {
    "burnout": "You’re not weak — you’re human. What part of the job is draining you most right now?",
    "fatigue": "Shift fatigue is real. What’s your sleep or energy been like lately?",
    "anxious": "Your nervous system might be stuck in overdrive. Want to try a breathing reset?",
    "stressed": "Under pressure, we forget to reset. What’s one thing you can step back from?",
    "alcohol": "Are you using it to numb out or unwind? Be honest with yourself — no shame here.",
    "drinking": "What role is drinking playing in your recovery or stress cycle right now?",
    "drugs": "What’s been going on that made that seem like the best option?",
    "gambling": "Is the risk-taking about money — or something else? Let’s unpack that.",
    "family": "Family strain can compound firehouse stress. What’s weighing most heavily right now?",
    "wife": "What happened between you two that’s stuck in your mind?",
    "husband": "When did the disconnection start? What are you not saying?",
    "kids": "What kind of example do you want to set for them through this moment?",
    "partner": "What would healthy partnership look like for you right now?",
    "sponsor": "Have you checked in with your sponsor lately? They’ve probably been there too.",
    "rehab": "If part of you thinks you need help, you probably do. Let’s talk about next steps."
}

# User Input
user_input = st.chat_input("How you doin? What’s on your mind?")
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # System prompt with tone context
    system_prompt = (
        f"You are an AI mindset and mental health coach for firefighters. "
        f"You speak like a trusted, seasoned peer — clear, grounded, gritty, and culturally fluent. "
        f"Use plain, direct language. Skip therapy jargon. Speak to the realities of the job — firehouse culture, shift work fatigue, and critical incident stress. "
        f"{tone_prompts[tone]} "
        f"Give perspective, encouragement, and practical tools. When someone is overwhelmed, recommend breathwork, grounding techniques, or a quick mindset tool. "
        f"Always coach toward emotional strength, clarity under pressure, and personal accountability. "
        f"Remind firefighters that adversity builds toughness. Hard calls, conflict, and failure are reps for mental growth and increased grit."
    )

    # Match a follow-up if applicable
    matched_prompt = ""
    lowered_input = user_input.lower()
    for keyword, followup in keyword_followups.items():
        if keyword in lowered_input:
            matched_prompt = followup
            break

    with st.spinner("Coach is thinking..."):
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        messages = [{"role": "system", "content": system_prompt}] + st.session_state.chat_history
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7
        )
        reply = response.choices[0].message.content
        if matched_prompt:
            reply += f"

{matched_prompt}"
        st.session_state.chat_history.append({"role": "assistant", "content": reply})

# Chat Display (after toolkit and tone)
for msg in st.session_state.chat_history:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Footer
st.markdown("---")
st.caption("🚧 This is a demonstration version of the CCFD Mindset & Mental Health Coach. It is a work in progress and not a substitute for professional clinical support.")
