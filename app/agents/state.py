from typing import TypedDict, List, Dict, Any

class AgentState(TypedDict):
    user_id: str
    conversation_id: str
    goal: str
    messages: List[Dict[str, str]]
    steps: List[Dict[str, Any]]
    tools: List[Dict[str, Any]]
    current_step: int = 0
    max_steps: int = 5
    completed: bool = False
    error: str = ""
    final_response: str = ""
    

    
    

