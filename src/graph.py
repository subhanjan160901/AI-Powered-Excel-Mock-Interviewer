from langgraph.graph import StateGraph, END
from . import interview_logic

def build_graph():
    """
    Builds the LangGraph for the mock interview process.
    """
    workflow = StateGraph(dict)

    # Add nodes (no changes here)
    workflow.add_node("start_interview", interview_logic.start_interview)
    workflow.add_node("ask_question", interview_logic.ask_question)
    workflow.add_node("process_user_response", interview_logic.process_user_response)
    workflow.add_node("generate_final_report", interview_logic.generate_final_report)

    # Entry point (no changes here)
    workflow.set_conditional_entry_point(
        interview_logic.route_start_of_interview,
    )

    # --- THIS IS THE CRITICAL FIX ---

    # The flow from start to the first question is correct.
    workflow.add_edge("start_interview", "ask_question")
    
    # After asking a question, the graph should STOP for that turn.
    # This allows the UI to wait for user input.
    workflow.add_edge("ask_question", END) # <--- THIS IS THE FIX

    # The conditional edge should ONLY come from process_user_response
    workflow.add_conditional_edges(
        "process_user_response",
        interview_logic.route_after_evaluation,
        {
            "ask_question": "ask_question",
            "generate_final_report": "generate_final_report",
            "terminate": END
        }
    )
    
    # The final report node still ends the graph normally.
    workflow.add_edge("generate_final_report", END)

    # Compile the graph
    return workflow.compile()