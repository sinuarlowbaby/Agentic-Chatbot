from typing import TypedDict, List, Dict, Any

class AgentState(TypedDict):
    user_id: str
    conversation_id: str
    goal: str
    messages: List[Dict[str, str]]
    steps: List[Dict[str, Any]]
    tools: List[Dict[str, Any]]
    current_step: int
    max_steps: int
    completed: bool
    error: str
    final_response: str
    

    
    

