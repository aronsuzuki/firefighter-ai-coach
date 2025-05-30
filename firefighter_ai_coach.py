
import streamlit as st
import openai

# Set your OpenAI API key here or use Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("🧠 Firefighter AI Mental Health & Mindset Coach")

st.markdown("Welcome, brother/sister. Let’s check in for a moment. This is just between us.")

# Initial check-in
checkin_type = st.radio("What do you want to check in on today?", [
    "How I'm feeling mentally",
    "How I slept last night",
    "Stress level check",
    "Mindset reset (Growth Mindset Prompt)"
])

user_input = st.text_area("What's on your mind?", height=150)

if st.button("Submit"):
    with st.spinner("Talking with your AI coach..."):
        prompt = f"You are an AI mental health and mindset coach tailored for firefighters. You speak like a seasoned firefighter—empathetic, real, and direct. A firefighter just shared this in a {checkin_type.lower()} check-in:

'{user_input}'

Respond with understanding, and guide them with either a grounding exercise, growth mindset insight (challenges are gifts), or resilience coaching depending on what they said."

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an empathetic AI coach for firefighters."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        ai_message = response['choices'][0]['message']['content']
        st.markdown("### 🔊 Your AI Coach Says:")
        st.markdown(ai_message)
