
import streamlit as st
from openai import OpenAI
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
import uuid

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Log file setup
log_file = "session_logs.csv"
if not os.path.exists(log_file):
    pd.DataFrame(columns=["session_id", "timestamp", "topic", "inputs", "duration"]).to_csv(log_file, index=False)

st.title("🧠 Firefighter AI Mental Health & Mindset Coach")

# Admin access for analytics
if "admin" in st.query_params:
    st.subheader("📊 Usage Analytics Dashboard")
    df = pd.read_csv(log_file)
    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        st.metric("Total Sessions", len(df))
        st.metric("Avg Duration (sec)", round(df["duration"].mean(), 2))

        fig1 = px.histogram(df, x="topic", title="Sessions by Topic")
        st.plotly_chart(fig1)

        df_daily = df.groupby(df["timestamp"].dt.date).count()
        fig2 = px.line(df_daily, y="session_id", title="Daily Usage Frequency")
        st.plotly_chart(fig2)
    else:
        st.info("No session data yet.")
    st.stop()

# Regular check-in flow
st.markdown("Welcome, brother/sister. Let’s check in. This is just between us.")

session_id = str(uuid.uuid4())
start_time = datetime.now()

checkin_type = st.radio("What do you want to check in on today?", [
    "How I'm feeling mentally",
    "How I slept last night",
    "Stress level check",
    "Mindset reset (Growth Mindset Prompt)"
])

user_input = st.text_area("What's on your mind?", height=150)

if st.button("Submit"):
    with st.spinner("Talking with your AI coach..."):
        prompt = f"""You are an AI mental health and mindset coach tailored for firefighters. You speak like a seasoned firefighter—empathetic, real, and direct. 
        A firefighter just shared this in a {checkin_type.lower()} check-in:

        '{user_input}'

        Respond with understanding, and guide them with either a grounding exercise, growth mindset insight (challenges are gifts), or resilience coaching depending on what they said."""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an empathetic AI coach for firefighters."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        ai_message = response.choices[0].message.content
        st.markdown("### 🔊 Your AI Coach Says:")
        st.markdown(ai_message)

        # Log session data
        duration = (datetime.now() - start_time).total_seconds()
        inputs = len(user_input.split())
        log_df = pd.read_csv(log_file)
        log_df = pd.concat([log_df, pd.DataFrame([{
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "topic": checkin_type,
            "inputs": inputs,
            "duration": duration
        }])])
        log_df.to_csv(log_file, index=False)
