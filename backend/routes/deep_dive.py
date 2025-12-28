import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from langchain_openai import ChatOpenAI

from backend.chains.deep_dive_start import generate_deep_dive_start
from backend.chains.deep_dive_evaluate import generate_deep_dive_evaluation


router = APIRouter()

# In-memory session storage (use Redis/DB in production)
sessions: dict[str, dict] = {}

# LLM for generating follow-ups
llm = ChatOpenAI(model="gpt-4", temperature=0.7)


# === Request/Response Models ===

class DeepDiveProfile(BaseModel):
    age: str
    city: str
    country: str
    academic_interests: List[str]
    personal_interests: List[str]
    communication_goals: List[str]
    emotional_needs: List[str]
    short_term_goal: str


class StartResponse(BaseModel):
    session_id: str
    topic: str
    opening_question: str


class AnswerRequest(BaseModel):
    session_id: str
    answer: str


class AnswerResponse(BaseModel):
    message: Optional[str] = None
    is_complete: bool = False


class EvaluateRequest(BaseModel):
    topic: str
    turns: List[dict]


class EvaluateResponse(BaseModel):
    feedback: str


# === Helper Functions ===

def generate_followup(topic: str, conversation_history: str, last_answer: str) -> str:
    """Generate a follow-up question based on the conversation."""
    messages = [
        {"role": "system",
         "content": f"You are Marley, a warm, curious teen coach. "
                    f"The topic is: {topic}. "
                    f"Your job is to ask ONE thoughtful, simple follow-up question "
                    f"that helps the student elaborate on their thinking. "
                    f"Keep it conversational and short. Do NOT ask multi-part questions."},
        {"role": "user", "content": f"Conversation so far:\n{conversation_history}\n\nStudent's last answer: {last_answer}"}
    ]
    return llm.invoke(messages).content


# === Endpoints ===

@router.post("/deep-dive/start", response_model=StartResponse)
async def start_deep_dive(profile: DeepDiveProfile):
    """Start a new personalized Deep Dive session."""
    # Generate personalized topic and opening question
    result = generate_deep_dive_start(
        age=profile.age,
        city=profile.city,
        country=profile.country,
        academic_interests=profile.academic_interests,
        personal_interests=profile.personal_interests,
        communication_goals=profile.communication_goals,
        emotional_needs=profile.emotional_needs,
        short_term_goal=profile.short_term_goal,
    )
    
    session_id = str(uuid.uuid4())
    
    # Initialize session
    sessions[session_id] = {
        "turn": 0,
        "topic": result["topic"],
        "questions": [result["opening_question"]],
        "answers": []
    }
    
    return StartResponse(
        session_id=session_id,
        topic=result["topic"],
        opening_question=result["opening_question"]
    )


@router.post("/deep-dive/answer", response_model=AnswerResponse)
async def submit_answer(request: AnswerRequest):
    """Submit user's answer and get next question or signal completion."""
    session_id = request.session_id
    answer = request.answer
    
    # Get session
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_id]
    
    # Store the answer
    session["answers"].append(answer)
    session["turn"] += 1
    
    # Build conversation history
    conversation_history = ""
    for q, a in zip(session["questions"], session["answers"]):
        conversation_history += f"Q: {q}\nA: {a}\n\n"
    
    # Check if we've done 3 turns (0, 1, 2 -> after 3rd answer we're complete)
    if session["turn"] >= 3:
        return AnswerResponse(
            is_complete=True
        )
    
    # Generate follow-up question
    followup = generate_followup(session["topic"], conversation_history, answer)
    session["questions"].append(followup)
    
    return AnswerResponse(
        message=followup,
        is_complete=False
    )


@router.post("/deep-dive/evaluate", response_model=EvaluateResponse)
async def evaluate_deep_dive(request: EvaluateRequest):
    """Evaluate the full Deep Dive conversation."""
    feedback = generate_deep_dive_evaluation(request.topic, request.turns)
    return EvaluateResponse(feedback=feedback)


@router.delete("/deep-dive/{session_id}")
async def end_session(session_id: str):
    """End a Deep Dive session early."""
    if session_id in sessions:
        del sessions[session_id]
    return {"status": "session ended"}


# === Legacy endpoints for backwards compatibility ===

@router.post("/deepdive/start")
async def legacy_start():
    """Legacy start endpoint."""
    session_id = str(uuid.uuid4())
    initial_question = "How can AI make changes in education? Share your first thought."
    
    sessions[session_id] = {
        "turn": 0,
        "topic": "AI in Education",
        "questions": [initial_question],
        "answers": []
    }
    
    return {"session_id": session_id, "question": initial_question}


@router.post("/deepdive/answer")
async def legacy_answer(request: AnswerRequest):
    """Legacy answer endpoint."""
    return await submit_answer(request)
