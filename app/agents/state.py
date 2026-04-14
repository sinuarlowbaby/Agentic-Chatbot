from typing import TypedDict, List, Dict, Any
from typing_extensions import NotRequired


class AgentState(TypedDict):
    user_id: str
    conversation_id: str
    goal: str
    messages: List[Dict[str, str]]
    steps: List[Dict[str, Any]]
    plan_steps: NotRequired[List[Dict[str, Any]]]
    tools: List[Dict[str, Any]]
    current_step: int
    max_steps: int
    done: bool
    error: NotRequired[str]
    final_response: NotRequired[str]
    intermediate_result: NotRequired[str]