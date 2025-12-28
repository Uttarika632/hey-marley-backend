from pathlib import Path
#from dotenv import load_dotenv
import os

# Load .env from project root (one level up from backend - openAI/comet API keys)
#load_dotenv(Path(__file__).parent.parent / ".env")
# Load .env from project root (backendopenAI/comet API keys)
#load_dotenv(Path(__file__).parent / ".env")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.stt import router as stt_router
from backend.routes.feedback import router as feedback_router
from backend.routes.word_bomb import router as word_bomb_router
from backend.routes.deep_dive import router as deep_dive_router
from backend.routes import session_complete
from backend.routes import rapid_fire
from backend.routes import action_plan
from backend.routes import skill_profile
# Opik client disabled for now (package not installed)
# from backend.utils.opik_client import init_opik
# opik_client = init_opik()

app = FastAPI(
    title="Hey Marley Backend",
    description="AI-powered backend service",
    version="1.0.0"
)

# Enable CORS for frontend (allow_credentials must be False when using "*" origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For local dev
    allow_credentials=False,  # Must be False when using "*"
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(stt_router, tags=["Speech-to-Text"])
app.include_router(feedback_router, tags=["Feedback"])
app.include_router(word_bomb_router, prefix="/api", tags=["Word Bomb"])
app.include_router(deep_dive_router, prefix="/api", tags=["Deep Dive"])
app.include_router(session_complete.router, prefix="/api", tags=["Session"])
app.include_router(action_plan.router, prefix="/api", tags=["Action Plan"])
app.include_router(rapid_fire.router, prefix="/api", tags=["Rapid Fire"])
app.include_router(skill_profile.router, prefix="/api", tags=["Skill Profile"])


@app.get("/")
async def root():
    return {"message": "Hello from Hey Marley Backend"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

