#!/usr/bin/env python3
"""Design custom voices using ElevenLabs Voice Design API"""

import os
import base64
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

# Character voice descriptions
VOICE_DESIGNS = {
    "casey": {
        "description": """A male narrator in his early 30s with a dry, slightly exasperated American voice.
        He sounds like someone who's seen too much internet chaos and is tired but still shows up.
        Think podcast host energy mixed with deadpan comedy delivery.
        Warm but sarcastic undertone, the kind of guy who sighs before reading something ridiculous.
        Clear enunciation, medium pitch, conversational but authoritative.""",
        "preview_text": "Internet Improv presents... I mumbled my name at a coffee shop. The barista heard Kevin. I panicked and just nodded. Now she asks about my dog every morning. I don't own any pets."
    },
    "rex": {
        "description": """A male voice in his late 20s with an extremely deadpan, monotone delivery.
        Deep voice, slow and deliberate pacing. Zero enthusiasm, maximum sarcasm.
        Sounds perpetually unimpressed, like nothing surprises him anymore.
        American accent, very dry humor, the kind of voice that makes simple statements hilarious.""",
        "preview_text": "You have two options. One: Find another coffee place. Two: Change your name to Kevin. Both are equally reasonable."
    },
    "fizz": {
        "description": """A young male voice, early 20s, absolutely bursting with chaotic energy.
        Fast-talking, excitable, slightly unhinged. High energy like a caffeinated gamer or YouTuber.
        American accent, tends to speed up when excited.
        Mischievous tone, always sounds like he's about to suggest something ridiculous.""",
        "preview_text": "Option 2 sounds easier! I hear Kevin rescues injured pandas in his spare time. The guy's a legend!"
    },
    "harper": {
        "description": """A warm, kind female voice in her mid-20s with genuine sweetness.
        Soft and friendly, the voice of someone who sees the best in everyone.
        American accent, gentle tone, sounds like a supportive friend.
        Wholesome energy without being saccharine, authentic warmth.""",
        "preview_text": "Or just embrace it! Who doesn't want a cool coffee persona like Kevin? I think it's kind of sweet actually."
    },
    "mira": {
        "description": """A dramatic female voice in her late 20s who treats everything like theater.
        Theatrical, expressive, tends to over-enunciate for effect.
        Rich, resonant voice that projects emotion. Think stage actress energy.
        American accent with dramatic flair, gasps and sighs built into her delivery.""",
        "preview_text": "Kevin? Oh, he once climbed a tree to save my blind kitten. One hell of a guy, I tell ya! A true hero among us!"
    },
    "dot": {
        "description": """A matter-of-fact female voice in her early 30s, intellectual and precise.
        Sounds like she's always explaining something, slightly nerdy delivery.
        Clear and articulate, the voice of someone who loves details and facts.
        American accent, measured pace, treats every statement as important information.""",
        "preview_text": "I heard someone say that if Kevin dies, he's giving his eyes to Stevie Wonder. Technically that would require specific legal arrangements."
    },
    "byte": {
        "description": """A slightly robotic male voice, young adult, with subtle glitchy qualities.
        Speaks in a measured, algorithmic way but with hints of developing personality.
        Occasionally emphasizes words unexpectedly, like an AI learning human speech patterns.
        Neutral accent, calm and collected, deadpan but not quite human.""",
        "preview_text": "Chuck Norris has a shrine dedicated to Kevin. This information has been verified by multiple sources. Probability of accuracy: high."
    },
}


def design_voice(character_name):
    """Generate voice previews for a character."""
    if character_name not in VOICE_DESIGNS:
        print(f"Unknown character: {character_name}")
        print(f"Available: {', '.join(VOICE_DESIGNS.keys())}")
        return

    design = VOICE_DESIGNS[character_name]

    print(f"\nDesigning voice for: {character_name}")
    print(f"Description: {design['description'][:100]}...")

    client = ElevenLabs(api_key=API_KEY)

    # Generate voice previews
    response = client.text_to_voice.create_previews(
        voice_description=design["description"],
        text=design["preview_text"],
    )

    # Save previews
    output_dir = BASE_DIR / "episodes" / "001-kevin-identity" / "audio" / "voice_designs" / character_name
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nGenerated {len(response.previews)} previews:")

    for i, preview in enumerate(response.previews):
        filepath = output_dir / f"{character_name}_design_{i}.mp3"

        # Decode base64 audio and save
        audio_data = base64.b64decode(preview.audio_base_64)
        with open(filepath, "wb") as f:
            f.write(audio_data)

        print(f"  Preview {i}: {filepath}")
        print(f"    Voice ID: {preview.generated_voice_id}")

        # Save voice ID to file for later use
        id_file = output_dir / f"{character_name}_design_{i}_voice_id.txt"
        with open(id_file, "w") as f:
            f.write(preview.generated_voice_id)

    print(f"\nListen to the previews and pick your favorite!")
    print(f"Voice IDs saved alongside audio files for later use.")


def list_characters():
    """List available characters."""
    print("\nAvailable characters:")
    print("-" * 60)
    for name, design in VOICE_DESIGNS.items():
        print(f"{name}: {design['description'][:60]}...")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python design_voice.py list           - List characters")
        print("  python design_voice.py <character>    - Design voice for character")
        print("  python design_voice.py all            - Design voices for all characters")
        print("\nExample:")
        print("  python design_voice.py casey")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "list":
        list_characters()
    elif cmd == "all":
        for character in VOICE_DESIGNS:
            design_voice(character)
    else:
        design_voice(cmd)
