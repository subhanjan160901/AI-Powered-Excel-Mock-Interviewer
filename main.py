# main.py - NEW STREAMLIT VERSION

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/subhanjanbasu/Desktop/ai_interviewer/service.json"


from dotenv import load_dotenv
import streamlit as st
from src.graph import build_graph



# --- Page and Model Setup ---

# Load environment variables
load_dotenv()



# Check for API key and build the LangGraph app
# This part is moved to the top to fail fast if the key is missing
if not os.getenv("GOOGLE_API_KEY"):
    st.error("Error: GOOGLE_API_KEY not found. Please set it in your .env file and restart.")
    st.stop()

app = build_graph()

# Set the title of the Streamlit page
st.title("🤖 AI-Powered Excel Mock Interviewer")
st.markdown("Welcome! This tool will conduct a mock technical interview to assess your Excel skills. Click 'Start New Interview' to begin.")

# --- Core Functions ---

def run_graph(current_state: dict) -> dict:
    """Invokes the graph and returns the final state of that run."""
    return app.invoke(current_state)

# --- Session State and UI ---

# Initialize session state if it doesn't exist
if "interviewer_state" not in st.session_state:
    st.session_state.interviewer_state = {
        "interview_status": 0, # 0: Not Started, 1: In Progress, 2: Finished
        "interview_history": [],
        "questions": [],
        "question_index": 0,
        "evaluations": [],
        "final_feedback": ""
    }

# Display the chat history
for message in st.session_state.interviewer_state.get("interview_history", []):
    role, text = message
    if role == "ai":
        with st.chat_message("assistant"):
            st.markdown(text)
    elif role == "human":
        with st.chat_message("user"):
            st.markdown(text)

# --- Buttons and Input Handling ---

# Button to start a new interview
if st.button("Start New Interview"):
    # Reset the state and start the interview
    st.session_state.interviewer_state = {
        "interview_status": 0,
        "interview_history": [],
        "questions": [],
        "question_index": 0,
        "evaluations": [],
        "final_feedback": ""
    }
    # Run the graph to get the welcome message
    initial_state = st.session_state.interviewer_state
    new_state = run_graph(initial_state)
    st.session_state.interviewer_state = new_state
    st.rerun() # Rerun the script to display the new messages

# Handle user input only if the interview is in progress
if st.session_state.interviewer_state["interview_status"] == 1:
    if prompt := st.chat_input("Your answer..."):
        # Add user message to state
        current_state = st.session_state.interviewer_state
        current_state["interview_history"].append(("human", prompt))
        
        # Run the graph to get the AI's response (evaluation + next question/report)
        new_state = run_graph(current_state)
        st.session_state.interviewer_state = new_state
        st.rerun() # Rerun the script to display the new messages

# Display a message when the interview is finished
elif st.session_state.interviewer_state["interview_status"] == 2:
    st.success("Interview complete! You can find your performance report above. Click 'Start New Interview' to try again.")
