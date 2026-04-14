from langchain.tools import tool
from langchain_tavily import TavilySearch
from dotenv import load_dotenv
import os

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


if __name__ == "__main__":
    print(web_search_tool.invoke("what is ollama"))