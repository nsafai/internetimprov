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

## Future Development Areas

When adding functionality, consider these potential needs:

- Content sourcing/curation from Reddit, Twitter, forums
- Character assignment logic (matching character personality to content type)
- Script generation/adaptation from internet content
- Animation pipeline tools
- Episode structure templates
- Voice/dialogue generation aligned to character personalities
- Visual design systems for consistent character representation
- Multi-platform export/formatting
