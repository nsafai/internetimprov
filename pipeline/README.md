# Internet Improv - Character Generation Pipeline

## Overview

This pipeline uses Stable Diffusion WebUI (AUTOMATIC1111) with JuggernautXL to generate consistent 3D Pixar-style character assets for the "Internet Improv" animated series.

---

## Prerequisites

### Required Software
- [Stable Diffusion WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
- Python 3.10+
- curl (comes with Mac/Linux, install via Git Bash or WSL on Windows)

### Required Model
- **JuggernautXL Ragnarok** (`juggernautXL_ragnarokBy.safetensors`)
- Place in: `stable-diffusion-webui/models/Stable-diffusion/`

---

## Setup

### Step 1: Apply API Bug Fix

The WebUI API has a bug that crashes on reload. Apply this fix before first run.

**File:** `stable-diffusion-webui/modules/api/api.py` (around line 207)

**Find this code:**
```python
self.router = APIRouter()
self.app = app
self.queue_lock = queue_lock
api_middleware(self.app)
```

**Replace with:**
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

### Step 2: Start WebUI with API

**Mac/Linux:**
```bash
cd /path/to/stable-diffusion-webui
./webui.sh --api
```

**Windows (Command Prompt):**
```cmd
cd C:\path\to\stable-diffusion-webui
webui-user.bat
```
Note: Edit `webui-user.bat` and add `--api` to `COMMANDLINE_ARGS`:
```
set COMMANDLINE_ARGS=--api
```

**Windows (PowerShell):**
```powershell
cd C:\path\to\stable-diffusion-webui
.\webui-user.bat
```

Wait for: `Running on local URL: http://127.0.0.1:7860`

### Step 3: Test API Connection

**Mac/Linux:**
```bash
curl -s http://127.0.0.1:7860/sdapi/v1/sd-models | head -c 200
```

**Windows (PowerShell):**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:7860/sdapi/v1/sd-models" | ConvertTo-Json
```

**Windows (Command Prompt with curl):**
```cmd
curl -s http://127.0.0.1:7860/sdapi/v1/sd-models
```

---

## Configuration

| Setting | Value |
|---------|-------|
| **Primary Model** | `juggernautXL_ragnarokBy.safetensors` |
| **Default Resolution** | 896x1152 (Portrait) / 1024x1024 (Square) |
| **Sampler** | DPM++ 2M Karras |
| **CFG Scale** | 7 |
| **Steps** | 20 |
| **Batch Size** | 1-4 |
| **img2img Denoising** | 0.5 |
| **API Endpoint** | `http://127.0.0.1:7860` |

### Performance (Apple Silicon)
- ~1.5 min per image at 896x1152
- ~6 min for batch of 4

### Performance (NVIDIA GPU)
- ~15-30 sec per image (varies by GPU)
- ~1-2 min for batch of 4

---

## Quick Generate: CLI Commands

### Create Payload File

**Mac/Linux:**
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
  "batch_size": 1,
  "n_iter": 1,
  "seed": -1,
  "send_images": true,
  "save_images": false
}
EOF
```

**Windows (PowerShell):**
```powershell
@'
{
  "prompt": "3D animated male character, Pixar Disney style, stylized proportions, soft 3D render, smooth skin texture, warm studio lighting, clean solid background, full body shot, standing pose, adult man late 20s, short dark brown hair side-parted, thick expressive dark eyebrows, brown eyes, warm tan skin, slight stubble, friendly approachable face, slim athletic build, olive khaki blazer jacket, cream beige button-up collared shirt, brown leather belt, dark navy blue jeans, brown leather oxford shoes, dark wristwatch on left wrist, standing naturally, one hand in pocket, relaxed confident stance, neutral calm expression, slight knowing look, relaxed face, high quality, detailed, professional 3D animation style, Pixar aesthetic",
  "negative_prompt": "photorealistic, hyperrealistic, photograph, real human, anime, 2d, flat, cartoon, sketch, painting, watercolor, blurry, low quality, bad anatomy, extra fingers, mutated hands, poorly drawn face, distorted face, ugly, duplicate, morbid, dark, gritty, horror, scary, nsfw, nude, text, watermark, signature, logo, multiple characters, crowd",
  "sampler_name": "DPM++ 2M Karras",
  "steps": 20,
  "cfg_scale": 7,
  "width": 896,
  "height": 1152,
  "batch_size": 1,
  "n_iter": 1,
  "seed": -1,
  "send_images": true,
  "save_images": false
}
'@ | Out-File -FilePath "$env:TEMP\casey_payload.json" -Encoding UTF8
```

### Generate Image

**Mac/Linux:**
```bash
# Generate and save response to file
curl -s -X POST "http://127.0.0.1:7860/sdapi/v1/txt2img" \
  -H "Content-Type: application/json" \
  -d @/tmp/casey_payload.json \
  -o /tmp/casey_response.json

