# main.py

import streamlit as st
from src.graph import build_graph

# No more API key logic!
app = build_graph()

st.title("🤖 AI-Powered Excel Mock Interviewer (Local LLM)")
st.markdown("Welcome! This tool uses a self-hosted open-source model to conduct the interview. Click 'Start New Interview' to begin.")

# The rest of your UI logic for session state, chat display, and buttons
# remains exactly the same as your last working version.

# Session State Initialization
if "interviewer_state" not in st.session_state:
    st.session_state.interviewer_state = {
        "interview_status": 0, "interview_history": [], "questions": [],
        "question_index": 0, "evaluations": [], "final_feedback": "", "warnings": []
    }

# Display chat history
for message in st.session_state.interviewer_state.get("interview_history", []):
    role, text = message
    with st.chat_message("user" if role == "human" else "assistant"):
        st.markdown(text)

# Button handling
if st.button("Start New Interview"):
    st.session_state.interviewer_state = {
        "interview_status": 0, "interview_history": [], "questions": [],
        "question_index": 0, "evaluations": [], "final_feedback": "", "warnings": []
    }
    new_state = run_graph(st.session_state.interviewer_state)
    st.session_state.interviewer_state = new_state
    st.rerun()

# Input handling
if st.session_state.interviewer_state["interview_status"] == 1:
    if prompt := st.chat_input("Your answer..."):
        current_state = st.session_state.interviewer_state
        current_state["interview_history"].append(("human", prompt))
        new_state = run_graph(current_state)
        st.session_state.interviewer_state = new_state
        st.rerun()
elif st.session_state.interviewer_state["interview_status"] == 2:
    st.success("Interview complete!")
