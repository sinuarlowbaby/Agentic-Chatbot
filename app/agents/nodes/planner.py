from app.agents.state import AgentState
from app.core.llm_client import llm_client

def planner_node(state: AgentState):
    goal = state["goal"]

    plan =f"""
    You are a master planner. Your goal is to create a step-by-step plan to achieve the following goal:
    {goal}
    
    Please create a step-by-step plan to achieve the goal.
    """
    response = llm_client(plan)
    state["steps"].append({"type": "plan", "content": response})
    state["current_step"] = 1
    return state