from app.agents.state import AgentState


def evaluator_node(state: AgentState) -> AgentState:
    current_step = state.get("current_step", 0)
    max_steps = state.get("max_steps", 5)
    has_result = bool(str(state.get("intermediate_result", "")).strip())
    has_error = bool(str(state.get("error", "")).strip())

    if has_error or current_step >= max_steps - 1:
        # Hard stop — error or step budget exhausted
        done = True
        final_response = (
            state.get("error") or state.get("intermediate_result", "Agent could not complete the task.")
        )
    elif has_result:
        # We have a usable result — mark done and surface it
        done = True
        final_response = state.get("intermediate_result", "")
    else:
        # No result yet and budget remaining — loop back
        done = False
        final_response = state.get("final_response", "")

    return {
        **state,
        "done": done,
        "current_step": current_step + 1,
        "final_response": final_response,
    }