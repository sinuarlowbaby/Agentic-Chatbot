from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.core.session import get_session_id
from app.db import models
import uuid 
from app.core.llm_client import llm_client
from app.agents.graph import build_graph
from app.core.session import get_user_id


router = APIRouter(prefix="/api/v1/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=3, max_length=255, description="Message to be sent to the chatbot")


router = APIRouter()

graph = build_graph()


@router.post("/chat")
async def chat(
    message: str,
    user_id: str = Depends(get_user_id)
):
    initial_state = {
        "user_id": user_id,
        "conversation_id": "conv_1",
        "goal": message,
        "messages": [],
        "steps": [],
        "current_step": 0,
        "max_steps": 3,
        "done": False,
        "final_answer": ""
    }

    result = graph.invoke(initial_state)

    return {
        "response": result.get("intermediate_result", "No result")
    }


    return {"message": response}