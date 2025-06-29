from langgraph.graph import END
from utils.state import ReviewState


def proceed_router(state: ReviewState) -> str:
    if not state.resume or not state.resume.get("file") or not state.job or not state.job.get("desc"):
        return "chatbot"
    elif state.has_error:
        return END
    return "proceed"