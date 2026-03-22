from langgraph.graph import StateGraph, START, END
from state import AgentState
from agents import reader_node, policy_node, judge_node

def router_logic(state: AgentState):
    return "policy" if "AGGRESSIVE" in state["sentiment"] else "judge"

workflow = StateGraph(AgentState)

workflow.add_node("reader", reader_node)
workflow.add_node("policy", policy_node)
workflow.add_node("judge", judge_node)

workflow.add_edge(START, "reader")
workflow.add_conditional_edges("reader", router_logic, {"policy": "policy", "judge": "judge"})
workflow.add_edge("policy", "judge")
workflow.add_edge("judge", END)

app = workflow.compile()