from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from llm_config import main_llm
from utils.state import ReviewState
from utils.prompt_helper import load_prompt


async def review_agent(state: ReviewState) -> ReviewState:
    """Review the resume against the job description."""
    # If there are any errors from the previous stage, return early
    if state.has_error:
        return state
    # Ensure both resume and job description analyses are available
    if not state.resume or not state.resume.get("analysis") or\
        not state.job or not state.job.get("analysis"):
        state.has_error = True
        state.messages.append(AIMessage(content="There are issues with analysing the resume or job description. Please ensure both are provided and properly formatted."))
        return state
    
    # Generate messages for resume review
    try:
        prompt = load_prompt("review")
    except FileNotFoundError as e:
        state.has_error = True
        state.messages.append(AIMessage(content=str(e)))
        return state

    state.messages.append(SystemMessage(content=prompt))
    state.messages.append(HumanMessage(content=f"Resume:\n{state.resume.get('analysis')}\n\nJob Description:\n{state.job.get('analysis')}"))

    # Invoke LLM to review the resume
    llm_output = await main_llm.ainvoke(state.messages)
    state.messages.append(AIMessage(content=llm_output.content))
    state.report = str(llm_output.content)

    return state