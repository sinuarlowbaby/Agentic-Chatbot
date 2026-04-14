from app.agents.state import AgentState
from app.tools.tools import web_search_tool, analyze_data_tool, summarize_data_tool



def executor_node(state: AgentState) -> AgentState:
    plan_steps = state.get("plan_steps", [])
    current_step = state.get("current_step", 0)

    # Pick the current plan step; fall back to the raw goal
    if plan_steps and current_step < len(plan_steps):
        step_def = plan_steps[current_step]
        action = step_def.get("plan_step", "web_search")
        query = step_def.get("query", state["goal"])
    else:
        action = "web_search"
        query = state["goal"]

    try:
        if action == "web_search":
            result = web_search_tool.invoke(query)
        elif action == "analyze_data":
            result = analyze_data_tool.invoke(query)
        elif action == "summarize_data":
            result = summarize_data_tool.invoke(query)
        else:
            result = "Unknown action"
        output = result.content

    except Exception as e:
        return {
            **state,
            "error": f"Tool execution failed: {e}",
            "done": True,
        }

    return {
        **state,
        "steps": state["steps"] + [{
            "type": "execution", 
            "step": current_step, 
            "action": action, 
            "query": query, 
            "output": output}],
        "intermediate_result": output,
        "done": current_step >= len(plan_steps) - 1,
        "current_step": current_step + 1,
    }