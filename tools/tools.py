from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv
import os

load_dotenv()

@tool
def get_weather(city: str) -> str:
    """Get the weather of a city"""
    return f"The weather of {city} is sunny"