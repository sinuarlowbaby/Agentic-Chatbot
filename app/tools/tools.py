from langchain.tools import tool
from langchain_tavily import TavilySearch
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from app.core.llm_client import llm
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field

class AnalyzeDataInput(BaseModel):
    summary: str = Field(..., description="Summary of the data")
    key_findings: str = Field(..., description="Key findings from the data")
    recommendations: str = Field(..., description="Recommendations based on the data")
    confidence: float = Field(..., description="Confidence score between 0 and 1")

class SummarizeDataInput(BaseModel):
    summary: str = Field(..., description="Summary of the data")
    key_findings: str = Field(..., description="Key findings from the data")
    recommendations: str = Field(..., description="Recommendations based on the data")
    confidence: float = Field(..., description="Confidence score between 0 and 1")


load_dotenv()


def _get_tavily() -> TavilySearch:
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise EnvironmentError("TAVILY_API_KEY is not set in environment variables")
    return TavilySearch(
        tavily_api_key=api_key,
        max_results=3,
        include_raw_content=True,
    )


@tool
def web_search_tool(query: str) -> str:
    """Search the web for up-to-date information about a given query."""
    tavily = _get_tavily()
    results = tavily.invoke(query)
    return results

@tool
def analyze_data_tool(query: str,intermediate_result: str = "") -> dict:
    """Analyze the data for a given query."""
    parser = PydanticOutputParser(AnalyzeDataInput)
    prompt = PromptTemplate(
        input_variables=["query", "intermediate_result", "analysis_type", "format_instructions"],
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        },
        template="""
        Act as a data analyst and data scientist.
        Analyze the following data for a given query:
        {query}
        previous intermediate result : {intermediate_result}
        analysis_type : {analysis_type}
        Respond ONLY with valid JSON in this format:
        format : {format_instructions}
        """
    )

    final_prompt = prompt.format(query=query,intermediate_result=intermediate_result,analysis_type="general")

    chain = prompt | llm | PydanticOutputParser(AnalyzeDataInput)
    response = chain.invoke(final_prompt)
    try:
        parsed_response = PydanticOutputParser(AnalyzeDataInput).parse(response)
        return parsed_response.dict()

    except Exception as e:
        return {
            "error": f"Failed to parse analyze data: {str(e)}",
            "done": True,
        }

@tool
def summarize_data_tool(query: str) -> dict:
    """Summarize the data for a given query."""
    parser = PydanticOutputParser(SummarizeDataInput)
    prompt = PromptTemplate(
        input_variables=["query", "format_instructions"],
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        },
        template="""
        Act as a summarizer.
        Summarize the following data for a given query:
        {query}
        Respond ONLY with valid JSON in this format:
        format : {format_instructions}
        """
    )

    final_prompt = prompt.format(query=query)

    chain = prompt | llm | PydanticOutputParser(SummarizeDataInput)
    response = chain.invoke(final_prompt)
    try:
        parsed_response = PydanticOutputParser(SummarizeDataInput).parse(response)
        return parsed_response.dict()

    except Exception as e:
        return {
            "error": f"Failed to parse summarize data: {str(e)}",
            "done": True,
        }

if __name__ == "__main__":
    print(web_search_tool.invoke("what is ollama"))