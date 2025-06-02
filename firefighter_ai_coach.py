import streamlit as st
from openai import OpenAI
from datetime import datetime
import os
import json

st.set_page_config(page_title="CCFD Mindset & Mental Health Coach", page_icon="🧠")

col1, col2 = st.columns([1, 6])
with col1:
    st.image("CCFD_Patch1.PNG", width=100)
with col2:
    st.title("🚒 CCFD Mindset & Mental Health Coach")

st.markdown("<hr style='margin-top: 0;'>", unsafe_allow_html=True)

st.markdown("High Performers prioritize their mental health. Use the box below to talk about what’s on your mind, or pick something from the Mindset Toolkit dropdown. You can also guide the tone to match how you want to be coached today.")

tone_prompts = {
    "Conversational": "Speak casually and supportively, like a trusted peer at the station.",
    "Calm & Clinical": "Maintain a grounded, clinical tone — clear, calm, and supportive.",
    "Tough Love": "Be direct, challenge the user respectfully, and inspire accountability and growth."
}

toolkit_options = {
    "Reset Your Head": {
        "🧘 Just Breathe": "Box breathe: Inhale 4, hold 4, exhale 4, hold 4.",
        "🧠 Clear Miscommunication": "Reflect: What emotion are you holding? Who benefits if you let it go?",
        "📵 Shut Off the Noise": "Step away from screens. Take a break. Get sunlight or fresh air."
    },
    "Refocus with Purpose": {
        "✅ Celebrate a Win": "Name one thing you handled well today — even if it’s small.",
        "🎯 What’s In My Control?": "List 2 things you can control right now. Focus there.",
        "🔁 Shift Perspective": "What would the strongest version of you say about this moment?"
    },
    "Rebuild & Reconnect": {
        "💬 Role-play a Tough Conversation": "Play out a high-stakes convo. What needs to be said? Say it here.",
        "🧍‍♂️ You’re Not Alone": "Remember who you’d call if things got rough. Say what you’d tell them.",
        "📖 Learn the Lesson": "What’s one thing this moment is teaching you? Put it into words."
    }
}

toolkit_menu = [""]
toolkit_lookup = {}
for category, tools in toolkit_options.items():
    for label, content in tools.items():
        entry = f"{category} → {label}"
        toolkit_menu.append(entry)
        toolkit_lookup[entry] = content

selected_tool = st.selectbox("🧰 Mindset Toolkit", toolkit_menu)
if selected_tool and selected_tool in toolkit_lookup:
    st.info(toolkit_lookup[selected_tool])

st.markdown("---")
tone = st.selectbox("Preferred coaching tone:", list(tone_prompts.keys()))

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

system_prompt = (
    f"You are an AI mindset and mental health coach for firefighters. "
    f"You speak like a trusted, seasoned peer — clear, grounded, and culturally fluent. "
    f"Use plain, direct language. Skip therapy jargon. Speak to the realities of the job — firehouse culture, shift work fatigue, and critical incident stress. "
    f"{tone_prompts[tone]} "
    f"Give perspective, encouragement, and practical tools. When someone is overwhelmed, recommend breathwork, grounding techniques, or a quick mindset tool. "
    f"Always coach toward emotional strength, clarity under pressure, and personal accountability. "
    f"Remind firefighters that challenges are not setbacks — they’re reps for mental toughness."
)

user_input = st.chat_input("How you doin? What’s on your mind?")
if user_input:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    messages = [{"role": "system", "content": system_prompt}] + st.session_state.chat_history
    messages.append({"role": "user", "content": user_input})

    with st.spinner("Coach is thinking..."):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7
        )
        reply = response.choices[0].message.content.strip()
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({"role": "assistant", "content": reply})

        os.makedirs("logs", exist_ok=True)
        with open(f"logs/{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
            json.dump({
                "timestamp": str(datetime.now()),
                "tone": tone,
                "tool": selected_tool,
                "input": user_input,
                "output": reply
            }, f)

st.markdown("---")
for msg in st.session_state.chat_history:
    st.chat_message(msg["role"]).markdown(msg["content"])

st.markdown("""
<style>
#custom-footer {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: #f9f9f9;
    text-align: center;
    color: gray;
    padding: 10px 0;
    font-size: 0.8rem;
    z-index: 9999;
    border-top: 1px solid #ccc;
}
</style>
<div id="custom-footer">
🚧 This is a demonstration version of the CCFD Mindset & Mental Health Coach. It is a work in progress and not a substitute for professional clinical support.
</div>
""", unsafe_allow_html=True)

