#!/usr/bin/env python3
"""
Internet Improv - Character Asset Generation Script
Generates consistent character images using Stable Diffusion WebUI API
"""

import requests
import base64
import json
import os
from datetime import datetime
from pathlib import Path

# =============================================================================
# CONFIGURATION
# =============================================================================

API_URL = "http://127.0.0.1:7860"
BASE_DIR = Path(__file__).resolve().parent.parent  # internetimprov folder
PIPELINE_DIR = BASE_DIR / "pipeline"
CHARACTERS_DIR = BASE_DIR / "characters"
EPISODES_DIR = BASE_DIR / "episodes"

# Default settings (from your configuration)
DEFAULTS = {
    "model": "juggernautXL_ragnarokBy.safetensors",
    "sampler": "DPM++ 2M Karras",
    "steps": 20,
    "cfg_scale": 7,
    "width": 896,
    "height": 1152,
    "batch_size": 4,
    "denoising_strength": 0.5,  # For img2img
}

# Default negative prompt
DEFAULT_NEGATIVE = (
    "photorealistic, hyperrealistic, photograph, real human, anime, 2d, flat, "
    "cartoon, sketch, painting, watercolor, blurry, low quality, bad anatomy, "
    "extra fingers, mutated hands, poorly drawn face, distorted face, ugly, "
    "duplicate, morbid, dark, gritty, horror, scary, nsfw, nude, text, "
    "watermark, signature, logo, multiple characters, crowd"
)

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def check_api():
    """Check if WebUI API is running."""
    try:
        r = requests.get(f"{API_URL}/sdapi/v1/sd-models", timeout=5)
        return r.status_code == 200
    except requests.exceptions.RequestException:
        return False


def get_current_model():
    """Get currently loaded model."""
    try:
        r = requests.get(f"{API_URL}/sdapi/v1/options")
        return r.json().get("sd_model_checkpoint", "Unknown")
    except:
        return "Unknown"


def set_model(model_name):
    """Switch to specified model."""
    payload = {"sd_model_checkpoint": model_name}
    r = requests.post(f"{API_URL}/sdapi/v1/options", json=payload)
    return r.status_code == 200


def load_character_prompt(character_name):
    """Load character prompt data from JSON."""
    prompt_file = PIPELINE_DIR / "prompts" / f"{character_name}.json"
    if prompt_file.exists():
        with open(prompt_file, 'r') as f:
            return json.load(f)
    return None


