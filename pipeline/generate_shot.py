#!/usr/bin/env python3
"""
Internet Improv - Shot Generator for Runway
Generates medium-shot character images optimized for Runway Gen-3/4 animation
"""

import requests
import base64
import json
from pathlib import Path
from datetime import datetime

API_URL = "http://127.0.0.1:7860"
BASE_DIR = Path(__file__).resolve().parent.parent
EPISODES_DIR = BASE_DIR / "episodes"

# Runway-optimized settings (medium shot, larger for quality)
RUNWAY_SETTINGS = {
    "sampler_name": "DPM++ 2M Karras",
    "steps": 25,  # Higher quality
    "cfg_scale": 7,
    "width": 1024,   # Square works well for medium shots
    "height": 1024,
    "batch_size": 3,  # 3 variations per shot
    "seed": -1,
}

# Base style prompt (consistent across all characters)
STYLE_BASE = "3D animated character, Pixar Disney style, stylized proportions, soft 3D render, smooth skin texture, warm studio lighting, clean solid cream beige background"
STYLE_QUALITY = "high quality, detailed, professional 3D animation style, Pixar aesthetic, DreamWorks style, soft diffused lighting, clean render"

# Framing for Runway (medium shot)
RUNWAY_FRAMING = "medium shot, chest up, waist up framing, character centered, face clearly visible, looking at camera"

NEGATIVE_PROMPT = "photorealistic, hyperrealistic, photograph, real human, anime, 2d, flat, cartoon, sketch, painting, watercolor, blurry, low quality, bad anatomy, extra fingers, mutated hands, poorly drawn face, distorted face, ugly, duplicate, morbid, dark, gritty, horror, scary, nsfw, nude, text, watermark, signature, logo, multiple characters, crowd, full body, legs visible, feet visible"

# Character definitions
CHARACTERS = {
    "casey": {
        "identity": "adult man late 20s, short dark brown hair side-parted, thick expressive dark eyebrows, brown eyes, warm tan skin, slight stubble, friendly approachable face",
        "outfit": "olive khaki blazer jacket, cream beige button-up collared shirt, dark wristwatch on left wrist",
    },
    "rex": {
        "identity": "adult man early 30s, sharp angular face, short black hair slicked back, piercing dark eyes, pale skin, perpetually unimpressed expression, lean build",
        "outfit": "all black outfit, black turtleneck sweater, black jacket",
    },
    "fizz": {
        "identity": "young adult, wild spiky orange-yellow hair, bright wide eyes, round energetic face, freckles, mischievous grin, small and wiry build",
        "outfit": "bright yellow hoodie, orange accents, casual energetic style",
    },
    "harper": {
        "identity": "adult woman mid 20s, soft wavy light brown hair, warm kind eyes, gentle smile, rosy cheeks, soft rounded features",
        "outfit": "soft pink cozy sweater, delicate necklace, warm and inviting appearance",
    },
    "mira": {
        "identity": "adult woman late 20s, dramatic dark wavy hair, expressive large eyes with bold makeup, theatrical features, elegant bone structure",
        "outfit": "sheer transparent purple blouse, dramatic accessories, theatrical bohemian style",
    },
    "dot": {
        "identity": "adult woman early 30s, neat short dark hair with bangs, large round glasses, intelligent focused eyes, serious but kind face",
        "outfit": "smart navy blue cardigan, white collared shirt underneath, professional academic style",
    },
    "byte": {
        "identity": "androgynous young adult, short teal-blue hair with digital gradient effect, slightly robotic smooth features, glowing subtle cyan eyes, friendly but slightly uncanny",
        "outfit": "tech hoodie with circuit pattern details, minimalist futuristic style, subtle LED accents",
    },
}

