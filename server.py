from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os
import uuid

from voice_engine.tts_engine import VoiceEngine

app = FastAPI()
engine = VoiceEngine()

os.makedirs("output", exist_ok=True)
os.makedirs("uploads", exist_ok=True)

app.mount("/output", StaticFiles(directory="output"), name="output")
app.mount("/web", StaticFiles(directory="web"), name="web")

# HOME FIX
@app.get("/")
def home():
    return HTMLResponse('<script>window.location="/web/index.html"</script>')

# VOICE CLONE MAX QUALITY
@app.post("/clone")
async def clone(
    text: str = Form(...),
    language: str = Form("en"),
    speaker_wav: UploadFile = File(...)
):

    uid = str(uuid.uuid4())

    input_path = f"uploads/{uid}.wav"
    output_path = f"output/{uid}.wav"

    # save audio
    with open(input_path, "wb") as f:
        shutil.copyfileobj(speaker_wav.file, f)

    # generate high quality voice
    audio_file = engine.generate(
        text=text,
        speaker_wav=input_path,
        output_path=output_path,
        language=language
    )

    return {
        "audio_url": f"/output/{uid}.wav"
    }
