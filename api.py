from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from main import app as agent_graph # Imports your LangGraph from main.py
import os
from dotenv import load_dotenv

load_dotenv()



server = FastAPI()

# --- STEP 1: FIX CORS (Crucial for React) ---
server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

class PostRequest(BaseModel):
    text: str

# --- STEP 2: MODERATE ENDPOINT ---
@server.post("/moderate")
async def moderate_post(request: PostRequest):
    # This runs your Python Agents
    result = await agent_graph.ainvoke({"post": request.text})
    return result

# --- STEP 3: LOGS ENDPOINT ---
@server.get("/logs")
async def get_logs():
    connection = mysql.connector.connect(
        host="localhost", user="root", password = os.getenv("MYSQL_PASSWORD"), database="safespace_db"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM moderation_logs ORDER BY created_at DESC")
    logs = cursor.fetchall()
    cursor.close()
    connection.close()
    return logs

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(server, host="0.0.0.0", port=8000)