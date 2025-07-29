from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
import shutil
from clone_voice import clone_voice
from synthesize import generate_speech
import os

app = FastAPI()

@app.post("/generate")
async def generate(voice_sample: UploadFile = File(...), text: str = Form(...)):
    os.makedirs("storage", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    voice_path = f"storage/{voice_sample.filename}"
    with open(voice_path, "wb") as buffer:
        shutil.copyfileobj(voice_sample.file, buffer)

    embedding = clone_voice(voice_path)
    output_path = generate_speech(text, embedding)
    return FileResponse(output_path, media_type="audio/wav")