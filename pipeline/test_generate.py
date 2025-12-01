#!/usr/bin/env python3
"""Quick test: Generate 2 Casey images"""

import requests
import base64
import json
from pathlib import Path
from datetime import datetime

API_URL = "http://127.0.0.1:7860"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "characters" / "casey" / "test_outputs"

# Load Casey prompt
prompt_file = Path(__file__).resolve().parent / "prompts" / "casey.json"
with open(prompt_file) as f:
    casey = json.load(f)

# Build full prompt
prompt = ", ".join([
    casey["base_prompt"],
    casey["identity_tags"],
    casey["outfit_tags"],
    casey["poses"]["standing_neutral"],
    casey["expressions"]["neutral"],
    casey["style_tags"]
])

negative = casey["negative_prompt_default"]

settings = casey["recommended_settings"]

def check_api():
    try:
        r = requests.get(f"{API_URL}/sdapi/v1/sd-models", timeout=5)
        return r.status_code == 200
    except:
        return False

def generate():
    print("Checking API...")
    if not check_api():
        print("ERROR: SD WebUI API not running!")
        print("Start it with: webui-user.bat")
        return

    print("API connected!")

    # Check current model
    r = requests.get(f"{API_URL}/sdapi/v1/options")
    current_model = r.json().get("sd_model_checkpoint", "Unknown")
    print(f"Current model: {current_model}")

    # Switch to Juggernaut if needed
    if "juggernaut" not in current_model.lower():
        print("Switching to JuggernautXL...")
        requests.post(f"{API_URL}/sdapi/v1/options", json={
            "sd_model_checkpoint": settings["model"]
        })
        print("Model switched!")

    print(f"\nGenerating 2 Casey images...")
    print(f"Prompt: {prompt[:80]}...")

    payload = {
        "prompt": prompt,
        "negative_prompt": negative,
        "sampler_name": settings["sampler"],
        "steps": settings["steps"],
        "cfg_scale": settings["cfg_scale"],
        "width": settings["width"],
        "height": settings["height"],
        "batch_size": 2,  # Generate 2 images
        "seed": -1,
    }

    print("\nSending request to API...")
    r = requests.post(f"{API_URL}/sdapi/v1/txt2img", json=payload)

    if r.status_code == 200:
        result = r.json()
        images = result["images"]
        info = json.loads(result.get("info", "{}"))
        seed = info.get("seed", "unknown")

        # Save images
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        for i, img_data in enumerate(images):
            filename = f"casey_test_{timestamp}_{i:02d}.png"
            filepath = OUTPUT_DIR / filename

            img_bytes = base64.b64decode(img_data)
            with open(filepath, 'wb') as f:
                f.write(img_bytes)

            print(f"Saved: {filepath}")

        print(f"\nDone! Seed used: {seed}")
        print(f"Images saved to: {OUTPUT_DIR}")
    else:
        print(f"ERROR: {r.status_code}")
        print(r.text)

if __name__ == "__main__":
    generate()
