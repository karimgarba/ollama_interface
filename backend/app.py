"""
module: backend.app
description: This module contains the FastAPI application for the AI Assistant.
author: Karim Garba
date_created: 08-04-25
date_modified: 08-04-25
last_modified_by: Karim Garba
version: 0.1
"""
import os
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uuid
from dotenv import load_dotenv

from services.db_handler import DatabaseHandler
from services.ai_handler import AIHandler

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="AI Assistant API",
    description="API for interacting with the AI Assistant",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
db_path = os.getenv("DB_PATH", "data/assistant.db")
db_handler = DatabaseHandler(db_path=db_path)

# AI Handler
ai_handler = AIHandler(db_handler=db_handler)

# Pydantic models
class MessageRequest(BaseModel):
    prompt: str
    system_prompt: Optional[str] = None
    session_id: Optional[str] = None

class ModelRequest(BaseModel):
    model_name: str

class MemoryRequest(BaseModel):
    session_id: str
    name: str

class SessionResponse(BaseModel):
    session_id: str
    model: str
    created_at: str

class MessageResponse(BaseModel):
    role: str
    content: str
    created_at: str

# API Routes
@app.get("/")
async def root(request: Request):
    print(f"Request received at root: {request.client.host}")
    return {"status": "online", "message": "AI Assistant API is running"}

@app.get("/api/models")
async def get_models():
    """Get available AI models"""
    models = ai_handler.get_models()
    return {"models": models}

@app.post("/api/models/select")
async def select_model(request: ModelRequest):
    """Select an AI model"""
    try:
        ai_handler.set_model(request.model_name)
        return {"status": "success", "model": request.model_name}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/chat")
async def generate_response(request: MessageRequest):
    """Generate a response from the AI model"""
    print(f"Chat request received: {request}")
    try:
        # Ensure a model is selected
        if not ai_handler.current_model:
            raise HTTPException(status_code=400, detail="No model selected. Please select a model before generating a response.")
        
        # Set session if provided
        if request.session_id:
            ai_handler.set_session_id(request.session_id)
        
        # Generate response
        response = ai_handler.generate_response(request.prompt, request.system_prompt)
        
        return {
            "response": response,
            "session_id": ai_handler.current_session_id
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sessions")
async def get_sessions():
    """Get all chat sessions"""
    try:
        sessions = ai_handler.get_sessions()
        return {"sessions": sessions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str):
    """Get a specific chat session"""
    try:
        session = ai_handler.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Get messages for this session
        messages = db_handler.get_chat_history(session_id)
        
        return {
            "session": session,
            "messages": messages
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/sessions/clear")
async def clear_session():
    """Clear the current session"""
    try:
        ai_handler.clear_chat_history()
        return {
            "status": "success", 
            "session_id": ai_handler.current_session_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/memories")
async def create_memory(request: MemoryRequest):
    """Create a memory from a chat session"""
    try:
        db_handler.add_memory(request.session_id, request.name)
        return {"status": "success", "message": "Memory created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/memories")
async def get_memories():
    """Get all memories"""
    try:
        memories = db_handler.get_memories()
        return {"memories": memories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)