# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Internet Improv is an animated sketch-comedy troupe that reenacts the internet's best comments, stories, and threads as mini "improv performances." This is a character-driven creative brand where recurring animated characters perform short, comedic, dramatic, or wholesome reenactments of internet threads.

**Core Concept**: An improv theatre company performing the internet.
- OP = the "prompt"
- Top comment = the "script"
- Characters = the performers
- The reenactment = the show

## The Cast

The project features 7 core characters, each with distinct personalities:

1. **Casey** — The Straight Man Narrator (reads OPs, provides structure, annoyed-but-loveable anchor)
2. **Fizz** — The Chaos Gremlin (hyperactive, unhinged, delivers wild comments)
3. **Harper** — The Wholesome One (soft, kind, sentimental, perfect for wholesome threads)
4. **Rex** — The Cynical Burn Master (deadpan, sarcastic, unimpressed)
5. **Dot** — The Lore Nerd (over-explains everything, great for ELI5/TIL)
6. **Mira** — The Dramatic Actor (theatrical, exaggerated, overacts everything)
7. **Byte** — The Meta Tech/AI Character (slightly robotic, glitchy, algorithm jokes)

Character artwork is stored in `/characters/`.

## Content Format Structure

Each episode follows a structured sketch format (20-35 seconds total):

1. Hook (1-2s): "Internet Improv presents…"
2. OP Setup (3-5s): Casey reads the prompt, cast reacts
3. Comment Reenactment (5-15s): Assigned character acts it out with exaggerated delivery
4. Improvised Chaos (3-8s): Other characters jump in, meta humor, breaking the script
5. Punchline Tag (1-3s): Final character reaction (Rex burn, Fizz chaos, Harper tears, Mira collapse)
6. Outro (1-2s): "Follow for more Internet Improv"

## Tone & Creative Direction

- Big reactions, improv energy, over-the-top acting
- Self-aware meta jokes, characters fighting over roles
- Fast-paced, snappy comedic beats
- Occasional wholesome moments and dramatic reenactments
- Exaggerated visual delivery encouraged

## Development Philosophy

When building tools/systems for this project:

- **Original IP**: All reenactments use original characters and performances (not reposted content)
- **Character-driven**: Everything should support the 7-character troupe dynamic
- **Platform-friendly**: Content should be monetizable across TikTok, IG/FB, YouTube Shorts/long-form
- **Scalable**: Build systems that can handle both short-form content and potential long-form expansions
- **Visual consistency**: Maintain distinct, cohesive art direction where one frame identifies it as Internet Improv

## Production Pipeline

### Image Generation (Stable Diffusion WebUI)

Located in `pipeline/generate_shot.py`. Uses SD WebUI API with JuggernautXL Ragnarok model.

**Settings:**
- Resolution: 1024x1024
- Sampler: DPM++ 2M Karras
- Steps: 25
- CFG Scale: 7
- Batch size: 3

**Usage:**
```bash
# Start SD WebUI with API enabled first:
# webui-user.bat with --api flag

python pipeline/generate_shot.py list              # List available shots
python pipeline/generate_shot.py shot01_casey_hook # Generate specific shot
python pipeline/generate_shot.py all               # Generate all shots
```

**Output:** `episodes/001-kevin-identity/shots/` with timestamp folders. Selected images go in `selected/` subfolder.

### Voice Generation (ElevenLabs)

Located in `pipeline/generate_audio.py`. Requires API key in `.env` file.

**Voice Design Process:**
1. Use ElevenLabs Voice Design web UI (https://elevenlabs.io/voice-design) to create custom voices
2. Describe the voice with personality traits matching the character
3. Save the voice and copy the Voice ID
4. Add Voice ID to `VOICES` dict in `generate_audio.py`

**Voice Settings (per character):**
- `stability`: Lower = more expressive/varied (0.15-0.4 for energetic, 0.8+ for deadpan)
- `similarity_boost`: How closely to match the voice (0.6-0.9)
- `style`: Emotional range (1.0 = max expressiveness)

**Script Direction Tips:**
- Use `...` for short pauses
- Use `!` and `?` for emphasis
- Avoid SSML `<break>` tags - they don't work well
- The voice design itself determines energy level more than settings
- For animated/energetic delivery, design the voice with words like "enthusiastic", "animated", "podcast host energy"

**Usage:**
```bash
python pipeline/generate_audio.py list       # List shots
python pipeline/generate_audio.py voices     # List available voices
python pipeline/generate_audio.py 01_casey_hook  # Generate specific shot
python pipeline/generate_audio.py all        # Generate all audio
```

**Output:** `episodes/001-kevin-identity/audio/`

### Animation (Runway)

Using Runway's Lip Sync feature to animate character images with voice audio.

**Workflow:**
1. Upload character image from `shots/selected/`
2. Upload corresponding audio from `audio/`
3. Generate lip-synced video

**Note:** Runway Lip Sync works best with photorealistic faces. For stylized/Pixar-style characters, results may vary. Hedra is an alternative for stylized characters.

**Credits:** Runway Standard plan ($12/mo) includes 625 credits. Lip Sync costs ~50-100 credits per generation.

### Character Voice IDs

Current voice assignments (update as voices are designed):
- Casey: `wAQta5nXit6sNLk15rnQ` (custom - needs more energy)
- Rex: TBD (should be deep, deadpan)
- Fizz: TBD (should be chaotic, fast-talking)
- Harper: TBD (warm, friendly)
- Mira: TBD (theatrical, dramatic)
- Dot: TBD (matter-of-fact, nerdy)
- Byte: TBD (slightly robotic)

## Episode Structure

Episodes are stored in `episodes/<episode-id>/` with:
- `shots/` - Generated character images
- `shots/selected/` - Final selected images (renamed 01-10)
- `audio/` - Voice audio files
- `video/` - Final animated clips (TBD)

## Future Development Areas

When adding functionality, consider these potential needs:

- Content sourcing/curation from Reddit, Twitter, forums
- Character assignment logic (matching character personality to content type)
- Script generation/adaptation from internet content
- Video compositing/editing pipeline
- Multi-platform export/formatting
