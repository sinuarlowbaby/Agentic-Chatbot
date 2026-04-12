def evaluator_node(state):
    step = state["current_step"]

    if step >= state["max_steps"]:
        state["done"] = True
    else:
        # simple logic (later: LLM-based evaluation)
        state["done"] = True

    state["current_step"] += 1

    return state