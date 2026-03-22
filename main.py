import os
from typing import TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

load_dotenv()

# --- 1. THE STATE DEFINITION ---
# This is the "folder" that gets passed from agent to agent
class AgentState(TypedDict):
    post: str
    sentiment: str
    relevant_rule: str
    decision: str

# --- 2. THE MODEL (Ollama Local) ---
# We use ChatOpenAI because Ollama provides an OpenAI-compatible local API
llm = ChatOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama", # Required but ignored by Ollama
    model="llama3.2:3b",
    temperature=0
)

# --- 3. THE AGENTS (Nodes) ---

def reader_agent(state: AgentState):
    print("🔍 [Agent 1: Reader] Analyzing intent...")
    # We tell the AI to be VERY specific
    prompt = (
        f"Analyze this post: '{state['post']}'\n"
        "If it is mean, rude, or aggressive, output ONLY the word: AGGRESSIVE\n"
        "Otherwise, output ONLY the word: SAFE"
    )
    response = llm.invoke(prompt)
    # .strip() removes any accidental spaces or newlines
    sentiment_result = response.content.strip().upper()
    return {"sentiment": sentiment_result}

def route_post(state: AgentState):
    # Now we check for the exact word
    if "AGGRESSIVE" in state["sentiment"]:
        print("🚩 [Router]: Sentiment is Aggressive. Sending to Policy Expert.")
        return "policy"
    else:
        print("✅ [Router]: Sentiment is Safe. Skipping to Judge.")
        return "judge"

def policy_agent(state: AgentState):
    print("⚖️ [Agent 2: Policy Expert] Checking guidelines...")
    # Read the local rulebook
    with open("guidelines.txt", "r") as f:
        rules = f.read()
    
    prompt = f"Rules: {rules}\n\nPost: {state['post']}\nWhich rule is most relevant here? Quote the rule name."
    response = llm.invoke(prompt)
    return {"relevant_rule": response.content}

def judge_agent(state: AgentState):
    print("👨‍⚖️ [Agent 3: Judge] Making final verdict...")
    
    # Use .get() or check if the key exists to avoid the KeyError
    rule_text = state.get('relevant_rule', "No specific rule violation detected (Post marked as SAFE).")
    
    prompt = (
        f"Post: {state['post']}\n"
        f"Sentiment: {state['sentiment']}\n"
        f"Rule Analysis: {rule_text}\n\n"
        "Based on the above, should this post be APPROVED, FLAG_USER, or REJECTED? "
        "Provide a 1-sentence reason."
    )
    response = llm.invoke(prompt)
    return {"decision": response.content}

# --- 4. THE GRAPH (Updated with Conditional Routing) ---
workflow = StateGraph(AgentState)

workflow.add_node("reader", reader_agent)
workflow.add_node("policy", policy_agent)
workflow.add_node("judge", judge_agent)

# Start with the Reader
workflow.add_edge(START, "reader")

# NEW: Add the Conditional Edge
workflow.add_conditional_edges(
    "reader",           # Where the decision starts
    route_post,         # The function that makes the decision
    {
        "policy": "policy", # Map the string 'policy' to the node 'policy'
        "judge": "judge"    # Map the string 'judge' to the node 'judge'
    }
)

# Connect the rest
workflow.add_edge("policy", "judge")
workflow.add_edge("judge", END)

app = workflow.compile()

# --- 5. EXECUTION ---
if __name__ == "__main__":
    test_post = "Great job on the code, keep it up!"
    print(f"\n--- PROCESSING POST: '{test_post}' ---\n")
    
    final_output = app.invoke({"post": test_post})
    
    print("\n" + "="*30)
    print("FINAL SYSTEM DECISION:")
    print(final_output["decision"])
    print("="*30)