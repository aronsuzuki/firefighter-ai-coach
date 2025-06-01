
import streamlit as st
from openai import OpenAI
from datetime import datetime
import os
import json

st.set_page_config(page_title="CCFD Mindset & Mental Health Coach", page_icon="🧠")

# Branding layout
col1, col2 = st.columns([1, 5])
with col1:
    st.image("CCFD_Patch1.PNG", width=80)
with col2:
    st.title("🚒 CCFD Mindset & Mental Health Coach")
    st.caption("Responding with Integrity • Serving with Compassion")
    st.markdown("High Performers prioritize their mental health. Use the box below to talk about what’s on your mind, or pick something from the mindset toolkit dropdown. You can also guide the tone to match how you want to be coached today.")

# Tone selection moved below input box
tone_prompts = {
    "Conversational": "Speak casually and supportively, like a trusted peer at the station.",
    "Calm & Clinical": "Maintain a grounded, clinical tone — clear, calm, and supportive.",
    "Tough Love": "Be direct, challenge the user respectfully, and inspire accountability and growth."
}

# Coaching Toolkit
toolkit = {
    "Reset": {
        "🧘 Box Breathing": "Breathe in for 4, hold for 4, out for 4, hold for 4. Repeat until grounded.",
        "💭 Reframe Challenge": "What would the strongest version of you say about this?",
        "🧠 Clear Mind After Miscommunication": "What emotion are you holding? Who benefits if you let it go?"
    },
    "Perspective": {
        "✅ Celebrate One Win": "Name one thing you got right today.",
        "🎯 What Matters Now": "What truly matters most in this moment?",
        "📌 5 Years From Now": "Will this still matter in 5 years?"
    },
    "Communication": {
        "🗣 Crucial Conversation Practice": "Let's role-play a high-stakes talk. What’s the topic?",
        "📢 Say It Better": "Want to say something clearly and respectfully? Type it and get help refining it.",
        "🔄 Repair the Bridge": "Want to patch up a rift? Let’s rehearse how to reopen dialogue."
    }
}

selected_tool_category = st.selectbox("Mindset Toolkit", list(toolkit.keys()))
selected_tool = st.selectbox("Tool Options", list(toolkit[selected_tool_category].keys()))
st.info(toolkit[selected_tool_category][selected_tool])

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.chat_input("How you doin? What’s on your mind?")
tone = st.selectbox("Coaching Tone", ["Conversational", "Calm & Clinical", "Tough Love"])
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    base_system_prompt = (
        "You are an AI mindset and mental health coach for firefighters. "
        "You speak like a trusted, seasoned peer — clear, grounded, culturally aware. "
        "Use plain language. Avoid therapy buzzwords. Reference firehouse culture and values. "
        f"{tone_prompts[tone]} "
        "Offer mindset tools and encouragement. When distress is high, recommend breathing, reframing, or a micro-win. "
        "Always prioritize emotional resilience, mental clarity, and personal accountability."
    )

    with st.spinner("Coach is thinking..."):
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        messages = [{"role": "system", "content": base_system_prompt}] + st.session_state.chat_history
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7
        )
        reply = response.choices[0].message.content
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").markdown(reply)

    # Log usage
    os.makedirs("logs", exist_ok=True)
    log_data = {
        "timestamp": str(datetime.now()),
        "tone": tone,
        "tool_category": selected_tool_category,
        "tool": selected_tool,
        "input": user_input,
        "output": reply
    }
    with open(f"logs/{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
        json.dump(log_data, f)

# Show conversation history
st.markdown("---")
for msg in st.session_state.chat_history:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Footer
st.markdown("---")
st.caption("🚧 This is a demonstration version of the CCFD Mindset & Mental Health Coach. It is a work in progress and not a substitute for professional clinical support.")
