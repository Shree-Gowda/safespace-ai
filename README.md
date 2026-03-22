# 🛡️ SafeSpace: Multi-Agent AI Moderation Platform

A full-stack, modular AI moderation system that uses specialized agents to review social media content against custom community guidelines.

## 🚀 Tech Stack
- **AI Orchestration:** LangGraph (Python)
- **Model:** Llama 3.2 via Ollama (Local)
- **Backend:** FastAPI, MySQL
- **Frontend:** React (Vite), Axios
- **Knowledge Base:** RAG-lite (Retrieval Augmented Generation)

## 🏗️ Architecture
1. **Reader Agent:** Analyzes sentiment and intent.
2. **Policy Agent:** Cross-references posts with a `guidelines.txt` using RAG logic.
3. **Judge Agent:** Makes the final decision and persists logs to MySQL.
4. **Router:** Optimizes latency by skipping policy checks for "Safe" content.

## 🛠️ How to Run
1. Start Ollama: `ollama run llama3.2:3b`
2. Run Backend: `python api.py`
3. Run Frontend: `npm run dev` (inside /safespace-frontend)
