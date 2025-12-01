#!/usr/bin/env python3
"""Test different voices for a character"""

import os
from pathlib import Path
from elevenlabs import ElevenLabs

BASE_DIR = Path(__file__).resolve().parent.parent

def load_api_key():
    env_file = BASE_DIR / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if line.startswith("ELEVENLABS_API_KEY="):
                    return line.strip().split("=", 1)[1]
    return os.environ.get("ELEVENLABS_API_KEY")

API_KEY = load_api_key()

# Test voices for Casey (male narrator)
TEST_VOICES = {
    "adam": "pNInz6obpgDQGcFmaJgB",
    "brian": "nPczCjzI2devNBz1zQrb",
    "daniel": "onwK4e9ZLuTAKqWW03F9",
    "charlie": "IKne3meq5aSn9XLyUdCD",
    "george": "JBFqnCBsd6RMkjVDRZzb",
    "chris": "iP95p4xoKVk53GoZ742B",
}

TEST_LINE = "internet improv presents"

def generate_samples():
    output_dir = BASE_DIR / "episodes" / "001-kevin-identity" / "audio" / "voice_tests"
    output_dir.mkdir(parents=True, exist_ok=True)

    client = ElevenLabs(api_key=API_KEY)

    for name, voice_id in TEST_VOICES.items():
        print(f"Generating sample for: {name}")

        audio = client.text_to_speech.convert(
            voice_id=voice_id,
            text=TEST_LINE,
            model_id="eleven_multilingual_v2",
        )

        filepath = output_dir / f"casey_test_{name}.mp3"
        with open(filepath, "wb") as f:
            for chunk in audio:
                f.write(chunk)

        print(f"  Saved: {filepath}")

    print(f"\nAll samples saved to: {output_dir}")

if __name__ == "__main__":
    generate_samples()
