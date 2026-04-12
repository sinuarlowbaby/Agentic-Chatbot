from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
from db.database import engine, get_db
from db import models
from sqlalchemy.orm import Session
from typing import Optional
from app.core.session import get_session_id
from contextlib import asynccontextmanager
from api import chat

models.Base.metadata.create_all(bind=engine) # create all tables

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=3, max_length=255, description="Message to be sent to the chatbot")

app = FastAPI()
app.include_router(chat.router)

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Application startup")
    yield
    print("Application shutdown")


@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    print("Application startup in http://127.0.0.1:8000")
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)