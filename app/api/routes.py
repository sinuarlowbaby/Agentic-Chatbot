import uuid
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.core.session import get_session_id
from app.agents.graph import build_graph


router = APIRouter(prefix="/api/v1/chat", tags=["chat"])

graph = build_graph()


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=3, max_length=255, description="Message to send to the agent")


@router.post("/")
async def chat(body: ChatRequest, user_id: str = Depends(get_session_id)):
    initial_state = {
        "user_id": user_id,
        "conversation_id": str(uuid.uuid4()),
        "goal": body.message,
        "messages": [],
        "steps": [],
        "tools": [],
        "current_step": 0,
        "max_steps": 3,
        "done": False,
        "error": "",
        "final_response": "",
        "intermediate_result": "",
        "plan_steps": [],
    }

    try:
        result = graph.invoke(initial_state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent execution failed: {e}")

    if result.get("error"):
        return {
            "response": f"Agent encountered an issue: {result['error']}",
            "conversation_id": result.get("conversation_id"),
            "steps_taken": result.get("current_step", 0),
        }

    return {
        "response": result.get("final_response") or result.get("intermediate_result", "No result"),
        "conversation_id": result.get("conversation_id"),
        "steps_taken": result.get("current_step", 0),
    }