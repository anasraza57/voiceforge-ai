from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from clone_voice import clone_voice
from synthesize import generate_speech

app = FastAPI(
    title="VoiceForge TTS API",
    description="Upload a voice sample and text to generate speech using Tortoise-TTS",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health"])
def root():
    return {"message": "VoiceForge TTS API is up and running."}

@app.get("/health", tags=["Health"])
def health():
    return {"ok": True}

@app.post("/generate", tags=["TTS Generation"], summary="Generate speech from a voice sample and text")
async def generate(voice_sample: UploadFile = File(...), text: str = Form(...)):
    os.makedirs("storage", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    # Save the uploaded file
    voice_path = f"storage/{voice_sample.filename}"
    with open(voice_path, "wb") as buffer:
        shutil.copyfileobj(voice_sample.file, buffer)

    # Pass the voice file path directly to generate_speech
    output_path = generate_speech(text, voice_path)

    return FileResponse(output_path, media_type="audio/wav")
