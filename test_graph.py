import asyncio
from app.agents.graph import build_graph
import uuid

async def test():
    graph = build_graph()
    initial_state = {
        "user_id": "test_user",
        "conversation_id": "test_conv",
        "goal": "Claude AI achievements 2026",
        "messages": [],
        "steps": [],
        "tools": [],
        "current_step": 0,
        "max_steps": 3,
        "done": False,
        "error": "",
        "final_response": "",
        "intermediate_result": "",
        "plan_steps": [],
    }
    print("Invoking graph...")
    result = graph.invoke(initial_state)
    print("Graph Result:", result)

if __name__ == "__main__":
    asyncio.run(test())
