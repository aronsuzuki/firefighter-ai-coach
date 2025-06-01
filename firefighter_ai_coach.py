import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="CCFD Mindset & Mental Health Coach", page_icon="🧠")

tone = st.selectbox("Select your preferred coaching tone:", ["Conversational", "Calm & Clinical", "Tough Love"])
tone_prompts = {
    "Conversational": "Speak casually and supportively, like a trusted peer at the station.",
    "Calm & Clinical": "Maintain a grounded, clinical tone — clear, calm, and supportive.",
    "Tough Love": "Be direct, challenge the user respectfully, and inspire accountability and growth."
}

# Apply the supercharged system message
system_prompt = f"""
"You are an AI mindset and mental health coach for firefighters. "
"You speak like a trusted, seasoned peer — clear, grounded, culturally aware. "
"Use plain language. Avoid therapy buzzwords. Reference firehouse culture: long shifts, trauma, pride, and teamwork. "
"{tone_prompt} "
"Offer mindset tools and encouragement. When distress is high, recommend speaking with peer support or EAP. "
"Always prioritize emotional resilience, mental clarity, and personal accountability."
""".replace("{tone_prompt}", tone_prompts[tone])

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "system", "content": system_prompt}]

st.title("🚒 CCFD Mindset & Mental Health Coach")
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
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").markdown(reply)

# Display full conversation
for msg in st.session_state.chat_history[1:]:
    st.chat_message(msg["role"]).markdown(msg["content"])
