
import streamlit as st
from openai import OpenAI
from datetime import datetime
import os
import json

st.set_page_config(page_title="CCFD Mindset & Mental Health Coach", page_icon="🧠")

# Layout: Logo and Title
col1, col2 = st.columns([1, 6])
with col1:
    st.image("CCFD_Patch1.PNG", width=80)
with col2:
    st.title("🚒 CCFD Mindset & Mental Health Coach")
st.markdown("<hr style='margin-top:0;'>", unsafe_allow_html=True)

# Instruction paragraph
st.markdown("High Performers prioritize their mental health. Use the box below to talk about what’s on your mind, or pick something from the mindset toolkit. You can also guide the tone to match how you want to be coached today.")

# Initialize tone prompts and selector (placed after chat input)
tone_prompts = {
    "Conversational": "Speak casually and supportively, like a trusted peer at the station.",
    "Calm & Clinical": "Maintain a grounded, clinical tone — clear, calm, and supportive.",
    "Tough Love": "Be direct, challenge the user respectfully, and inspire accountability and growth."
}

# Mindset Toolkit (single dropdown with category + tool)
tool_options = {
    "Reset: Box Breathing": "Take a breath: inhale 4, hold 4, exhale 4, hold 4. Repeat for 4 rounds.",
    "Reset: Let it Pass": "Note what you’re feeling. Label it. Say: 'It’s okay to feel this. It’ll pass.'",
    "Reset: Control Reset": "Ask: What’s mine to control? Let go of what isn’t.",
    "Reframe: Strongest Self": "What would the strongest version of you say about this?",
    "Reframe: Shift the Story": "Is there a more helpful story you could tell yourself about this?",
    "Reframe: Flash Forward": "Will this still matter in a week, a month, or a year?",
    "Reconnect: One Win": "Name one thing you got right today, even if it’s small.",
    "Reconnect: Call a Teammate": "Consider texting or calling a teammate. Connection is medicine.",
    "Reconnect: Pride Reminder": "What about your work gives you pride, even on hard days?",
    "Crucial Conversation": "Let’s walk through a tough conversation together. What’s the context?"
}

selected_tool = st.selectbox("🧰 Mindset Toolkit", options=[""] + list(tool_options.keys()))
if selected_tool and selected_tool in tool_options:
    st.info(tool_options[selected_tool])

# Chat input
user_input = st.chat_input("How you doin? What’s on your mind?")
tone = st.selectbox("Select your preferred coaching tone:", list(tone_prompts.keys()))

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# System prompt with growth-through-adversity emphasis
system_prompt = (
    f"You are an AI mindset and mental health coach for firefighters. "
    f"You speak like a trusted, seasoned peer — clear, grounded, and culturally fluent. "
    f"Use plain, direct language. Skip therapy jargon. Speak to the realities of firehouse life — shift work, adrenaline dumps, and tough calls. "
    f"{tone_prompt} "
    f"Give perspective, encouragement, and practical tools. When someone sounds overwhelmed, offer grounding, breathing, or a short mindset reset. "
    f"Always coach toward emotional strength, clarity under pressure, and personal accountability. "
    f"Remind firefighters that challenges are not setbacks — they’re reps that build mental and emotional muscle. Resilience is earned by facing the hard stuff, not avoiding it."
).replace("{tone_prompt}", tone_prompts[tone])

# Append messages and get response
if user_input:
    if not any(msg["role"] == "system" for msg in st.session_state.chat_history):
        st.session_state.chat_history.insert(0, {"role": "system", "content": system_prompt})
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

        # Log interaction
        os.makedirs("logs", exist_ok=True)
        log_data = {
            "timestamp": str(datetime.now()),
            "tone": tone,
            "tool": selected_tool,
            "input": user_input,
            "output": reply
        }
        with open(f"logs/{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
            json.dump(log_data, f)

# Display conversation (without duplication)
st.markdown("<hr style='margin-top:1.5em;'>", unsafe_allow_html=True)
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").markdown(msg["content"])

# Footer disclaimer
st.markdown("---")
st.caption("🚧 This is a demonstration version of the CCFD Mindset & Mental Health Coach. It is a work in progress and not a substitute for professional clinical support.")
