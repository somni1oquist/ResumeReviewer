import os
import time
import streamlit as st
from graph_config import graph
from utils.state import ReviewState
from langchain_core.messages import AIMessage, SystemMessage


@st.dialog("Review Result", width="large")
def review_dialog(state: ReviewState):
    result = state.report
    if not result:
        result = state.messages[-1].content if state.messages else "No review available."
    st.write(result)
    like, dislike = st.columns(2)
    if like.button("Like", icon=":material/thumb_up:", use_container_width=True):
        state.accepted = True
        st.toast("Thank you for liking the review.", icon=":material/check_circle:")
        time.sleep(2)  # Delay to allow toast to show
        st.rerun()
    if dislike.button("Dislike", icon=":material/thumb_down:", use_container_width=True):
        state.accepted = False
        st.toast("Thank you for your feedback.", icon=":material/close:")
        time.sleep(2)  # Delay to allow toast to show
        st.rerun()

# Visualise layout and elements
st.title("Resume Reviewer")
st.caption("Upload your resume and enter the job description, then get a detailed review.")

with st.form("review_form", clear_on_submit=True):
    # Text area for job description input
    jd = st.text_area(
        "Job Description",
        placeholder="Paste the job description here...",
        key="job_description",
        height=200
    )
    # File uploader for resume
    resume = st.file_uploader(
        "Upload Your Resume",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=False,
        help="Upload your resume file (PDF, DOCX, or TXT format).",
        width="stretch",
        key="resume_uploader"
    )
    # Submit button
    submit_button = st.form_submit_button("Submit",
        icon=":material/done_all:",
        use_container_width=True
    )


# Initialise for chat history if not already present 
if "review_state" not in st.session_state:
    st.session_state["review_state"] = ReviewState(
        messages=[
            SystemMessage(content=os.getenv("INIT_PROMPT", "Please provide your resume and job description."))
        ],
        resume={},
        job={},
        report="",
        accepted=False
    )

state: ReviewState = st.session_state["review_state"]
# Display chat history without system prompts
# if not state.report:
#     prompts = [msg for msg in state.messages if isinstance(msg, AIMessage)]
#     for msg in prompts:
#         st.chat_message("assistant").write(msg.content)

# If the form is submitted, process the inputs
if submit_button:
    # Input for user prompt
    if jd and resume:
        state.job = {"desc": jd.strip()}
        state.resume = {"file": resume}

        result = None
        with st.spinner("Processing...", show_time=True, width="stretch"):
            # Invoke graph
            import asyncio
            result = asyncio.run(graph.ainvoke(state))

        # Update session state
        st.session_state["review_state"] = ReviewState(**result)

        # Display latest assistant message
        review_dialog(st.session_state["review_state"])
        # messages = result["messages"]
        # if messages and isinstance(messages[-1], AIMessage):
        #     st.chat_message("assistant").write(messages[-1].content)
    else:
        check_resume = not resume
        check_job_ad = not jd
        check_both = check_resume and check_job_ad
        if check_both:
            st.toast("Please upload your resume and enter the job description to proceed.", icon=":material/warning:")
        elif check_resume:
            st.toast("Please upload your resume to proceed.", icon=":material/warning:")
        else:
            st.toast("Please enter the job description to proceed.", icon=":material/warning:")
