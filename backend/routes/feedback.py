from fastapi import APIRouter
from backend.chains.rapid_fire_feedback import generate_rapid_fire_feedback


router = APIRouter()


@router.post("/rapid-fire-feedback")
async def rapid_fire_feedback(input: dict):
    transcript = input.get("transcript", "")
    response = generate_rapid_fire_feedback(transcript)
    return {"feedback": response}


# Keep old endpoint for backwards compatibility
@router.post("/warm-feedback")
async def warm_feedback(input: dict):
    transcript = input.get("transcript", "")
    response = generate_rapid_fire_feedback(transcript)
    return {"feedback": response}
