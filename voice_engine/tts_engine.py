import os
import torch
from TTS.api import TTS

class VoiceEngine:
    def __init__(self):
        print("🔄 Loading XTTS v2 (MAX QUALITY MODE)...")

        # ⚡ force safer torch load
        torch.set_num_threads(4)

        self.tts = TTS(
            model_name="tts_models/multilingual/multi-dataset/xtts_v2",
            progress_bar=False,
            gpu=False  # mets True si GPU NVIDIA
        )

        print("✅ XTTS READY (QUALITY MODE)")

    def generate(self, text, speaker_wav, output_path, language="en"):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # 🔥 CLEAN HIGH QUALITY GENERATION
        self.tts.tts_to_file(
            text=text,
            speaker_wav=speaker_wav,
            file_path=output_path,
            language=language,

            # ⚡ improve stability + natural speech
            split_sentences=True
        )

        return output_path
