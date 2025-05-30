
import streamlit as st
from openai import OpenAI
from datetime import datetime
import pandas as pd
import os
import uuid

st.set_page_config(
    page_title="Clark County Fire Coach",
    page_icon="🚒",
    layout="wide"
)

# Load logo
st.image("CCFD_Patch1.PNG", width=150)
st.title("🚒 Clark County Fire Department AI Coach")
st.markdown("*Responding with Integrity. Serving with Compassion.*")
st.markdown("**Core Values: Pride, Passion & Professionalism**")

# Session state for chat history and metadata
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "You are an empathetic AI mental health and mindset coach for firefighters. Speak like a seasoned firefighter—grounded, relatable, and practical. Encourage growth mindset and resilience."}
    ]
if "checkin_type" not in st.session_state:
    st.session_state.checkin_type = None
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "start_time" not in st.session_state:
    st.session_state.start_time = datetime.now()

# Sidebar for admin and controls
with st.sidebar:
    st.markdown("### 🛠️ Options")
    if st.button("🔁 Reset Conversation"):
        st.session_state.chat_history = st.session_state.chat_history[:1]
        st.session_state.checkin_type = None
        st.experimental_rerun()

    if "admin" in st.query_params:
        st.markdown("### 📊 Admin Mode")
        log_file = "session_logs.csv"
        if os.path.exists(log_file):
            df = pd.read_csv(log_file)
            st.metric("Total Sessions", len(df))
            st.metric("Avg Duration (sec)", round(df["duration"].mean(), 2))
            st.dataframe(df.tail(10))
        else:
            st.info("No session logs yet.")

# Initial topic selection
if st.session_state.checkin_type is None:
    st.session_state.checkin_type = st.radio("What kind of check-in would you like to start with?", [
        "How I'm feeling mentally",
        "How I slept last night",
        "Stress level check",
        "Mindset reset (Growth Mindset Prompt)"
    ])
    st.session_state.chat_history.append(
        {"role": "user", "content": f"I’d like to start with a {st.session_state.checkin_type.lower()} check-in."}
    )

# Display conversation history
for msg in st.session_state.chat_history[1:]:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**AI Coach:** {msg['content']}")

# User input
user_input = st.text_input("Your message:", key="user_input")

if st.button("Send"):
    if user_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.spinner("Coach is thinking..."):
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=st.session_state.chat_history,
                temperature=0.7
            )
            ai_reply = response.choices[0].message.content
            st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})

        st.experimental_rerun()

# Log session metadata on exit
if "end_logged" not in st.session_state and len(st.session_state.chat_history) > 2:
    duration = (datetime.now() - st.session_state.start_time).total_seconds()
    inputs = sum(1 for m in st.session_state.chat_history if m["role"] == "user")
    log_file = "session_logs.csv"
    if not os.path.exists(log_file):
        pd.DataFrame(columns=["session_id", "timestamp", "topic", "inputs", "duration"]).to_csv(log_file, index=False)
    log_df = pd.read_csv(log_file)
    log_df = pd.concat([log_df, pd.DataFrame([{
        "session_id": st.session_state.session_id,
        "timestamp": datetime.now().isoformat(),
        "topic": st.session_state.checkin_type,
        "inputs": inputs,
        "duration": duration
    }])])
    log_df.to_csv(log_file, index=False)
    st.session_state.end_logged = True
