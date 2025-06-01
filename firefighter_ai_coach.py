
import streamlit as st
from openai import OpenAI
from datetime import datetime
import os
import json

st.set_page_config(page_title="CCFD Mindset & Mental Health Coach", page_icon="🧠")

# Branding
st.image("CCFD_Patch1.PNG", width=100)
st.title("🚒 CCFD Mindset & Mental Health Coach")
st.markdown("High Performers prioritize their mental health. Use the box below to talk about what’s on your mind, or pick something from the mindset toolkit dropdown. You can also guide the tone to match how you want to be coached today.")

# Micro-Coaching Modules (Grouped by Theme)
st.markdown("### 🧰 Mindset Toolkit")
tool_groups = {
    "Resilience & Reset": [
        "🧘 Breath + Reframe",
        "🌊 Let Go of Rumination",
        "⏸ Pause + Recenter"
    ],
    "Confidence & Wins": [
        "✅ Celebrate One Win",
        "💪 Confidence Check"
    ],
    "Communication & Clarity": [
        "🧠 Clear Mind After Miscommunication",
        "🎭 Role-play a Crucial Conversation"
    ]
}
selected_tool = st.selectbox("Choose a tool to help right now:", ["None"] + [tool for group in tool_groups.values() for tool in group])
if selected_tool == "🧘 Breath + Reframe":
    st.info("Box breathe: Inhale 4, hold 4, exhale 4, hold 4. Then reframe: *What would the strongest version of you say about this moment?*")
elif selected_tool == "✅ Celebrate One Win":
    st.info("What’s one thing you got right today — even if it’s small?")
elif selected_tool == "🧠 Clear Mind After Miscommunication":
    st.info("Reflect: What emotion are you holding? Who benefits if you let it go? Say: *I didn’t know then what I know now. I’ll do better next time.*")
elif selected_tool == "🌊 Let Go of Rumination":
    st.info("Name the loop. Say it out loud. Decide: Will you act on it or accept it? Then breathe. Let it pass.")
elif selected_tool == "💪 Confidence Check":
    st.info("When did you last overcome something hard? What helped you do it? You’ve got proof you can handle pressure.")
elif selected_tool == "🎭 Role-play a Crucial Conversation":
    st.info("What do you want to say? Type what you'd say in the heat of the moment. The coach will guide you toward a more effective version.")

# Tone Selector — moved below chat input
st.markdown("---")
tone = st.selectbox("Preferred coaching tone:", ["Conversational", "Calm & Clinical", "Tough Love"])
st.markdown("---")
tone_prompts = {
    "Conversational": "Speak casually and supportively, like a trusted peer at the station.",
    "Calm & Clinical": "Maintain a grounded, clinical tone — clear, calm, and supportive.",
    "Tough Love": "Be direct, challenge the user respectfully, and inspire accountability and growth."
}

# System prompt
system_prompt = (
    f"You are an AI mindset and mental health coach for firefighters. "
    f"You speak like a trusted, seasoned peer — clear, grounded, culturally fluent. "
    f"Use plain language. Avoid therapy buzzwords. Reference firehouse culture, shift work stress, and real calls. "
    f"{tone_prompts[tone]} "
    f"Offer mindset tools and encouragement. When distress is high, recommend grounding techniques, breathing, or a quick micro-coaching tool. "
    f"Always prioritize emotional resilience, mental clarity, and personal accountability."
)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "system", "content": system_prompt}]

# Input and conversation flow
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

        # Append a context-aware follow-up prompt
        follow_ups = [
            ("angry", "Want help thinking through how to handle that anger constructively?"),
            ("stressed", "Would it help to talk about what’s stacking up for you?"),
            ("divorce", "Want to explore how to communicate clearly or set boundaries during this?"),
            ("kids", "Would it help to reflect on how to show up strong for your kids right now?"),
            ("fix", "Want to walk through what a calm conversation with her could sound like?"),
            ("alone", "Want to talk about who’s on your team right now and how to lean on them?")
        ]
        default_prompt = "Want to unpack that more or shift gears to something else on your mind?"
        context_prompt = next((msg for keyword, msg in follow_ups if keyword in user_input.lower()), default_prompt)
        reply += f"\n\n---\n_{context_prompt}_"
        st.session_state.chat_history.append({"role": "assistant", "content": reply})

        # Log usage
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

# Render chat history
for msg in st.session_state.chat_history[1:]:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Disclaimer
st.markdown("---")
st.caption("🚧 This is a demonstration version of the CCFD Mindset & Mental Health Coach. It is a work in progress and not a substitute for professional clinical support.")
