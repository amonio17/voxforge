from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import shutil
import uuid
import os

from voice_engine.tts_engine import VoiceEngine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = VoiceEngine()

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "output"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.post("/clone")
async def clone_voice(
    text: str = Form(...),
    speaker_wav: UploadFile = File(...)
):
    file_id = str(uuid.uuid4())

    speaker_path = f"{UPLOAD_DIR}/{file_id}.wav"
    output_path = f"{OUTPUT_DIR}/{file_id}.wav"

    with open(speaker_path, "wb") as buffer:
        shutil.copyfileobj(speaker_wav.file, buffer)

    engine.generate(text, speaker_path, output_path)

    return {
        "audio_url": f"http://127.0.0.1:8000/audio/{file_id}"
    }


@app.get("/audio/{file_id}")
def get_audio(file_id: str):
    path = f"{OUTPUT_DIR}/{file_id}.wav"
    return FileResponse(path, media_type="audio/wav")
