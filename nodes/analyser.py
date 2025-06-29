from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from llm_config import parse_llm
from utils.state import ReviewState
from utils.parse_helper import parse_resume
from utils.prompt_helper import load_prompt


async def resume_agent(state: ReviewState) -> ReviewState:
    """Parse the resume file and extract key information."""
    if not state.resume or not state.resume.get("file"):
        state.has_error = True
        state.messages.append(AIMessage(content="Please upload your resume to proceed."))
        return state

    # Parse resume file
    parsed_resume = parse_resume(state.resume.get("file"))
    try:
        prompt = load_prompt("resume")
    except FileNotFoundError as e:
        state.has_error = True
        state.messages.append(AIMessage(content=str(e)))
        return state

    state.messages.append(SystemMessage(content=prompt))
    state.messages.append(HumanMessage(content=parsed_resume))

    # Invoke LLM to analyse resume
    llm_output = await parse_llm.ainvoke(state.messages)
    state.messages.append(AIMessage(content=llm_output.content))
    state.resume["analysis"] = str(llm_output.content)

    return state

async def jd_agent(state: ReviewState) -> ReviewState:
    """Parse the job description text and extract key information."""
    if not state.job or not state.job.get("desc"):
        state.has_error = True
        state.messages.append(AIMessage(content="Please provide the job description text to proceed."))
        return state

    # Generate messages for job description parsing
    try:
        prompt = load_prompt("job")
    except FileNotFoundError as e:
        state.has_error = True
        state.messages.append(AIMessage(content=str(e)))
        return state

    state.messages.append(SystemMessage(content=prompt))
    state.messages.append(HumanMessage(content=state.job["desc"]))

    # Invoke LLM to analyse job description
    llm_output = await parse_llm.ainvoke(state.messages)
    state.messages.append(AIMessage(content=llm_output.content))
    state.job["analysis"] = str(llm_output.content)

    return state