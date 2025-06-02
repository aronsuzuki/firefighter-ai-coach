import streamlit as st
from openai import OpenAI
from datetime import datetime
import os
import json

st.set_page_config(page_title="CCFD Mindset & Mental Health Coach", page_icon="🧠")

# --- Branding and Layout ---
col1, col2 = st.columns([1, 6])
with col1:
    st.image("CCFD_Patch1.PNG", width=80)
with col2:
    st.title("CCFD Mindset & Mental Health Coach")

st.markdown("---")
st.markdown("You’re in control here. This chat doesn’t report anything or judge you. "
            "Use the box below to talk about what’s on your mind, or pick something from the mindset toolkit.")

# --- Tone selector ---
tone = st.selectbox("Select your preferred coaching tone:", ["Conversational", "Calm & Clinical", "Tough Love"])

tone_prompts = {
    "Conversational": "Speak casually and supportively, like a trusted peer at the station.",
    "Calm & Clinical": "Maintain a grounded, clinical tone — clear, calm, and supportive.",
    "Tough Love": "Be direct, challenge the user respectfully, and inspire accountability and growth."
}

# --- System prompt ---
system_prompt = (
    f"You are an AI mindset and mental health coach for firefighters. "
    f"You speak like a trusted, seasoned peer — clear, grounded, gritty, and culturally fluent. "
    f"Use plain, direct language. Skip therapy jargon. Speak to the realities of the job — firehouse culture, shift work fatigue, and critical incident stress. "
    f"{tone_prompts[tone]} "
    f"Give perspective, encouragement, and practical tools. When someone is overwhelmed, recommend breathwork, grounding techniques, or a quick mindset tool. "
    f"Always coach toward emotional strength, clarity under pressure, and personal accountability. "
    f"Remind firefighters that adversity builds toughness. Hard calls, conflict, and failure are reps for mental growth and increased grit."
)

# --- Keyword-based follow-up prompts ---
keyword_prompts = {
    "trust": "Sounds like trust has been tested. What would rebuilding that look like for you?",
    "team": "Team dynamics make or break morale. Is it support or friction right now?",
    "overwhelmed": "You’re carrying a lot. Want to talk about what’s feeling heaviest?",
    "burnout": "Burnout sneaks in quiet. What’s draining your tank most lately?",
    "fatigue": "Fatigue hits different in this line of work. Want to walk through what’s weighing you down?",
    "anger": "Anger’s a signal — not the whole story. Want to unpack what’s under it?",
    "anxious": "That unsettled edge is real. Want to sort through what’s feeding it?",
    "grief": "Grief doesn’t run on a clock. What’s been hardest to carry?",
    "family": "Balancing home life with this job can be brutal. What’s been the hardest part lately?",
    "spouse": "Balancing home life with this job can be brutal. What’s been the hardest part lately?",
    "wife": "Balancing home life with this job can be brutal. What’s been the hardest part lately?",
    "husband": "Balancing home life with this job can be brutal. What’s been the hardest part lately?",
    "partner": "Balancing home life with this job can be brutal. What’s been the hardest part lately?",
    "kids": "Balancing home life with this job can be brutal. What’s been the hardest part lately?",
    "home": "Balancing home life with this job can be brutal. What’s been the hardest part lately?",
    "drinking": "Thanks for being real about that. Want to talk about what role that’s playing right now?",
    "alcohol": "Thanks for being real about that. Want to talk about what role that’s playing right now?",
    "substance": "Thanks for being real about that. Want to talk about what role that’s playing right now?",
    "gambling": "Thanks for being real about that. Want to talk about what role that’s playing right now?",
    "drugs": "Thanks for being real about that. Want to talk about what role that’s playing right now?",
    "sponsor": "Thanks for being real about that. Want to talk about what role that’s playing right now?",
    "rehab": "Thanks for being real about that. Want to talk about what role that’s playing right now?",
    "injury": "Being sidelined physically hits harder than it looks. How are you dealing with that frustration?",
    "pain": "Being sidelined physically hits harder than it looks. How are you dealing with that frustration?",
    "back": "Being sidelined physically hits harder than it looks. How are you dealing with that frustration?",
    "recovery": "Being sidelined physically hits harder than it looks. How are you dealing with that frustration?",
    "retirement": "Planning your next chapter can feel heavy. What would a win look like for you in the long run?",
    "future": "Planning your next chapter can feel heavy. What would a win look like for you in the long run?",
    "career": "Planning your next chapter can feel heavy. What would a win look like for you in the long run?"
}

# --- Chat history ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "system", "content": system_prompt}]

# --- Mindset Toolkit Placeholder ---
st.markdown("### 🧰 Mindset Toolkit")
selected_tool = st.selectbox("Choose a tool to help right now:", ["", "🧘 Breath Reset", "✅ Celebrate One Win", "🎭 Crucial Conversation Role-play"])
if selected_tool == "🧘 Breath Reset":
    st.info("Try this: Inhale for 4, hold for 4, exhale for 4, hold for 4. Repeat 3 times.")
elif selected_tool == "✅ Celebrate One Win":
    st.info("What’s one thing you handled well today — even if it’s small?")
elif selected_tool == "🎭 Crucial Conversation Role-play":
    st.info("Think of a high-stakes convo you’re dreading. Want to practice what to say and how to stay grounded?")

st.markdown("---")

# --- Chat Input ---
user_input = st.chat_input("How you doin? What’s on your mind?")

# --- Process Chat ---
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

# --- Display Chat ---
for msg in st.session_state.chat_history[1:]:
    st.chat_message(msg["role"]).markdown(msg["content"])

# --- Display Smart Follow-up Prompt (if no tool selected) ---
if user_input and selected_tool == "":
    lower_input = user_input.lower()
    for keyword, prompt in keyword_prompts.items():
        if keyword in lower_input:
            st.chat_message("assistant").markdown(f"**Follow-up:** {prompt}")
            break

# --- Footer Disclaimer ---
st.markdown("---")
st.caption("🚧 This is a demonstration version of the CCFD Mindset & Mental Health Coach. It is a work in progress and not a substitute for professional clinical support.")