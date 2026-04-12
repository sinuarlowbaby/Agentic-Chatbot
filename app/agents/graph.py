from langgraph.graph import StateGraph, END

from app.agents.state import AgentState
from app.agents.nodes.planner import planner_node
from app.agents.nodes.executor import executor_node
from app.agents.nodes.evaluator import evaluator_node


def build_graph():

    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("planner", planner_node)
    graph.add_node("executor", executor_node)
    graph.add_node("evaluator", evaluator_node)

    # Flow
    graph.set_entry_point("planner")

    graph.add_edge("planner", "executor")
    graph.add_edge("executor", "evaluator")

    # Conditional loop
    def should_continue(state):
        return "executor" if not state["done"] else END

    graph.add_conditional_edges(
        "evaluator",
        should_continue
    )

    return graph.compile()