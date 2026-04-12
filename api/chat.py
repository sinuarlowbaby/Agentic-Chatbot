from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from db.database import get_db
from sqlalchemy.orm import Session
from typing import Optional
from app.core.session import get_session_id

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=3, max_length=255, description="Message to be sent to the chatbot")

@router.post("/chat")
def chat(request: ChatRequest, db: Session = Depends(get_db),session_id: str = Depends(get_session_id)):
    print(request.message)
    print(session_id)
    print(db)

    return {"message": request.message}