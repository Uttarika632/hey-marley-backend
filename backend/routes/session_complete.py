from fastapi import APIRouter
from chains.full_session_evaluator import evaluate_full_session


router = APIRouter()


@router.post("/complete-session")
async def complete_session(data: dict):
    """Aggregate task transcripts and return a unified evaluation."""
    rapid_fire = data["rapid_fire"]
    word_bomb = data["word_bomb"]
    deep_dive = data["deep_dive"]

    evaluation = evaluate_full_session(
        rapid_fire=rapid_fire,
        word_bomb=word_bomb,
        deep_dive=deep_dive,
    )

    return {"evaluation": evaluation}






