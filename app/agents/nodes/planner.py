import json
from typing import List
from app.agents.state import AgentState
from app.core.llm_client import llm_client
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

class PlanStep(BaseModel):
    step: int = Field(..., description="Step number")
    plan_step: str = Field(..., description="Action to take")
    query: str = Field(..., description="Query to use")

class PlanOutput(BaseModel):
    plan_steps: List[PlanStep] = Field(..., description="List of plan steps")

def planner_node(state: AgentState) -> AgentState:
    goal = state["goal"]

    prompt = PromptTemplate(
        input_variables=["goal"],
        template="""
            
                You are a master planner. Given a user goal, break it into a numbered list of
                concrete steps.
                Goal :{goal}
                instructions :{format_instructions}
                Respond ONLY with valid JSON in this format:
                {
                "plan_steps": [
                    {"step": int, "plan_step": str, "query": str}
                ]
                }
                No explanation, no markdown — raw JSON only.
                Example: [{"step":1,"plan_step":"web_search","query":"latest AI news 2026"}]
            
    """)
    format_instructions = PydanticOutputParser(PlanOutput).get_format_instructions()
    final_prompt = prompt.format(goal=goal, format_instructions=format_instructions)
    response = llm_client(final_prompt)
    print("🛑response : ",response)
    try:
        parsed_response = PydanticOutputParser(PlanOutput).parse(response)
        plan_steps = [step.dict() for step in parsed_response.plan_steps]
    except Exception as e:
        return {
            **state,
            "error": f"Failed to parse plan: {str(e)}",
            "done": True,
        }

    
    return {
        **state,
        "plan_steps": plan_steps,
        "steps": state["steps"] + [{"type": "plan", "content": plan_steps}],
        "current_step": 0,
    }