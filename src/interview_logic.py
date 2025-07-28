# src/interview_logic.py

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# Initialize the Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5, top_p=0.9)

# Pre-defined list of Excel questions
EXCEL_QUESTIONS = [
    "What is the difference between the VLOOKUP and HLOOKUP functions in Excel?",
    "Explain how to use the INDEX and MATCH functions together, and why you might prefer them over VLOOKUP.",
    "Describe what a Pivot Table is and give an example of a scenario where it would be useful.",
    "What is Conditional Formatting in Excel? Can you provide an example?",
    "How would you use the IFERROR function? Give a practical example.",
    "Explain the purpose of the SUMIFS function and how it differs from SUMIF."
]

# CHANGE THE TYPE HINT IN THE FUNCTION SIGNATURE
def start_interview(state: dict) -> dict:
    """
    Node to start the interview, introduce the agent, and explain the process.
    """
    intro_message = (
        "Welcome to the automated Excel skills assessment. This system is designed to help us understand your proficiency in advanced Excel, a key skill for our Finance, Operations, and Data Analytics roles. "
        "I will ask you a series of technical questions. Please provide clear and concise answers. Your performance summary will be generated at the end. "
        "Let's begin."
    )
    return {
        **state,
        "interview_status": 1, 
        "interview_history": [("ai", intro_message)],
        "questions": EXCEL_QUESTIONS,
        "question_index": 0,
        "evaluations": [],      # Explicitly initialize evaluations
        "final_feedback": "",   # Explicitly initialize final_feedback
    }

def ask_question(state: dict) -> dict:
    question_index = state["question_index"]
    current_question = state["questions"][question_index]
    
    history = state.get("interview_history", [])
    history.append(("ai", current_question))
    
    return { **state, "interview_history": history }

def process_user_response(state: dict) -> dict:
    """
    Node to evaluate the user's latest response from the history.
    It no longer takes console input.
    """
    history = state.get("interview_history", [])
    if not history or history[-1][0] != "human":
        raise ValueError("No user response found in history to evaluate.")

    user_response = history[-1][1]
    current_question = state["questions"][state["question_index"]]

    evaluation_prompt = ChatPromptTemplate.from_messages([
        ("system", 
         "You are an automated evaluation system for a company's hiring pipeline. Your purpose is to provide a consistent, unbiased evaluation of a candidate's technical Excel skills to help senior analysts make faster screening decisions. "
         "Evaluate the candidate's answer based on the following strict criteria:\n"
         "1.  **Technical Accuracy:** Is the explanation of the function or concept factually correct?\n"
         "2.  **Clarity and Conciseness:** Is the answer clear, easy to understand, and to the point, as expected in a professional setting?\n"
         "3.  **Completeness and Best Practices:** Did the candidate cover all key aspects of the question? Did they mention why one method might be preferred over another (e.g., INDEX/MATCH vs. VLOOKUP)?\n\n"
         "Provide a single, concise paragraph summarizing the evaluation. Do not be conversational. Start directly with the evaluation."
        ),
        ("human", f"Question: {current_question}\n\nCandidate's Answer: {user_response}")
    ])
    evaluator_chain = evaluation_prompt | llm
    
    print("AI: (Evaluating answer...)")
    evaluation = evaluator_chain.invoke({}).content
    print(f"AI: (Evaluation complete: {evaluation})")

    evaluations = state.get("evaluations", [])
    evaluations.append(evaluation)

    return {
        **state,
        "evaluations": evaluations,
        "question_index": state["question_index"] + 1
    }

def generate_final_report(state: dict) -> dict:
    interview_transcript = "\n".join([f"{speaker.capitalize()}: {text}" for speaker, text in state['interview_history']])
    evaluations_summary = "\n\n".join(f"Evaluation for Question {i+1}:\n{e}" for i, e in enumerate(state['evaluations']))

    report_prompt = ChatPromptTemplate.from_template(
        "You are an AI Recruitment Analyst. Your mission is to generate a comprehensive, constructive performance summary for a candidate who has just completed a mock technical interview for an advanced Excel role (e.g., for Finance, Operations, or Data Analytics).\n\n"
        "You will be given the full interview transcript and a series of per-question evaluations. Your report must be structured using Markdown as follows:\n\n"
        "### Overall Performance Summary\n"
        "A brief, high-level summary of the candidate's performance, mentioning their overall grasp of Excel concepts.\n\n"
        "### Strengths\n"
        "- Use bullet points to list specific areas where the candidate excelled. Mention specific examples from the interview (e.g., 'Provided a clear and accurate explanation of INDEX/MATCH').\n\n"
        "### Areas for Improvement\n"
        "- Use bullet points to list specific, actionable areas for improvement. Be constructive and suggest what to focus on (e.g., 'Could provide more detail on the practical business use cases for Pivot Tables.').\n\n"
        "The tone should be professional, encouraging, and objective, providing clear evidence from the interview to support your points.\n\n"
        "---\n**Interview Transcript**\n{transcript}\n\n"
        "---\n**Answer Evaluations**\n{evaluations}\n---"
    )
    report_chain = report_prompt | llm
    final_feedback = report_chain.invoke({"transcript": interview_transcript, "evaluations": evaluations_summary}).content
    
    history = state.get("interview_history", [])
    history.append(("ai", final_feedback))

    return {**state, "final_feedback": final_feedback, "interview_history": history, "interview_status": 2} # <-- CHANGE HERE (Set status to "Finished")

def route_after_evaluation(state: dict):
    if state["question_index"] >= len(state["questions"]):
        return "generate_final_report"
    else:
        return "ask_question"

def route_start_of_interview(state: dict):
    """
    Routes based on the interview status.
    """
    # CHANGE THIS LOGIC:
    if state.get("interview_status", 0) == 0:
        return "start_interview"
    else:
        return "process_user_response"