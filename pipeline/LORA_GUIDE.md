# LoRA Integration Guide

## What is a LoRA?

LoRA (Low-Rank Adaptation) is a technique to fine-tune Stable Diffusion on specific concepts (characters, styles) without retraining the entire model. A Casey LoRA would let you generate consistent Casey images with just a trigger word.

## When to Train a LoRA

**Train a LoRA when:**
- img2img alone isn't maintaining character consistency well enough
- You're generating 50+ images of the same character
- You need precise control over character identity across many poses/scenes
- You want to simplify your prompts (just use trigger word instead of full description)

**Skip LoRA for now if:**
- You're still iterating on character design
- img2img is working well enough
- You only need a few dozen images

## LoRA File Location

Place LoRA files here:
```
/Users/nicolaisafai/dev/stable-diffusion-webui/models/Lora/
```

Example:
```
models/Lora/
├── casey_v1.safetensors
├── fizz_v1.safetensors
└── internet_improv_style.safetensors
```

## Using LoRAs in Prompts

Once a LoRA is installed, trigger it in your prompt with:
```
<lora:casey_v1:0.8>
```

The number (0.8) is the **strength**:
- 0.5-0.7: Subtle influence, blends with base model
- 0.8-1.0: Strong influence, character is dominant
- 1.0+: Can cause artifacts, use carefully

**Example full prompt with LoRA:**
```
<lora:casey_v1:0.8> casey, 3D animated male character, Pixar style, standing with tablet, neutral expression, olive blazer, cream shirt, dark jeans
```

## Training a Casey LoRA

### Prerequisites
- 10-20 high-quality Casey reference images
- Consistent style across all images
- Various angles and expressions
- kohya_ss or similar LoRA training tool

### Recommended Training Images

| Type | Count | Description |
|------|-------|-------------|
| Front view | 3-4 | Face clearly visible |
| 3/4 view | 3-4 | Your most common angle |
| Side profile | 2-3 | Clean silhouette |
| Full body | 3-4 | Shows outfit |
| Expressions | 4-5 | Different emotions |

### Training Settings (SDXL LoRA)

```yaml
# Recommended settings for character LoRA
network_dim: 32
network_alpha: 16
learning_rate: 0.0001
train_batch_size: 1
num_epochs: 10-15
resolution: 1024
optimizer: AdamW8bit
```

### Captioning Strategy

Each training image needs a caption. Use consistent format:

```
casey, adult man, short dark brown hair, thick eyebrows, brown eyes, olive blazer, cream shirt, dark jeans, [pose], [expression], 3D animated, Pixar style
```

The key is using "casey" as your trigger word consistently.

## Integrating LoRA into Pipeline

### Update generate_assets.py

Add LoRA support to prompts:

```python
def build_prompt_with_lora(base_prompt, lora_name, lora_strength=0.8):
    """Add LoRA trigger to prompt."""
    lora_trigger = f"<lora:{lora_name}:{lora_strength}>"
    return f"{lora_trigger} {base_prompt}"
```

### Update casey.json

Add LoRA configuration:

```json
{
  "character": "casey",
  "lora": {
    "name": "casey_v1",
    "strength": 0.8,
    "trigger_word": "casey"
  },
  ...
}
```

## LoRA Training Services

If you don't want to train yourself:

| Service | Cost | Turnaround |
|---------|------|------------|
| civitai.com (community) | Free-$20 | Varies |
| Replicate | ~$5-10 | Hours |
| RunPod | ~$2-5 | Hours (DIY) |

## Future LoRAs to Consider

1. **casey_v1** - Casey character LoRA
2. **fizz_v1** - Fizz character LoRA
3. **internet_improv_style** - Overall art style LoRA
4. **Character pack** - All 7 characters in one LoRA (advanced)

## Troubleshooting

**LoRA not loading:**
- Check filename matches exactly (case-sensitive)
- Ensure .safetensors extension
- Verify file is in correct Lora folder

**Character looks wrong:**
- Lower LoRA strength (try 0.6)
- Ensure base prompt still includes key details
- Check if LoRA was trained on same base model (SDXL)

**Style conflicts:**
- JuggernautXL has strong style; LoRA may fight it
- Try training LoRA on JuggernautXL directly
- Or lower LoRA strength and rely more on prompt
