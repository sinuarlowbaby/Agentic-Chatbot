from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import JSONB
from db.database import Base



class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    title = Column(String)
    created_at = Column(TIMESTAMP, default=func.now())

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, index=True)
    role = Column(String)
    content = Column(String)
    meta_data = Column("metadata", JSONB)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

class AgentRun(Base):
    __tablename__ = "agent_runs"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, index=True)
    message_id = Column(Integer, index=True)
    status = Column(String)
    result = Column(String)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

class ToolCall(Base):
    __tablename__ = "tool_calls"
    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, index=True)
    tool_name = Column(String)
    tool_input = Column(JSONB)
    tool_output = Column(String)
    step_type = Column(String)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())
