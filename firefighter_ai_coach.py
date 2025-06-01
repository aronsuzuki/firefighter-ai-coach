
import streamlit as st
from openai import OpenAI
from datetime import datetime
import os
import json

st.set_page_config(page_title="CCFD Mindset & Mental Health Coach", page_icon="🧠")

# Two-column layout for logo and header
col1, col2 = st.columns([1, 6])
with col1:
    st.image("CCFD_Patch1.PNG", width=80)
with col2:
    st.markdown("## CCFD Mindset & Mental Health Coach")

# Separator line
st.markdown("---")

# Instructions paragraph
st.markdown("High Performers prioritize their mental health. Use the box below to talk about what’s on your mind, or pick something from the mindset toolkit dropdown. You can also guide the tone to match how you want to be coached today.")
