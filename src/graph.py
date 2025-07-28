from langgraph.graph import StateGraph, END
from . import interview_logic

def build_graph():
    """
    Builds the LangGraph for the mock interview process.
    """
    # CHANGE THIS LINE:
    workflow = StateGraph(dict) # Use dict instead of InterviewerState

    # Add the nodes to the graph
    workflow.add_node("start_interview", interview_logic.start_interview)
    workflow.add_node("ask_question", interview_logic.ask_question)
    workflow.add_node("process_user_response", interview_logic.process_user_response)
    workflow.add_node("generate_final_report", interview_logic.generate_final_report)

    # Conditional entry point
    workflow.set_conditional_entry_point(
        interview_logic.route_start_of_interview,
    )

    # Define the flow
    workflow.add_edge("start_interview", "ask_question")
    
    workflow.add_conditional_edges(
        "process_user_response",
        interview_logic.route_after_evaluation,
        {
            "ask_question": "ask_question",
            "generate_final_report": "generate_final_report"
        }
    )

    workflow.add_edge("ask_question", END)
    workflow.add_edge("generate_final_report", END)

    # Compile the graph
    return workflow.compile()