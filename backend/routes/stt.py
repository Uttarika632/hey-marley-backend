import os

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from openai import OpenAI


router = APIRouter()


def get_openai_client():
    """Get OpenAI client (initialized lazily)"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    return OpenAI(api_key=api_key)


@router.post("/stt")
async def transcribe_audio(file: UploadFile = File(...)):
    client = get_openai_client()
    
    # Save uploaded audio file temporarily
    temp_file_path = f"temp/{file.filename}"
    os.makedirs("temp", exist_ok=True)

    with open(temp_file_path, "wb+") as f:
        f.write(await file.read())

    # Run Whisper transcription
    with open(temp_file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    
    transcript = transcription.text

    # Save transcript in a folder for now (later move to DB)
    os.makedirs("transcripts", exist_ok=True)
    transcript_path = f"transcripts/{file.filename}.txt"

    with open(transcript_path, "w") as f:
        f.write(transcript)

    # Clean up temp file
    os.remove(temp_file_path)

    return JSONResponse({
        "transcript": transcript,
        "file_saved": transcript_path
    })