# Shot-specific prompts for Episode 001
EPISODE_001_SHOTS = {
    "shot01_casey_hook": {
        "character": "casey",
        "expression": "neutral confident expression, slight friendly smile, looking at camera",
        "pose": "holding tablet in hands, presenting stance",
        "action": "about to speak, welcoming",
    },
    "shot02_casey_reading": {
        "character": "casey",
        "expression": "focused reading expression, looking down slightly, concentrated",
        "pose": "holding tablet, looking at screen",
        "action": "reading from tablet",
    },
    "shot03_rex_deadpan": {
        "character": "rex",
        "expression": "deadpan expression, flat unamused stare, one eyebrow slightly raised",
        "pose": "arms crossed over chest",
        "action": "delivering dry commentary",
    },
    "shot04_fizz_excited": {
        "character": "fizz",
        "expression": "excited expression, wide grin, eyes bright with enthusiasm",
        "pose": "hands up gesturing, animated stance",
        "action": "enthusiastically agreeing",
    },
    "shot05_harper_wholesome": {
        "character": "harper",
        "expression": "warm genuine smile, kind eyes, soft expression",
        "pose": "hands clasped together near chest",
        "action": "offering kind suggestion",
    },
    "shot06_fizz_mischievous": {
        "character": "fizz",
        "expression": "mischievous grin, conspiratorial look, raised eyebrow",
        "pose": "leaning forward slightly, hands together",
        "action": "sharing a secret, playful",
    },
    "shot07_byte_robotic": {
        "character": "byte",
        "expression": "slightly robotic smile, friendly but uncanny, processing look",
        "pose": "standing straight, slight head tilt",
        "action": "delivering fact with artificial enthusiasm",
    },
    "shot08_mira_theatrical": {
        "character": "mira",
        "expression": "dramatic theatrical expression, emotional, eyes glistening",
        "pose": "one hand on chest, other hand gesturing outward",
        "action": "dramatic storytelling moment",
    },
    "shot09_dot_serious": {
        "character": "dot",
        "expression": "matter-of-fact expression, serious but earnest, slight knowing look",
        "pose": "adjusting glasses with one hand",
        "action": "delivering obscure fact",
    },
    "shot10_casey_outro": {
        "character": "casey",
        "expression": "tired deadpan expression, slight exhale, done with this energy",
        "pose": "holding tablet loosely, shoulders slightly slumped",
        "action": "wrapping up, looking at camera",
    },
}


def build_prompt(shot_key):
    """Build full prompt for a specific shot."""
    shot = EPISODE_001_SHOTS[shot_key]
    char = CHARACTERS[shot["character"]]

    parts = [
        STYLE_BASE,
        RUNWAY_FRAMING,
        char["identity"],
        char["outfit"],
        shot["pose"],
        shot["expression"],
        shot["action"],
        STYLE_QUALITY,
    ]

    return ", ".join(parts)


def generate_shot(shot_key, output_dir=None):
    """Generate images for a specific shot."""

    if shot_key not in EPISODE_001_SHOTS:
        print(f"Unknown shot: {shot_key}")
        print(f"Available shots: {list(EPISODE_001_SHOTS.keys())}")
        return None

    shot = EPISODE_001_SHOTS[shot_key]
    prompt = build_prompt(shot_key)

    print(f"\n{'='*60}")
    print(f"Generating: {shot_key}")
    print(f"Character: {shot['character']}")
    print(f"{'='*60}")
    print(f"\nPrompt preview: {prompt[:100]}...")

    payload = {
        **RUNWAY_SETTINGS,
        "prompt": prompt,
        "negative_prompt": NEGATIVE_PROMPT,
    }

    print(f"\nSending request to API...")

    try:
        r = requests.post(f"{API_URL}/sdapi/v1/txt2img", json=payload, timeout=600)

        if r.status_code == 200:
            result = r.json()
            images = result["images"]
            info = json.loads(result.get("info", "{}"))
            seed = info.get("seed", "unknown")

            # Determine output directory
            if output_dir is None:
                output_dir = EPISODES_DIR / "001-kevin-identity" / "shots"

            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)

            # Save images
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            saved_files = []

            for i, img_data in enumerate(images):
                filename = f"{shot_key}_{timestamp}_{i:02d}.png"
                filepath = output_path / filename

                img_bytes = base64.b64decode(img_data)
                with open(filepath, 'wb') as f:
                    f.write(img_bytes)

                saved_files.append(filepath)
                print(f"  Saved: {filename}")

            print(f"\nGenerated {len(saved_files)} images")
            print(f"Seed: {seed}")
            print(f"Output: {output_path}")

            return saved_files
        else:
            print(f"Error: {r.status_code}")
            print(r.text)
            return None

    except requests.exceptions.Timeout:
        print("Error: Request timed out (10 min limit)")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def list_shots():
    """List all available shots."""
    print("\nAvailable shots for Episode 001:")
    print("-" * 50)
    for key, shot in EPISODE_001_SHOTS.items():
        print(f"  {key}: {shot['character']} - {shot['expression'][:40]}...")


def generate_all():
    """Generate all shots for the episode."""
    print("\n" + "="*60)
    print("GENERATING ALL SHOTS FOR EPISODE 001")
    print("="*60)

    for shot_key in EPISODE_001_SHOTS:
        generate_shot(shot_key)
        print("\n")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python generate_shot.py list              - List available shots")
        print("  python generate_shot.py <shot_key>        - Generate specific shot")
        print("  python generate_shot.py all               - Generate all shots")
        print("\nExample:")
        print("  python generate_shot.py shot01_casey_hook")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "list":
        list_shots()
    elif cmd == "all":
        generate_all()
    else:
        generate_shot(cmd)
