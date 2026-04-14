from langgraph.graph import StateGraph, END

from app.agents.state import AgentState
from app.agents.nodes.planner import planner_node
from app.agents.nodes.executor import executor_node
from app.agents.nodes.evaluator import evaluator_node


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner_node)
    graph.add_node("executor", executor_node)
    graph.add_node("evaluator", evaluator_node)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "executor")
    graph.add_edge("executor", "evaluator")

    def should_continue(state: AgentState) -> str:
        # Hard ceiling — prevents infinite loops even if evaluator has a bug
        if state["done"] or state["current_step"] >= state["max_steps"]:
            return END
        # Loop back to planner so a fresh plan can be generated for the next step
        return "planner"

    graph.add_conditional_edges("evaluator", should_continue)

    return graph.compile()