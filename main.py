# main.py - CORRECTED FOR STREAMLIT CLOUD DEPLOYMENT

import os
# We no longer need dotenv for deployment, but it's fine to keep for local runs.
from dotenv import load_dotenv
import streamlit as st
from src.graph import build_graph

# --- CRITICAL CHANGE FOR DEPLOYMENT ---
# REMOVE THE HARDCODED PATH TO YOUR LOCAL service.json FILE.
# This line will cause your app to crash on Streamlit Cloud.
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/subhanjanbasu/Desktop/excel_interviewer/AI-Powered-Excel-Mock-Interviewer/service.json"

# Load local .env file (this is for local development and will be ignored on Streamlit Cloud)
load_dotenv()

# Try to get the key from Streamlit's secrets manager first.
# This is the correct way for deployment.
try:
    # This line sets the environment variable that LangChain looks for.
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
except (KeyError, FileNotFoundError):
    # If not on Streamlit Cloud, fall back to the local .env file.
    # The check below will handle if it's still not found.
    pass

# Check if the API key is available
if not os.getenv("GOOGLE_API_KEY"):
    st.error("Error: GOOGLE_API_KEY not found. Please set it in Streamlit Cloud's secrets, or in a local .env file.")
    st.stop()

# Now that the key is set, we can build the graph
app = build_graph()

# --- THE REST OF YOUR UI CODE REMAINS THE SAME ---

st.title("🤖 AI-Powered Excel Mock Interviewer")
st.markdown("Welcome! This tool will conduct a mock technical interview to assess your Excel skills. Click 'Start New Interview' to begin.")

# Core Functions
def run_graph(current_state: dict) -> dict:
    return app.invoke(current_state)

# Session State and UI
if "interviewer_state" not in st.session_state:
    st.session_state.interviewer_state = {
        "interview_status": 0,
        "interview_history": [],
        "questions": [],
        "question_index": 0,
        "evaluations": [],
        "final_feedback": "",
        "warnings": []
    }

# Display chat history
for message in st.session_state.interviewer_state.get("interview_history", []):
    role, text = message
    if role == "ai":
        with st.chat_message("assistant"):
            st.markdown(text)
    elif role == "human":
        with st.chat_message("user"):
            st.markdown(text)

# Display warnings
if "warnings" in st.session_state.interviewer_state and st.session_state.interviewer_state["warnings"]:
    for warning in st.session_state.interviewer_state["warnings"]:
        st.warning(warning)
    st.session_state.interviewer_state["warnings"] = []

# Buttons and Input Handling
if st.button("Start New Interview"):
    st.session_state.interviewer_state = {
        "interview_status": 0, "interview_history": [], "questions": [], "question_index": 0,
        "evaluations": [], "final_feedback": "", "warnings": []
    }
    initial_state = st.session_state.interviewer_state
    new_state = run_graph(initial_state)
    st.session_state.interviewer_state = new_state
    st.rerun()

if st.session_state.interviewer_state["interview_status"] == 1:
    if prompt := st.chat_input("Your answer..."):
        current_state = st.session_state.interviewer_state
        current_state["interview_history"].append(("human", prompt))
        new_state = run_graph(current_state)
        st.session_state.interviewer_state = new_state
        st.rerun()

elif st.session_state.interviewer_state["interview_status"] == 2:
    st.success("Interview complete! You can find your performance report above. Click 'Start New Interview' to try again.")