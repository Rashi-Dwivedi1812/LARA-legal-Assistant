import os
import uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# --- Import agent router ---
from agent.router import route_query
from db import (
    save_thread,
    save_message,
    get_user_threads,
    get_thread_messages,
    delete_thread,
)

# ============================
# 1. FASTAPI INITIALIZATION
# ============================

app = FastAPI(
    title="L.A.R.A Backend API",
    description="API for the Legal Analysis & Research Assistant",
    version="1.0.0",
)

# ============================
# 2. CORS CONFIGURATION
# ============================

# NOTE:
# - "*" is acceptable for demo/resume deployment
# - Lock this down later for production

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================
# 3. PYDANTIC MODELS
# ============================

class QueryRequest(BaseModel):
    user_query: str
    role: str
    thread_id: str


class QueryResponse(BaseModel):
    final_analysis: str
    thread_id: str


class ChatHistoryRequest(BaseModel):
    user_id: str


class ThreadMessagesRequest(BaseModel):
    thread_id: str


class SaveThreadRequest(BaseModel):
    user_id: str
    thread_id: str
    title: str | None = None


# ============================
# 4. API ENDPOINTS
# ============================

@app.get("/")
def health_check():
    return {"status": "L.A.R.A backend is running"}

@app.post("/process_query", response_model=QueryResponse)
async def process_legal_query(request: QueryRequest):
    try:
        result = route_query(
            role=request.role,
            user_query=request.user_query,
            thread_id=request.thread_id,
        )

        final_analysis = result.get(
            "final_analysis",
            "No analysis could be generated.",
        )

        # Save chat history
        save_message(request.thread_id, "user", request.user_query)
        save_message(request.thread_id, "bot", final_analysis)

        return QueryResponse(
            final_analysis=final_analysis,
            thread_id=request.thread_id,
        )

    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/get_chat_history")
async def get_chat_history(request: ChatHistoryRequest):
    try:
        return {"threads": get_user_threads(request.user_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch chat history")


@app.post("/get_thread_messages")
async def get_thread_messages_endpoint(request: ThreadMessagesRequest):
    try:
        return {"messages": get_thread_messages(request.thread_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch messages")


@app.post("/save_thread")
async def save_thread_endpoint(request: SaveThreadRequest):
    try:
        save_thread(request.user_id, request.thread_id, request.title)
        return {"message": "Thread saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to save thread")


@app.delete("/delete_thread/{thread_id}")
async def delete_thread_endpoint(thread_id: str):
    try:
        delete_thread(thread_id)
        return {"message": "Thread deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to delete thread")


# ============================
# 5. ENTRY POINT (LOCAL ONLY)
# ============================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
    )
