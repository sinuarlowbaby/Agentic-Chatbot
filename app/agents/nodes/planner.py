import json
from typing import List
from app.agents.state import AgentState
from app.core.llm_client import llm
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
    print("\n[PLANNER] Goal:", goal)

    parser = PydanticOutputParser(pydantic_object=PlanOutput)
    prompt = PromptTemplate(
        input_variables=["goal", "format_instructions"],
        template="""
            You are a master planner. Given a user goal, break it into a numbered list of
            concrete steps.
            You MUST ONLY use the following actions:
                - web_search
                - analyze_data
                - summarize_data
            Do NOT invent new actions.
            Goal: {goal}
            Instructions: {format_instructions}
            Respond ONLY with valid JSON in this format:
            {{"plan_steps": [{{"step": 1, "plan_step": "web_search", "query": "example query"}}]}}
            No explanation, no markdown - raw JSON only.
    """)
    format_instructions = parser.get_format_instructions()
    final_prompt = prompt.format(goal=goal, format_instructions=format_instructions)
    # print("🛑final_prompt : ",final_prompt)
    response = llm.invoke(final_prompt).content
    print("🛑response : ",response)
    try:
        parsed_response = parser.parse(response)
        print("🛑parsed_response : ",parsed_response)
        plan_steps = [step.model_dump() for step in parsed_response.plan_steps]
        print("🛑plan_steps : ",plan_steps)
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