# Decode the base64 image
python3 -c "
import json, base64
from datetime import datetime
with open('/tmp/casey_response.json') as f:
    data = json.load(f)
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
for i, img in enumerate(data.get('images', [])):
    filename = f'casey_{timestamp}_{i:02d}.png'
    with open(filename, 'wb') as f:
        f.write(base64.b64decode(img))
    print(f'Saved: {filename}')
info = json.loads(data.get('info', '{}'))
print(f'Seed: {info.get(\"seed\", \"unknown\")}')
"
```

**Windows (PowerShell):**
```powershell
# Generate and save response
curl.exe -s -X POST "http://127.0.0.1:7860/sdapi/v1/txt2img" `
  -H "Content-Type: application/json" `
  -d "@$env:TEMP\casey_payload.json" `
  -o "$env:TEMP\casey_response.json"

# Decode the base64 image
python -c @"
import json, base64
from datetime import datetime
with open(r'$env:TEMP\casey_response.json') as f:
    data = json.load(f)
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
for i, img in enumerate(data.get('images', [])):
    filename = f'casey_{timestamp}_{i:02d}.png'
    with open(filename, 'wb') as f:
        f.write(base64.b64decode(img))
    print(f'Saved: {filename}')
info = json.loads(data.get('info', '{}'))
print(f'Seed: {info.get(\"seed\", \"unknown\")}')
"@
```

### Check Progress (while generating)

**Mac/Linux:**
```bash
curl -s "http://127.0.0.1:7860/sdapi/v1/progress" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Progress: {d.get(\"progress\", 0)*100:.1f}%')"
```

**Windows (PowerShell):**
```powershell
(Invoke-RestMethod -Uri "http://127.0.0.1:7860/sdapi/v1/progress").progress * 100
```

---

## Folder Structure

```
internetimprov/
├── characters/
│   ├── casey/
│   │   ├── reference.png          # Primary reference image
│   │   ├── turnaround.png         # 4-angle turnaround sheet
│   │   ├── expressions/           # Expression variants
│   │   └── poses/                 # Pose library
│   ├── fizz/
│   ├── harper/
│   ├── rex/
│   ├── dot/
│   ├── mira/
│   └── byte/
├── episodes/
│   └── 001-kevin-identity/
│       ├── script.md              # Episode script
│       ├── shot-plan.md           # Shot-by-shot breakdown
│       ├── shots/                 # Generated shots
│       └── renders/               # Final animated renders
├── pipeline/
│   ├── README.md                  # This file
│   ├── QUICK_START.md             # Quick reference
│   ├── ASSET_CHECKLIST.md         # Character asset tracker
│   ├── IMG2IMG_SETTINGS.md        # img2img guide
│   ├── LORA_GUIDE.md              # LoRA training guide
│   ├── generate_assets.py         # Python automation script
│   ├── prompts/                   # Prompt templates
│   │   └── casey.json
│   ├── seeds/                     # Seed bank (golden seeds)
│   └── logs/                      # Generation logs
└── models/
    └── loras/                     # Future LoRA files
```

---

## File Naming Convention

```
{character}_{pose}_{YYYYMMDD}_{HHMMSS}_{index}.png
```

Example: `casey_standing_20241129_143052_00.png`

---

## API Reference

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

### Other Useful Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| /sdapi/v1/sd-models | GET | List available models |
| /sdapi/v1/samplers | GET | List available samplers |
| /sdapi/v1/options | GET | Get current settings |
| /sdapi/v1/progress | GET | Check generation progress |
| /sdapi/v1/interrupt | POST | Stop current generation |

---

## Troubleshooting

### "Cannot add middleware after an application has started"
Apply the API bug fix described in Setup Step 1.

### curl: command not found (Windows)
- Install Git for Windows (includes Git Bash with curl)
- Or use PowerShell's `Invoke-RestMethod` instead
- Or install curl via chocolatey: `choco install curl`

### Generation hangs or takes too long
- Mac (MPS): ~1.5 min per image is normal at 896x1152
- Reduce resolution to 768x1024 for faster iteration
- Reduce batch_size to 1 for quicker feedback

### Images not saving
Use `send_images: true` and decode the base64 response yourself (as shown in CLI commands above). The `save_images` parameter saves to WebUI's output folder, not a custom location.

### Model not found
Ensure JuggernautXL is in `stable-diffusion-webui/models/Stable-diffusion/` and refresh models in the WebUI interface.
