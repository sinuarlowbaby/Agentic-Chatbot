from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.core.session import get_session_id
from app.db import models
import uuid
from app.core.llm_client import llm_client

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=3, max_length=255, description="Message to be sent to the chatbot")

@router.post("/chat")
def chat(request: ChatRequest, db: Session = Depends(get_db),session_id: str = Depends(get_session_id)):
    # db.add(models.Message(content=request.message, role="user", conversation_id=str(uuid.uuid4())))
    # db.add(models.Conversation(user_id=session_id, title=request.message))
    # db.add(models.AgentRun(conversation_id=str(uuid.uuid4()), message_id=str(uuid.uuid4()), status="completed", result=request.message))
    # db.add(models.ToolCall(run_id=str(uuid.uuid4()), tool_name="tool1", tool_input={"input": request.message}, tool_output=request.message, step_type="tool"))
    # db.commit()
    response = llm_client(user_input=request.message)
    print(response)



    return {"message": response}