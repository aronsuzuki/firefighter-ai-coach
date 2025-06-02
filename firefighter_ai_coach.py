
import streamlit as st
import openai

st.set_page_config(page_title="CCFD Mindset & Mental Health Coach", layout="wide")

# App Header with Logo and Title
col1, col2 = st.columns([1, 6])
with col1:
    st.image("ccfd_logo.png", width=80)
with col2:
    st.markdown("## CCFD Mindset & Mental Health Coach")

# Separator and Instructions
st.markdown("---")
st.markdown("You’re in control here. This chat doesn’t report anything or judge you. Use the field below to talk about what’s on your mind, or pick something from the mindset toolkit. You can also guide the tone to match how you want to be coached today.")

# Tone Selector and Mindset Toolkit
tone = st.selectbox("Select coaching tone", ["Conversational", "Calm & Clinical", "Tough Love"])

toolkit_options = {
    "Reset": ["Breathing Reset", "Tactical Reframe", "Mind Sweep"],
    "Clarity": ["Decision Lens", "Mental Rehearsal", "Get Unstuck"],
    "Communication": ["Crucial Conversation", "Mentalizing", "Repair Attempt"],
}

selected_tool = st.selectbox("Mindset Toolkit", [""] + [f"{category}: {tool}" for category in toolkit_options for tool in toolkit_options[category]])

# Tone prompts
tone_prompts = {
    "Conversational": "Sound like a relatable and supportive firehouse peer.",
    "Calm & Clinical": "Use a calm, concise, slightly clinical tone like a seasoned CISM clinician.",
    "Tough Love": "Use a direct, no-BS tone like a salty firefighter who cares but doesn't coddle.",
}

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# System prompt
system_prompt = (
    f"You are an AI mindset and mental health coach for firefighters. "
    f"You speak like a trusted, seasoned peer — clear, grounded, gritty, and culturally fluent. "
    f"Use plain, direct language. Skip therapy jargon. Speak to the realities of the job — firehouse culture, shift work fatigue, and critical incident stress. "
    f"{tone_prompts[tone]} "
    f"Give perspective, encouragement, and practical tools. When someone is overwhelmed, recommend breathwork, grounding techniques, or a quick mindset tool. "
    f"Always coach toward emotional strength, clarity under pressure, and personal accountability. "
    f"Remind firefighters that adversity builds toughness. Hard calls, conflict, and failure are reps for mental growth and increased grit."
)

# Keyword-based follow-up prompts
keyword_prompts = {
    "fatigue": "Want to talk about how you're managing rest and recovery lately?",
    "anxious": "What’s been the biggest source of that anxious feeling?",
    "burnout": "Do you feel it’s the calls, the culture, or something off shift weighing you down?",
    "call": "Was it a recent call that triggered this? Walk me through it.",
    "drinking": "Has drinking, gambling, or anything else been creeping in more than usual?",
    "gambling": "Has drinking, gambling, or anything else been creeping in more than usual?",
    "drugs": "Has drinking, gambling, or anything else been creeping in more than usual?",
    "relationship": "Want to break down what’s been hardest about that relationship dynamic?",
    "wife": "Want to break down what’s been hardest about that relationship dynamic?",
    "husband": "Want to break down what’s been hardest about that relationship dynamic?",
    "family": "Are you feeling supported at home, or stretched thin in both places?",
    "kids": "Are you feeling supported at home, or stretched thin in both places?",
    "sponsor": "Do you have a sponsor, support group, or peer to talk through things with?",
    "rehab": "Is this something you're thinking about addressing with more structure or support?",
}

# Input field
user_input = st.text_input("How you doin’?", key="user_input")
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Build conversation
    messages = [{"role": "system", "content": system_prompt}] + st.session_state.chat_history

    # OpenAI API call (dummy response for offline demo)
    assistant_reply = f"Thanks for sharing. Let's unpack that a bit."

    # Add follow-up prompt if keyword match is found
    matched = next((prompt for keyword, prompt in keyword_prompts.items() if keyword in user_input.lower()), None)
    if matched:
        assistant_reply += " " + matched

    # Append response
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_reply})

# Display messages
st.markdown("---")
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f"**You:** {message['content']}")
    elif message["role"] == "assistant":
        st.markdown(f"**Coach:** {message['content']}")

# Disclaimer Footer
st.markdown("---")
st.markdown("**Disclaimer:** This is a demo. It’s not a substitute for professional mental health care. No data is saved or reported.")
