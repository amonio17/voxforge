import os
from TTS.api import TTS

class VoiceEngine:
    def __init__(self):
        print("🔄 Chargement XTTS v2...")
        self.tts = TTS(
            model_name="tts_models/multilingual/multi-dataset/xtts_v2",
            progress_bar=False,
            gpu=False
        )
        print("✅ Modèle prêt")

    def generate(self, text, speaker_wav, output_path="output/generated.wav", language="en"):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        if not os.path.exists(speaker_wav):
            raise FileNotFoundError("Audio introuvable")

        self.tts.tts_to_file(
            text=text,
            speaker_wav=speaker_wav,
            file_path=output_path,
            language=language
        )

        return output_path
