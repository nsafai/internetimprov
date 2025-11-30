# Internet Improv - Quick Start Guide

## Prerequisites

**Required fix for WebUI API bug:**

Before first run, apply this patch to fix the API middleware error:

Edit `/Users/nicolaisafai/dev/stable-diffusion-webui/modules/api/api.py` line ~207-210.

Change:
```python
self.router = APIRouter()
self.app = app
self.queue_lock = queue_lock
api_middleware(self.app)
```

To:
```python
self.router = APIRouter()
self.app = app
self.queue_lock = queue_lock
try:
    api_middleware(self.app)
except RuntimeError as e:
    if "Cannot add middleware after an application has started" in str(e):
        print("API middleware warning: middleware not added (app already started). API will still work.")
    else:
        raise
```

---

## 1. Start WebUI with API

```bash
cd /Users/nicolaisafai/dev/stable-diffusion-webui
./webui.sh --api
```

Wait for: `Running on local URL: http://127.0.0.1:7860`

**Note:** On Mac (Apple Silicon), SDXL runs on MPS (Metal). Expect ~2-3 min per image at 896x1152.

---

## 2. Test API Connection

```bash
curl -s http://127.0.0.1:7860/sdapi/v1/sd-models
```

Should return JSON with your installed models.

Check current model:
```bash
curl -s http://127.0.0.1:7860/sdapi/v1/options | python3 -c "import sys,json; print(json.load(sys.stdin).get('sd_model_checkpoint'))"
```

---

## 3. Generate Casey via CLI

**Step 1:** Create the payload file:

```bash
cat > /tmp/casey_payload.json << 'EOF'
{
  "prompt": "3D animated male character, Pixar Disney style, stylized proportions, soft 3D render, smooth skin texture, warm studio lighting, clean solid background, full body shot, standing pose, adult man late 20s, short dark brown hair side-parted, thick expressive dark eyebrows, brown eyes, warm tan skin, slight stubble, friendly approachable face, slim athletic build, olive khaki blazer jacket, cream beige button-up collared shirt, brown leather belt, dark navy blue jeans, brown leather oxford shoes, dark wristwatch on left wrist, standing naturally, one hand in pocket, relaxed confident stance, neutral calm expression, slight knowing look, relaxed face, high quality, detailed, professional 3D animation style, Pixar aesthetic",
  "negative_prompt": "photorealistic, hyperrealistic, photograph, real human, anime, 2d, flat, cartoon, sketch, painting, watercolor, blurry, low quality, bad anatomy, extra fingers, mutated hands, poorly drawn face, distorted face, ugly, duplicate, morbid, dark, gritty, horror, scary, nsfw, nude, text, watermark, signature, logo, multiple characters, crowd",
  "sampler_name": "DPM++ 2M Karras",
  "steps": 20,
  "cfg_scale": 7,
  "width": 896,
  "height": 1152,
  "batch_size": 4,
  "n_iter": 1,
  "seed": -1,
  "send_images": true,
  "save_images": false
}
EOF
```

**Step 2:** Run generation and save images:

```bash
cd /Users/nicolaisafai/Desktop/internetimprov/characters/casey/poses

curl -s -X POST "http://127.0.0.1:7860/sdapi/v1/txt2img" \
  -H "Content-Type: application/json" \
  -d @/tmp/casey_payload.json | python3 << 'PYEOF'
import sys, json, base64
from datetime import datetime

data = json.load(sys.stdin)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

for i, img in enumerate(data.get("images", [])):
    filename = f"casey_standing_{timestamp}_{i:02d}.png"
    with open(filename, "wb") as f:
        f.write(base64.b64decode(img))
    print(f"Saved: {filename}")

info = json.loads(data.get("info", "{}"))
print(f"Seed: {info.get('seed', 'unknown')}")
PYEOF
```

**Time estimate:** ~8-12 min for batch of 4 on Mac M1/M2/M3

---

## 4. Check Generation Progress

While generating, check progress:

```bash
curl -s "http://127.0.0.1:7860/sdapi/v1/progress" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Progress: {d.get(\"progress\", 0)*100:.1f}%')"
```

---

## 5. API Parameter Reference

### txt2img Endpoint

`POST http://127.0.0.1:7860/sdapi/v1/txt2img`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| prompt | string | "" | Main prompt |
| negative_prompt | string | "" | What to avoid |
| sampler_name | string | "Euler" | Sampler (use "DPM++ 2M Karras") |
| steps | int | 50 | Sampling steps |
| cfg_scale | float | 7.0 | Prompt guidance strength |
| width | int | 512 | Image width |
| height | int | 512 | Image height |
| batch_size | int | 1 | Images per batch |
| n_iter | int | 1 | Number of batches |
| seed | int | -1 | Random seed (-1 = random) |
| send_images | bool | true | Return images in response |
| save_images | bool | false | Save to WebUI outputs folder |

