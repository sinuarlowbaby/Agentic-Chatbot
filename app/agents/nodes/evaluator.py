from app.agents.state import AgentState

def evaluator_node(state: AgentState) -> AgentState:
    current_step = state.get("current_step", 0)
    max_steps = state.get("max_steps", 5)
    plan_steps = state.get("plan_steps", [])
    steps = state.get("steps", [])

    output = steps[-1].get("output", "") if steps else ""
    error = state.get("error", "")

    has_error = bool(str(error).strip())
    has_output = bool(str(output).strip())

    # 🔴 1. Error → stop immediately
    if has_error:
        return {
            **state,
            "done": True,
            "final_response": error,
            "current_step": current_step + 1,
        }

    # 🔴 2. Max steps → stop
    if current_step >= max_steps - 1:
        print("➡️final response : ",state.get("intermediate_result", "Max steps reached"))
        return {
            **state,
            "done": True,
            "final_response": state.get("intermediate_result", "Max steps reached"),
            "current_step": current_step + 1,
        }

    # 🟡 3. Continue if plan not finished
    if current_step < len(plan_steps):
        return {
            **state,
            "done": False,
            "current_step": current_step + 1,
        }

    # 🟡 4. Quality check
    poor_result = len(str(output)) < 30

    if poor_result:
        return {
            **state,
            "done": False,
            "current_step": current_step + 1,
            "final_response": "Result too weak, continuing...",
        }

    # ✅ 5. Success → stop
    return {
        **state,
        "done": True,
        "final_response": output,
        "current_step": current_step + 1,
    }