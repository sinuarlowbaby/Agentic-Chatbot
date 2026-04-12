from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()
def llm_client(user_input: str):
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile", 
        groq_api_key=os.getenv("GROQ_API_KEY"))

    response = llm.invoke(user_input)
    print(response.content)
    return response.content
