import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

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

os.makedirs("output", exist_ok=True)

@app.post("/clone")
async def clone(text: str = Form(...), speaker_wav: UploadFile = File(...)):

    input_path = f"output/{speaker_wav.filename}"
    with open(input_path, "wb") as f:
        f.write(await speaker_wav.read())

    output_path = "output/result.wav"

    engine.generate(text, input_path, output_path)

    return {
        "audio_url": "/output/result.wav"
    }

# 🔥 IMPORTANT : servir le FRONTEND correctement
app.mount("/", StaticFiles(directory="web", html=True), name="web")

# 🔥 servir les fichiers audio
app.mount("/output", StaticFiles(directory="output"), name="output")
