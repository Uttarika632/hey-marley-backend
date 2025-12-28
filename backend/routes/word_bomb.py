from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from chains.word_bomb_feedback import generate_word_bomb_feedback
from chains.word_bomb_words import generate_word_bomb_words


router = APIRouter()


# === Word Generation (before gameplay) ===

class WordBombProfile(BaseModel):
    age: str
    city: str
    country: str
    academic_interests: List[str]
    personal_interests: List[str]
    communication_goals: List[str]
    emotional_needs: List[str]
    short_term_goal: str


@router.post("/word-bomb/start")
async def start_word_bomb(profile: WordBombProfile):
    """Generate personalized Word Bomb words based on user profile."""
    words = generate_word_bomb_words(
        age=profile.age,
        city=profile.city,
        country=profile.country,
        academic_interests=profile.academic_interests,
        personal_interests=profile.personal_interests,
        communication_goals=profile.communication_goals,
        emotional_needs=profile.emotional_needs,
        short_term_goal=profile.short_term_goal,
    )
    return {"words": words}


# === Feedback (after gameplay) ===

class WordBombFeedbackInput(BaseModel):
    transcript: str
    words: List[str]


@router.post("/word-bomb-feedback")
async def word_bomb_feedback(input: WordBombFeedbackInput):
    """Generate structured feedback for Word Bomb challenge."""
    response = generate_word_bomb_feedback(input.transcript, input.words)
    return {"feedback": response}


