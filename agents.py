from langchain_openai import ChatOpenAI
from state import AgentState

llm = ChatOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
    model="llama3.2:3b",
    temperature=0
)

def reader_node(state: AgentState):
    print("🔍 [Reader] Analyzing...")
    res = llm.invoke(f"Is this post AGGRESSIVE or SAFE? Post: {state['post']}")
    return {"sentiment": res.content.strip().upper()}

def policy_node(state: AgentState):
    print("⚖️ [Policy] Checking rules...")
    with open("guidelines.txt", "r") as f:
        rules = f.read()
    res = llm.invoke(f"Rules: {rules}\nPost: {state['post']}\nWhich rule applies?")
    return {"relevant_rule": res.content}

def judge_node(state: AgentState):
    from database import save_moderation_log
    print("👨‍⚖️ [Judge] Deciding...")
    rule = state.get('relevant_rule', "No specific rule.")
    res = llm.invoke(f"Post: {state['post']}\nRule: {rule}\nDecision: APPROVE or REJECT?")
    
    save_moderation_log(state['post'], state['sentiment'], res.content)
    return {"decision": res.content}