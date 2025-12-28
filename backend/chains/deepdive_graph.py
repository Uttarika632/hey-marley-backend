from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI


# -----------------------------
# 1. Define Conversation State
# -----------------------------
class DeepDiveState(TypedDict):
    turn: int                      # Which turn (0,1,2)
    questions: List[str]           # All questions asked so far
    answers: List[str]             # All user answers so far
    ai_message: Optional[str]      # Message Marley sends to user
    summary: Optional[str]         # Final summary + evaluation


# Model used to generate follow-up questions & summary
llm = ChatOpenAI(model="gpt-4", temperature=0.7)


# -----------------------------
# 2. Node: Ask a Question
# -----------------------------
def ask_question(state: DeepDiveState):
    turn = state["turn"]
    question = state["questions"][turn]

    return {
        **state,
        "ai_message": question   # This is what frontend shows
    }


# -----------------------------
# 3. Node: Wait for answer (pause)
# -----------------------------
def wait_for_answer(state: DeepDiveState):
    # This node does nothing except pause graph
    return state


# -----------------------------
# 4. Node: Generate Follow-up Question
# -----------------------------
def generate_followup(state: DeepDiveState):
    last_answer = state["answers"][-1]

    messages = [
        {"role": "system",
         "content": "You are Marley, a warm, curious teen coach. "
                    "Your job is to ask thoughtful, simple follow-up questions "
                    "based only on the user's last response. Keep it conversational."},
        {"role": "user", "content": last_answer}
    ]

    follow_up = llm.invoke(messages).content

    state["questions"].append(follow_up)

    return {
        **state,
        "ai_message": follow_up
    }


# -----------------------------
# 5. Node: Final Summary
# -----------------------------
def summarize_conversation(state: DeepDiveState):
    conversation_text = ""

    for q, a in zip(state["questions"], state["answers"]):
        conversation_text += f"Q: {q}\nA: {a}\n\n"

    messages = [
        {"role": "system",
         "content": "You are Marley, a friendly communication coach. "
                    "Summarize the teen's thinking warmly. "
                    "NO scores. NO criticism. Just a kind summary."},
        {"role": "user", "content": conversation_text}
    ]

    summary = llm.invoke(messages).content

    state["summary"] = summary

    return {
        **state,
        "ai_message": summary
    }


# -----------------------------
# 6. Build the Graph
# -----------------------------
graph = StateGraph(DeepDiveState)

# Add nodes
graph.add_node("ask", ask_question)
graph.add_node("wait", wait_for_answer)
graph.add_node("followup", generate_followup)
graph.add_node("summary", summarize_conversation)

# Set entry
graph.set_entry_point("ask")

# DEFINE EDGES:
# ask → wait
graph.add_edge("ask", "wait")


# wait → followup (if turn < 2), otherwise → summary
def route_after_answer(state: DeepDiveState):
    if state["turn"] < 2:
        return "followup"
    return "summary"


graph.add_conditional_edges(
    "wait",
    route_after_answer,
    {
        "followup": "followup",
        "summary": "summary"
    }
)

# followup → ask (ask next question)
graph.add_edge("followup", "ask")

# summary → END
graph.add_edge("summary", END)

# Compile graph
deepdive_graph = graph.compile()





