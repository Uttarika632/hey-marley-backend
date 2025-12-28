from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from backend.chains.rapid_fire_prompts import generate_rapid_fire_prompts


class RapidFireProfile(BaseModel):
    age: str
    city: str
    country: str
    academic_interests: List[str]
    personal_interests: List[str]
    communication_goals: List[str]
    emotional_needs: List[str]
    short_term_goal: str


router = APIRouter()


@router.post("/rapid-fire/start")
async def start_rapid_fire(profile: RapidFireProfile):
    prompts = generate_rapid_fire_prompts(
        age=profile.age,
        city=profile.city,
        country=profile.country,
        academic_interests=profile.academic_interests,
        personal_interests=profile.personal_interests,
        communication_goals=profile.communication_goals,
        emotional_needs=profile.emotional_needs,
        short_term_goal=profile.short_term_goal,
    )
    return {"prompts": prompts}





