from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from voice_engine.tts_engine import VoiceEngine

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# dossiers
os.makedirs("voices", exist_ok=True)
os.makedirs("output", exist_ok=True)

engine = VoiceEngine()

@app.post("/clone")
async def clone(file: UploadFile = File(...), text: str = Form(...)):
    file_path = f"voices/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    output_file = engine.generate(
        text=text,
        speaker_wav=file_path
    )

    return {"file": output_file}

app.mount("/", StaticFiles(directory="web", html=True), name="web")
