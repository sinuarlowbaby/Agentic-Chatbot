from app.agents.state import AgentState
from app.tools.tools import web_search_tool, analyze_data_tool, summarize_data_tool



def executor_node(state: AgentState) -> AgentState:
    plan_steps = state.get("plan_steps", [])
    print("🛑plan_steps : ",plan_steps)
    current_step = state.get("current_step", 0)
    print("🛑current_step : ",current_step)

    # Pick the current plan step; fall back to the raw goal
    if plan_steps and current_step < len(plan_steps):
        step_def = plan_steps[current_step]
        print("🛑step_def : ",step_def)
        action = step_def.get("plan_step", "web_search")
        print("🛑action : ",action)
        query = step_def.get("query", state["goal"])
        print("🛑query : ",query)
        intermediate_result = step_def.get("intermediate_result", "")
        print("🛑intermediate_result : ",intermediate_result)
    else:
        action = "web_search"
        print("🛑action : ",action)
        query = state["goal"]
        print("🛑query : ",query)
        intermediate_result = ""
        print("🛑intermediate_result : ",intermediate_result)

    TOOLS = {
        "web_search": web_search_tool,
        "analyze_data": analyze_data_tool,
        "summarize_data": summarize_data_tool,
    }

    try:
        if action in TOOLS:
            if action == "analyze_data":
                result = TOOLS[action].invoke({"query": query, "intermediate_result": intermediate_result})
            else:
                result = TOOLS[action].invoke({"query": query})
        else:
            result = "Unknown action"
        output = result if isinstance(result, (dict, list)) else str(result)

    except Exception as e:
        print("🛑ERROR : ", repr(e))
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
        "intermediate_result": state["intermediate_result"] + "\n" + str(output),
        "done": (
            current_step >= len(plan_steps) - 1
            or "error" in str(output).lower()
            or len(str(output)) < 20
        ),
        "current_step": current_step,
    }