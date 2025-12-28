from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from backend.chains.action_plan import generate_action_plan
from backend.chains.action_plan_v2 import generate_personalized_action_plan


router = APIRouter()


class ActionPlanV2Request(BaseModel):
    student_goal: str
    target_date: str
    skill_profile: str  # JSON string of skill profile


class ActionPlanV2Response(BaseModel):
    action_plan: str


@router.post("/action-plan-v2", response_model=ActionPlanV2Response)
async def action_plan_v2(request: ActionPlanV2Request):
    """Generate a personalized 3-week action plan based on goal and skill profile."""
    plan = generate_personalized_action_plan(
        student_goal=request.student_goal,
        target_date=request.target_date,
        skill_profile=request.skill_profile
    )
    return ActionPlanV2Response(action_plan=plan)


# Legacy endpoint for backwards compatibility
@router.post("/action-plan")
async def action_plan(data: dict):
    """Generate a personalized 3-week action plan based on evaluation (legacy)."""
    evaluation_json = data["evaluation_json"]
    plan = generate_action_plan(evaluation_json)
    return {"action_plan": plan}