def generate_timestamp():
    """Generate timestamp for filename."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def save_images(images, character, pose, output_dir):
    """Save generated images with metadata."""
    timestamp = generate_timestamp()
    saved_files = []

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for i, img_data in enumerate(images):
        filename = f"{character}_{pose}_{timestamp}_{i:02d}.png"
        filepath = output_path / filename

        # Decode and save image
        img_bytes = base64.b64decode(img_data)
        with open(filepath, 'wb') as f:
            f.write(img_bytes)

        saved_files.append(filepath)
        print(f"  Saved: {filename}")

    return saved_files


def log_generation(character, prompt, settings, seed, output_files):
    """Log generation metadata for reproducibility."""
    log_dir = PIPELINE_DIR / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "character": character,
        "prompt": prompt,
        "settings": settings,
        "seed": seed,
        "output_files": [str(f) for f in output_files]
    }

    log_file = log_dir / f"{character}_generations.jsonl"
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + "\n")


def save_seed(character, seed, description):
    """Save a 'golden seed' for reuse."""
    seeds_dir = PIPELINE_DIR / "seeds"
    seeds_dir.mkdir(parents=True, exist_ok=True)

    seeds_file = seeds_dir / f"{character}_seeds.json"

    seeds = {}
    if seeds_file.exists():
        with open(seeds_file, 'r') as f:
            seeds = json.load(f)

    seeds[str(seed)] = {
        "description": description,
        "saved_at": datetime.now().isoformat()
    }

    with open(seeds_file, 'w') as f:
        json.dump(seeds, f, indent=2)

    print(f"  Seed {seed} saved as '{description}'")


# =============================================================================
# GENERATION FUNCTIONS
# =============================================================================

def txt2img(prompt, negative_prompt, settings, seed=-1):
    """Generate image from text prompt."""
    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "sampler_name": settings.get("sampler", DEFAULTS["sampler"]),
        "steps": settings.get("steps", DEFAULTS["steps"]),
        "cfg_scale": settings.get("cfg_scale", DEFAULTS["cfg_scale"]),
        "width": settings.get("width", DEFAULTS["width"]),
        "height": settings.get("height", DEFAULTS["height"]),
        "batch_size": settings.get("batch_size", DEFAULTS["batch_size"]),
        "seed": seed,
    }

    r = requests.post(f"{API_URL}/sdapi/v1/txt2img", json=payload)

    if r.status_code == 200:
        result = r.json()
        return result["images"], result.get("info", "{}")
    else:
        print(f"Error: {r.status_code} - {r.text}")
        return None, None


def img2img(init_image_path, prompt, negative_prompt, settings, seed=-1):
    """Generate image variation from reference image."""
    # Load and encode reference image
    with open(init_image_path, 'rb') as f:
        init_image = base64.b64encode(f.read()).decode('utf-8')

    payload = {
        "init_images": [init_image],
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "sampler_name": settings.get("sampler", DEFAULTS["sampler"]),
        "steps": settings.get("steps", DEFAULTS["steps"]),
        "cfg_scale": settings.get("cfg_scale", DEFAULTS["cfg_scale"]),
        "width": settings.get("width", DEFAULTS["width"]),
        "height": settings.get("height", DEFAULTS["height"]),
        "batch_size": settings.get("batch_size", DEFAULTS["batch_size"]),
        "denoising_strength": settings.get("denoising_strength", DEFAULTS["denoising_strength"]),
        "seed": seed,
    }

    r = requests.post(f"{API_URL}/sdapi/v1/img2img", json=payload)

    if r.status_code == 200:
        result = r.json()
        return result["images"], result.get("info", "{}")
    else:
        print(f"Error: {r.status_code} - {r.text}")
        return None, None


# =============================================================================
# INTERACTIVE PROMPTS
# =============================================================================

def ask_yes_no(question, default="y"):
    """Ask a yes/no question."""
    suffix = "[Y/n]" if default.lower() == "y" else "[y/N]"
    response = input(f"{question} {suffix}: ").strip().lower()
    if not response:
        return default.lower() == "y"
    return response in ("y", "yes")


def ask_choice(question, options, default=None):
    """Ask user to choose from options."""
    print(f"\n{question}")
    for i, opt in enumerate(options, 1):
        marker = " (default)" if default and opt == default else ""
        print(f"  {i}. {opt}{marker}")

    while True:
        response = input("Enter number or value: ").strip()
        if not response and default:
            return default
        try:
            idx = int(response) - 1
            if 0 <= idx < len(options):
                return options[idx]
        except ValueError:
            pass
        # Allow direct value input
        if response:
            return response


def ask_seed():
    """Ask user for seed preference."""
    print("\nSeed options:")
    print("  1. Random (new seed)")
    print("  2. Enter specific seed")
    print("  3. Use saved seed")

    choice = input("Choose [1]: ").strip() or "1"

    if choice == "1":
        return -1
    elif choice == "2":
        seed = input("Enter seed number: ").strip()
        return int(seed) if seed else -1
    elif choice == "3":
        # List saved seeds
        print("\nSaved seeds would be listed here...")
        seed = input("Enter seed number: ").strip()
        return int(seed) if seed else -1
    return -1


def ask_negative_prompt():
    """Ask user for negative prompt."""
    print(f"\nDefault negative prompt:")
    print(f"  {DEFAULT_NEGATIVE[:80]}...")

    if ask_yes_no("Use default negative prompt?", "y"):
        return DEFAULT_NEGATIVE
    else:
        custom = input("Enter custom negative prompt: ").strip()
        return custom if custom else DEFAULT_NEGATIVE


def ask_sampler():
    """Ask user for sampler."""
    samplers = [
        "DPM++ 2M Karras",
        "DPM++ SDE Karras",
        "DPM++ 2M SDE Karras",
        "Euler a",
        "DDIM"
    ]
    return ask_choice("Select sampler:", samplers, default="DPM++ 2M Karras")


# =============================================================================
# CHARACTER GENERATION WORKFLOWS
# =============================================================================

def build_casey_prompt(pose="standing_neutral", expression="neutral"):
    """Build full prompt for Casey."""
    char_data = load_character_prompt("casey")

    if not char_data:
        print("Warning: casey.json not found, using hardcoded prompt")
        char_data = {
            "base_prompt": "3D animated male character, Pixar Disney style",
            "identity_tags": "adult man late 20s, short dark brown hair, thick eyebrows, brown eyes",
            "outfit_tags": "olive blazer, cream shirt, dark jeans, brown shoes",
            "style_tags": "high quality, professional 3D animation",
            "expressions": {"neutral": "neutral calm expression"},
            "poses": {"standing_neutral": "standing naturally, relaxed stance"}
        }

    # Get expression and pose tags
    expr_tag = char_data.get("expressions", {}).get(expression, "neutral expression")
    pose_tag = char_data.get("poses", {}).get(pose, "standing naturally")

    # Build full prompt
    prompt_parts = [
        char_data.get("base_prompt", ""),
        char_data.get("identity_tags", ""),
        char_data.get("outfit_tags", ""),
        pose_tag,
        expr_tag,
        char_data.get("style_tags", "")
    ]

    return ", ".join(filter(None, prompt_parts))


def generate_casey(pose="standing_neutral", expression="neutral", output_dir=None, mode="txt2img"):
    """Interactive Casey generation."""

    print("\n" + "="*60)
    print("CASEY GENERATION")
    print("="*60)

    # Build prompt
    prompt = build_casey_prompt(pose, expression)
    print(f"\nPrompt preview:")
    print(f"  {prompt[:100]}...")

    # Get settings interactively
    print("\n--- Settings ---")
    sampler = ask_sampler()
    negative_prompt = ask_negative_prompt()
    seed = ask_seed()

    settings = {
        **DEFAULTS,
        "sampler": sampler,
    }

    # Confirm before generating
    print(f"\n--- Generation Settings ---")
    print(f"  Mode: {mode}")
    print(f"  Sampler: {sampler}")
    print(f"  Steps: {settings['steps']}")
    print(f"  CFG: {settings['cfg_scale']}")
    print(f"  Size: {settings['width']}x{settings['height']}")
    print(f"  Batch: {settings['batch_size']}")
    print(f"  Seed: {'Random' if seed == -1 else seed}")

    if not ask_yes_no("\nProceed with generation?", "y"):
        print("Cancelled.")
        return

    # Generate
    print("\nGenerating...")

    if mode == "txt2img":
        images, info = txt2img(prompt, negative_prompt, settings, seed)
    else:
        ref_image = CHARACTERS_DIR / "casey" / "reference.png"
        if not ref_image.exists():
            print(f"Error: Reference image not found at {ref_image}")
            return
        images, info = img2img(ref_image, prompt, negative_prompt, settings, seed)

    if images:
        # Determine output directory
        if output_dir is None:
            output_dir = CHARACTERS_DIR / "casey" / "poses"

        # Save images
        saved = save_images(images, "casey", pose, output_dir)

        # Parse seed from info
        try:
            info_dict = json.loads(info)
            actual_seed = info_dict.get("seed", seed)
        except:
            actual_seed = seed

        # Log generation
        log_generation("casey", prompt, settings, actual_seed, saved)

        print(f"\nGenerated {len(saved)} images")
        print(f"Seed used: {actual_seed}")

        # Offer to save seed
        if ask_yes_no("Save this seed as a 'golden seed'?", "n"):
            desc = input("Description for this seed: ").strip() or f"{pose}_{expression}"
            save_seed("casey", actual_seed, desc)
    else:
        print("Generation failed!")


# =============================================================================
# EPISODE SHOT GENERATION
# =============================================================================

def generate_episode_shots(episode_id, shot_plan):
    """Generate all shots for an episode based on shot plan."""

    print(f"\n{'='*60}")
    print(f"EPISODE SHOT GENERATION: {episode_id}")
    print(f"{'='*60}")

    output_dir = EPISODES_DIR / episode_id / "shots"
    output_dir.mkdir(parents=True, exist_ok=True)

    for i, shot in enumerate(shot_plan, 1):
        print(f"\n--- Shot {i}/{len(shot_plan)}: {shot['character']} ---")
        print(f"  Description: {shot['description']}")
        print(f"  Expression: {shot['expression']}")

        if not ask_yes_no(f"Generate this shot?", "y"):
            continue

        # Build prompt for this character
        # (In full implementation, would load character-specific prompts)
        prompt = build_casey_prompt(shot.get('pose', 'standing_neutral'), shot['expression'])

        # Override character in prompt if not Casey
        if shot['character'] != 'casey':
            print(f"  Note: {shot['character']} prompt not yet configured, using Casey as template")

        negative_prompt = ask_negative_prompt()
        seed = ask_seed()

        settings = {**DEFAULTS, "sampler": ask_sampler()}

        images, info = txt2img(prompt, negative_prompt, settings, seed)

        if images:
            saved = save_images(images, shot['character'], shot['shot_id'], output_dir)
            print(f"  Saved {len(saved)} images for shot {i}")


# =============================================================================
# MAIN MENU
# =============================================================================

def main():
    """Main interactive menu."""

    print("\n" + "="*60)
    print("INTERNET IMPROV - Asset Generation Pipeline")
    print("="*60)

    # Check API
    if not check_api():
        print("\nERROR: WebUI API not accessible!")
        print("Start WebUI with: ./webui.sh --api")
        print(f"Expected at: {API_URL}")
        return

    print(f"\nAPI connected: {API_URL}")
    print(f"Current model: {get_current_model()}")

    while True:
        print("\n--- Main Menu ---")
        print("1. Generate Casey (txt2img)")
        print("2. Generate Casey variation (img2img)")
        print("3. Generate episode shots")
        print("4. Switch model")
        print("5. View/manage saved seeds")
        print("q. Quit")

        choice = input("\nSelect option: ").strip().lower()

        if choice == "1":
            pose = ask_choice("Select pose:", [
                "standing_neutral", "standing_tablet", "reading_tablet",
                "gesturing", "arms_crossed", "hand_on_hip"
            ], default="standing_neutral")

            expression = ask_choice("Select expression:", [
                "neutral", "exasperated", "deadpan", "amused",
                "surprised", "frustrated", "reading"
            ], default="neutral")

            generate_casey(pose, expression, mode="txt2img")

        elif choice == "2":
            pose = ask_choice("Select pose:", [
                "standing_neutral", "standing_tablet", "reading_tablet",
                "gesturing", "arms_crossed", "hand_on_hip"
            ], default="standing_neutral")

            expression = ask_choice("Select expression:", [
                "neutral", "exasperated", "deadpan", "amused",
                "surprised", "frustrated", "reading"
            ], default="neutral")

            generate_casey(pose, expression, mode="img2img")

        elif choice == "3":
            # Example shot plan for Kevin Identity
            shot_plan = [
                {"shot_id": "shot01", "character": "casey", "expression": "neutral", "description": "Casey reading OP"},
                {"shot_id": "shot02", "character": "rex", "expression": "deadpan", "description": "Rex delivers options"},
                {"shot_id": "shot03", "character": "fizz", "expression": "excited", "description": "Fizz agrees"},
            ]
            generate_episode_shots("001-kevin-identity", shot_plan)

        elif choice == "4":
            models = ["juggernautXL_ragnarokBy.safetensors", "sd_xl_base_1.0.safetensors"]
            model = ask_choice("Select model:", models)
            print(f"Switching to {model}...")
            if set_model(model):
                print("Model switched successfully!")
            else:
                print("Failed to switch model.")

        elif choice == "5":
            seeds_dir = PIPELINE_DIR / "seeds"
            if seeds_dir.exists():
                for f in seeds_dir.glob("*.json"):
                    print(f"\n{f.stem}:")
                    with open(f) as sf:
                        seeds = json.load(sf)
                        for seed, data in seeds.items():
                            print(f"  {seed}: {data['description']}")
            else:
                print("No saved seeds yet.")

        elif choice == "q":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
