from typing import TypedDict, List, Dict, Any
from app.agents.state import AgentState
from app.tools.tools import web_search_tool
from app.core.llm_client import llm_client

def executor_node(state):
    step_num = state["current_step"]

    # Simple logic (you can upgrade later with LLM tool selection)
    query = state["goal"]

    results = search_tool(query)
    content = scrape_tool(results)
    summary = summarize_tool(content)

    state["steps"].append({
        "type": "execution",
        "output": summary
    })

    state["intermediate_result"] = summary

    return state