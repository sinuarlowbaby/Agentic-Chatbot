from sqlalchemy import Column, Integer, String, TIMESTAMP, func
import uuid
from sqlalchemy.dialects.postgresql import JSONB
from app.db.database import Base



class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, index=True)
    title = Column(String)
    created_at = Column(TIMESTAMP, default=func.now())

class Message(Base):
    __tablename__ = "messages"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String, index=True)
    role = Column(String)
    content = Column(String)
    meta_data = Column("metadata", JSONB)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

class AgentRun(Base):
    __tablename__ = "agent_runs"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String, index=True)
    message_id = Column(String, index=True)
    status = Column(String)
    result = Column(String)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

class ToolCall(Base):
    __tablename__ = "tool_calls"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    run_id = Column(String, index=True)
    tool_name = Column(String)
    tool_input = Column(JSONB)
    tool_output = Column(String)
    step_type = Column(String)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())
