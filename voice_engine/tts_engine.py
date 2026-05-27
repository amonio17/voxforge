import os
import torch
from TTS.api import TTS

# 🔥 FIX stable XTTS (PyTorch weights_only issue)
_original_torch_load = torch.load

def patched_torch_load(*args, **kwargs):
    kwargs["weights_only"] = False
    return _original_torch_load(*args, **kwargs)

torch.load = patched_torch_load


class VoiceEngine:
    def __init__(self):
        print("🔄 Chargement du modèle XTTS v2...")

        self.tts = TTS(
            model_name="tts_models/multilingual/multi-dataset/xtts_v2",
            progress_bar=False,
            gpu=False
        )

        print("✅ Modèle chargé")

    def generate(self, text, speaker_wav, output_path="output/generated.wav"):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        if not os.path.exists(speaker_wav):
            raise FileNotFoundError("Fichier audio introuvable")

        self.tts.tts_to_file(
            text=text,
            speaker_wav=speaker_wav,
            file_path=output_path
        )

        return output_path
