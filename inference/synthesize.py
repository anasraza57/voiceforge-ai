import torch
import torchaudio
from tortoise.api import TextToSpeech  
from tortoise.utils.audio import load_audio
import os
import random
import string

# Initialize TTS as None - load lazily
tts = None

def get_tts():
    global tts
    if tts is None:
        tts = TextToSpeech()
    return tts

def generate_speech(text, voice_path):
    # Load voice audio directly from file path
    voice_samples = load_audio(voice_path, 22050)
    voice_samples = voice_samples.unsqueeze(0)  # Add batch dimension
    conditioning_latents = None  # Let tortoise compute these

    # Get TTS instance (loads lazily)
    tts_instance = get_tts()

    # Generate speech
    output = tts_instance.tts_with_preset(
        text,
        voice_samples=voice_samples,
        preset="fast"
    )

    # Save to file
    random_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    output_path = f"outputs/generated_{random_id}.wav"
    torchaudio.save(output_path, output.squeeze(0).cpu(), 24000)
    return output_path