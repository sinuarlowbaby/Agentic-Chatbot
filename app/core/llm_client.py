# from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI    
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# llm = ChatGroq(
#     model_name="llama-3.3-70b-versatile", 
#     groq_api_key=os.getenv("GROQ_API_KEY"),
#     temperature=0.7,
#     max_tokens=2000,
#     top_p=0.9,
#     frequency_penalty=0,
#     presence_penalty=0,
#     stop=None,
#     verbose=True,
#     streaming=True,

# )


llm = ChatOpenAI(
    model="gpt-4o",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.4,
    max_tokens=2000,
    streaming=True,
)
