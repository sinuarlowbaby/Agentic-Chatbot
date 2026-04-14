from app.agents.state import AgentState


def evaluator_node(state: AgentState) -> AgentState:
    current_step = state.get("current_step", 0)
    max_steps = state.get("max_steps", 5)
    intermediate_result = bool(str(state.get("intermediate_result", "")).strip())
    plan_steps = state.get("plan_steps", [])

    output = state.get("steps", [])[-1].get("final_response", "")
    has_result = bool(str(output).strip())
    has_error = bool(str(state.get("error", "")).strip())


    if has_error:
        # Hard stop — error or step budget exhausted
        done = True
        return {
            **state,
            "done": done,
            "current_step": current_step + 1,
            "final_response": state.get("error") or state.get("intermediate_result", "Agent could not complete the task."),
        }
    if current_step >= max_steps - 1:
        # Hard stop — step budget exhausted
        done = True
        return {
            **state,
            "done": done,
            "current_step": current_step + 1,
            "final_response": state.get("intermediate_result", "Agent could not complete the task."),
        }
    if current_step < len(plan_steps):
        # Hard stop — step budget exhausted
        done = False
        final_response = state.get("final_response", "")
    
    poor_result = len(str(output)) < 30
    if poor_result and current_step < max_steps - 1:
        # We have a usable result — mark done and surface it
        done = True
        final_response = state.get("intermediate_result", "")

    return {
        **state,
        "done": done,
        "current_step": current_step + 1,
        "final_response": final_response,
    }