### img2img Endpoint

`POST http://127.0.0.1:7860/sdapi/v1/img2img`

Additional parameters:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| init_images | list[str] | required | Base64-encoded input images |
| denoising_strength | float | 0.75 | How much to change (0=none, 1=full) |
| resize_mode | int | 0 | 0=scale, 1=crop |

---

## 6. Optimized Casey Prompt

### Full Prompt:
```
3D animated male character, Pixar Disney style, stylized proportions, soft 3D render, smooth skin texture, warm studio lighting, clean solid background, full body shot, standing pose, adult man late 20s, short dark brown hair side-parted, thick expressive dark eyebrows, brown eyes, warm tan skin, slight stubble, friendly approachable face, slim athletic build, olive khaki blazer jacket, cream beige button-up collared shirt, brown leather belt, dark navy blue jeans, brown leather oxford shoes, dark wristwatch on left wrist, standing naturally, one hand in pocket, relaxed confident stance, neutral calm expression, slight knowing look, relaxed face, high quality, detailed, professional 3D animation style, Pixar aesthetic
```

### Negative Prompt:
```
photorealistic, hyperrealistic, photograph, real human, anime, 2d, flat, cartoon, sketch, painting, watercolor, blurry, low quality, bad anatomy, extra fingers, mutated hands, poorly drawn face, distorted face, ugly, duplicate, morbid, dark, gritty, horror, scary, nsfw, nude, text, watermark, signature, logo, multiple characters, crowd
```

---

## 7. Expression Variations

Swap the expression portion of the prompt:

| Expression | Prompt Fragment |
|------------|-----------------|
| Neutral | `neutral calm expression, slight knowing look, relaxed face` |
| Exasperated | `exasperated expression, tired eyes, slight frown, annoyed but patient` |
| Deadpan | `deadpan expression, flat unamused stare, minimal emotion` |
| Amused | `subtly amused expression, slight smirk, raised eyebrow` |
| Reading | `looking down at tablet, focused expression, reading intently` |

---

## 8. Pose Variations

Swap the pose portion of the prompt:

| Pose | Prompt Fragment |
|------|-----------------|
| Standing neutral | `standing naturally, one hand in pocket, relaxed confident stance` |
| With tablet | `standing holding tablet in right hand, looking at viewer` |
| Reading tablet | `standing holding tablet with both hands, looking down at screen` |
| Gesturing | `standing with one hand gesturing outward, explaining something` |
| Arms crossed | `standing with arms crossed, slightly defensive but attentive` |

---

## 9. img2img Example (Character Consistency)

```bash
# Encode reference image to base64
REF_IMAGE=$(base64 -i /Users/nicolaisafai/Desktop/internetimprov/characters/casey/reference.png)

cat > /tmp/casey_img2img.json << EOF
{
  "init_images": ["$REF_IMAGE"],
  "prompt": "3D animated male character, Pixar Disney style... [full prompt]",
  "negative_prompt": "...",
  "sampler_name": "DPM++ 2M Karras",
  "steps": 20,
  "cfg_scale": 7,
  "width": 896,
  "height": 1152,
  "denoising_strength": 0.5,
  "batch_size": 4,
  "seed": -1
}
EOF

curl -s -X POST "http://127.0.0.1:7860/sdapi/v1/img2img" \
  -H "Content-Type: application/json" \
  -d @/tmp/casey_img2img.json | python3 [same decode script]
```

---

## 10. Output Locations

| Type | Location |
|------|----------|
| Casey poses | `characters/casey/poses/` |
| Casey expressions | `characters/casey/expressions/` |
| Episode shots | `episodes/001-kevin-identity/shots/` |
| Generation logs | `pipeline/logs/` |
| Saved seeds | `pipeline/seeds/` |

---

## 11. Performance Tips (Mac)

| Setting | Faster | Quality Impact |
|---------|--------|----------------|
| `batch_size: 1` | See results sooner | None |
| `steps: 15` | ~25% faster | Minimal |
| `width: 768, height: 1024` | ~30% faster | Slightly lower res |

For production quality, use full settings. For iteration/testing, reduce batch_size to 1.

---

## 12. Useful API Endpoints

```bash
# List available models
curl -s http://127.0.0.1:7860/sdapi/v1/sd-models

# List samplers
curl -s http://127.0.0.1:7860/sdapi/v1/samplers

# Get current settings
curl -s http://127.0.0.1:7860/sdapi/v1/options

# Check progress
curl -s http://127.0.0.1:7860/sdapi/v1/progress

# Interrupt generation
curl -s -X POST http://127.0.0.1:7860/sdapi/v1/interrupt
```
