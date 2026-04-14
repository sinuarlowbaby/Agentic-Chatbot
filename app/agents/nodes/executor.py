from app.agents.state import AgentState
from app.tools.tools import web_search_tool


def executor_node(state: AgentState) -> AgentState:
    plan_steps = state.get("plan_steps", [])
    current_step = state.get("current_step", 0)

    # Pick the current plan step; fall back to the raw goal
    if plan_steps and current_step < len(plan_steps):
        step_def = plan_steps[current_step]
        query = step_def.get("query", state["goal"])
    else:
        query = state["goal"]

    try:
        result = web_search_tool.invoke(query)
        output = str(result)
    except Exception as e:
        return {
            **state,
            "error": f"Tool execution failed: {e}",
            "done": True,
        }

    return {
        **state,
        "steps": state["steps"] + [{"type": "execution", "step": current_step, "output": output}],
        "intermediate_result": output,
    }