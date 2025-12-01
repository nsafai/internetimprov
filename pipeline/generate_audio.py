#!/usr/bin/env python3
"""
Internet Improv - Audio Generator using ElevenLabs
Generates voice audio for each shot using character-appropriate voices
"""

import os
from pathlib import Path
from elevenlabs import ElevenLabs, VoiceSettings

BASE_DIR = Path(__file__).resolve().parent.parent

# Try to load from .env file first
def load_api_key():
    env_file = BASE_DIR / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if line.startswith("ELEVENLABS_API_KEY="):
                    return line.strip().split("=", 1)[1]
    return os.environ.get("ELEVENLABS_API_KEY")

API_KEY = load_api_key()

BASE_DIR = Path(__file__).resolve().parent.parent
AUDIO_DIR = BASE_DIR / "episodes" / "001-kevin-identity" / "audio"

# Voice IDs from ElevenLabs voice library
# You can browse voices at: https://elevenlabs.io/voice-library
# These are placeholder IDs - we'll pick real ones together
VOICES = {
    "casey": "wAQta5nXit6sNLk15rnQ",      # Custom designed voice - dry, exasperated narrator
    "rex": "ErXwobaYiN019PkySvjV",         # Antoni - deep, deadpan
    "fizz": "VR6AewLTigWG4xSOukaG",        # Arnold - energetic, youthful
    "harper": "EXAVITQu4vr4xnSDxMaL",      # Bella - warm, friendly female
    "mira": "21m00Tcm4TlvDq8ikWAM",        # Rachel - dramatic female
    "dot": "AZnzlk1XvdvUeBnXmlld",         # Domi - matter-of-fact female
    "byte": "MF3mGyEYCl7XYWbV9V6O",        # Elli - slightly robotic
}

# Voice settings per character (stability, similarity_boost, style)
# Lower stability = more expressive/varied
# Higher style = more emotional range
VOICE_SETTINGS = {
    "casey": VoiceSettings(stability=0.4, similarity_boost=0.75, style=0.5),  # Expressive narrator
    "casey_reading": VoiceSettings(stability=0.15, similarity_boost=0.6, style=1.0),  # Max expressiveness for OP readings
    "rex": VoiceSettings(stability=0.8, similarity_boost=0.8, style=0.2),  # Deadpan, monotone
    "fizz": VoiceSettings(stability=0.25, similarity_boost=0.7, style=0.9),  # Chaotic, energetic
    "harper": VoiceSettings(stability=0.5, similarity_boost=0.8, style=0.6),  # Warm, friendly
    "mira": VoiceSettings(stability=0.3, similarity_boost=0.75, style=0.95),  # Theatrical, dramatic
    "dot": VoiceSettings(stability=0.7, similarity_boost=0.8, style=0.3),  # Matter-of-fact
    "byte": VoiceSettings(stability=0.85, similarity_boost=0.9, style=0.1),  # Robotic, consistent
}

# Episode 001 script
SCRIPT = {
    "01_casey_hook": {
        "character": "casey",
        "line": "Internet Improv presents...",
    },
    "02_casey_reading": {
        "character": "casey",
        "line": "I mumbled my name at a coffee shop. The barista heard... Kevin! I panicked and just nodded. Now she asks about my dog every morning. I don't own any pets.",
        "voice_settings": "casey_reading",  # Use more expressive settings
    },
    "03_rex_deadpan": {
        "character": "rex",
        "line": "You have two options. One: Find another coffee place. Two: Change your name to Kevin.",
    },
    "04_fizz_excited": {
        "character": "fizz",
        "line": "Option 2 sounds easier!",
    },
    "05_harper_wholesome": {
        "character": "harper",
        "line": "Or just embrace it! Who doesn't want a cool coffee persona like Kevin?",
    },
    "06_fizz_mischievous": {
        "character": "fizz",
        "line": "I hear Kevin rescues injured pandas in his spare time. The guy's a legend.",
    },
    "07_byte_robotic": {
        "character": "byte",
        "line": "Chuck Norris has a shrine dedicated to Kevin.",
    },
    "08_mira_theatrical": {
        "character": "mira",
        "line": "Kevin? Oh, he once climbed a tree to save my blind kitten. One hell of a guy, I tell ya!",
    },
    "09_dot_serious": {
        "character": "dot",
        "line": "I heard someone say that if Kevin dies, he's giving his eyes to Stevie Wonder.",
    },
    "10_casey_outro": {
        "character": "casey",
        "line": "...Follow for more Internet Improv.",
    },
}


def generate_audio(shot_key, output_dir=None):
    """Generate audio for a specific shot."""

    if not API_KEY:
        print("ERROR: ELEVENLABS_API_KEY not set")
        print("Set it with: set ELEVENLABS_API_KEY=your_key_here")
        return None

    if shot_key not in SCRIPT:
        print(f"Unknown shot: {shot_key}")
        return None

    shot = SCRIPT[shot_key]
    character = shot["character"]
    line = shot["line"]
    voice_id = VOICES[character]

    # Get voice settings - use shot-specific override if available, else character default
    settings_key = shot.get("voice_settings", character)
    voice_settings = VOICE_SETTINGS.get(settings_key)

    print(f"\nGenerating audio for: {shot_key}")
    print(f"Character: {character}")
    print(f"Line: {line}")
    if voice_settings:
        print(f"Settings: stability={voice_settings.stability}, style={voice_settings.style}")

    client = ElevenLabs(api_key=API_KEY)

    # Generate audio
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        text=line,
        model_id="eleven_multilingual_v2",  # Best quality model
        voice_settings=voice_settings,
    )

    # Determine output directory
    if output_dir is None:
        output_dir = AUDIO_DIR

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Save audio file
    filename = f"{shot_key}.mp3"
    filepath = output_path / filename

    with open(filepath, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    print(f"Saved: {filepath}")
    return filepath


def generate_all():
    """Generate audio for all shots."""
    print("\n" + "="*60)
    print("GENERATING ALL AUDIO FOR EPISODE 001")
    print("="*60)

    for shot_key in SCRIPT:
        generate_audio(shot_key)
        print()


def list_shots():
    """List all shots and their lines."""
    print("\nEpisode 001 Script:")
    print("-" * 60)
    for key, shot in SCRIPT.items():
        print(f"{key} ({shot['character']}): \"{shot['line'][:50]}...\"" if len(shot['line']) > 50 else f"{key} ({shot['character']}): \"{shot['line']}\"")


def list_voices():
    """List available voices from ElevenLabs."""
    if not API_KEY:
        print("ERROR: ELEVENLABS_API_KEY not set")
        return

    client = ElevenLabs(api_key=API_KEY)
    voices = client.voices.get_all()

    print("\nAvailable voices:")
    print("-" * 60)
    for voice in voices.voices:
        print(f"{voice.voice_id}: {voice.name}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python generate_audio.py list        - List shots and lines")
        print("  python generate_audio.py voices      - List available ElevenLabs voices")
        print("  python generate_audio.py <shot_key>  - Generate audio for specific shot")
        print("  python generate_audio.py all         - Generate all audio")
        print("\nExample:")
        print("  python generate_audio.py 01_casey_hook")
        print("\nFirst, set your API key:")
        print("  set ELEVENLABS_API_KEY=your_key_here")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "list":
        list_shots()
    elif cmd == "voices":
        list_voices()
    elif cmd == "all":
        generate_all()
    else:
        generate_audio(cmd)
