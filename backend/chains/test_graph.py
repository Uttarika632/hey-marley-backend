from langgraph.graph import StateGraph, END

def step1(state):
    state["message"] += " world"
    return state

graph = StateGraph(dict)
graph.add_node("step1", step1)
graph.set_entry_point("step1")
graph.set_finish_point("step1")

compiled = graph.compile()

result = compiled.invoke({"message": "Hello"})
print(result)

