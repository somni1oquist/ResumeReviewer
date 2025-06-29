from langgraph.graph import StateGraph, START, END
from utils.state import ReviewState
from utils.router_helper import proceed_router
from nodes.chatbot import chatbot, adjunct
from nodes.analyser import resume_agent, jd_agent
from nodes.reviewer import review_agent


# Build graph
builder = StateGraph(ReviewState)
builder.add_node("chatbot", chatbot)
builder.add_node("adjunct", adjunct)
# Add agents
builder.add_node("jd_agent", jd_agent)
builder.add_node("resume_agent", resume_agent)
builder.add_node("review_agent", review_agent)
# Define edges

builder.add_edge(START, "chatbot")
# If no resume or job description is provided, return to chatbot, else proceed to both agents
builder.add_conditional_edges("chatbot", proceed_router, {
    "proceed": "adjunct",
    "chatbot": "chatbot",
    END: END
})

# Analysis stage
builder.add_edge("adjunct", "resume_agent")
builder.add_edge("adjunct", "jd_agent")
# If both agents are done, proceed to review stage
builder.add_edge("resume_agent", "review_agent")
builder.add_edge("jd_agent", "review_agent")

# Review stage
builder.add_edge("review_agent", END)

graph = builder.compile()

# Visualise the graph
if __name__ == "__main__":
    print(graph.get_graph().draw_mermaid())
