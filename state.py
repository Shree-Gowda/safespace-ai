from typing import TypedDict

class AgentState(TypedDict):
    post: str
    sentiment: str
    relevant_rule: str
    decision: str