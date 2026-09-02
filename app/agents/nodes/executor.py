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
        intermediate_result = state.get("intermediate_result", "")
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
        if isinstance(result, dict) and "results" in result:
            output = "\n".join([r["content"] for r in result["results"][:3]])
        else:
            output = str(result)

    except Exception as e:
        print("🛑ERROR : ", repr(e))
        return {
            **state,
            "error": f"Tool execution failed: {e}",
            "done": True,
        }
    print("\n===== DATA FLOW =====")
    print("Prev result:", state.get("intermediate_result"))
    print("New output:", output)

    return {
        **state,
        "steps": state["steps"] + [{
            "type": "execution", 
            "step": current_step + 1, 
            "action": action, 
            "query": query, 
            "output": output}],
        "intermediate_result": output,
        "done": False,
        "current_step": current_step,
    }