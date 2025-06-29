from langchain_core.messages import AIMessage
from utils.state import ReviewState


def chatbot(state: ReviewState) -> ReviewState:
    if state.report:
        last_msg = state.messages[-1]["content"].lower() if state.messages else ""
        if "accept" in last_msg:
            state.messages.append(AIMessage(content="Thank you for accepting the review. Your resume is now ready for submission."))
            return state
        elif "refine" in last_msg or "improve" in last_msg:
            state.messages.append(AIMessage(content="Thank you for your feedback. Let's work on refining the resume."))
            return state
        else:
            state.messages.append(AIMessage(content="Thank you for your feedback. If you have any specific requests, please let me know."))
            return state

    return state

def adjunct(state: ReviewState) -> ReviewState:
    """Adjunct node to handle the transition from chatbot to analysis."""
    return state