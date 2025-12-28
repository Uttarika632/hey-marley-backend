from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from backend.chains.skill_profile import generate_skill_profile


router = APIRouter()


class SkillProfileRequest(BaseModel):
    rapid_fire_feedback: str
    word_bomb_feedback: str
    deep_dive_feedback: str


class SkillProfileResponse(BaseModel):
    skill_profile: str


@router.post("/skill-profile", response_model=SkillProfileResponse)
async def create_skill_profile(request: SkillProfileRequest):
    """Generate the final skill profile based on all three challenge feedbacks."""
    result = generate_skill_profile(
        rapid_fire_feedback=request.rapid_fire_feedback,
        word_bomb_feedback=request.word_bomb_feedback,
        deep_dive_feedback=request.deep_dive_feedback
    )
    return SkillProfileResponse(skill_profile=result)




