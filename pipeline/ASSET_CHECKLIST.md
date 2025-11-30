# Reference Asset Checklist

## Per-Character Asset Requirements

For each of the 7 characters, you should create and organize these reference assets:

### Tier 1: Essential (Before First Episode)

| Asset | Status | Description | File Location |
|-------|--------|-------------|---------------|
| **Main Reference** | | Clean 3/4 view, full body | `characters/{name}/reference.png` |
| **Turnaround Sheet** | | 4 angles: front, 3/4, side, back | `characters/{name}/turnaround.png` |

### Tier 2: Expression Library (For Animation)

| Asset | Status | Description | File Location |
|-------|--------|-------------|---------------|
| Neutral | | Default resting face | `characters/{name}/expressions/neutral.png` |
| Happy/Smiling | | Genuine smile | `characters/{name}/expressions/happy.png` |
| Sad/Concerned | | Downturned expression | `characters/{name}/expressions/sad.png` |
| Angry/Frustrated | | Tense, furrowed brow | `characters/{name}/expressions/angry.png` |
| Surprised | | Wide eyes, raised brows | `characters/{name}/expressions/surprised.png` |
| Character-Specific | | (See below) | `characters/{name}/expressions/...` |

### Tier 3: Pose Library (For Scene Variety)

| Asset | Status | Description | File Location |
|-------|--------|-------------|---------------|
| Standing Neutral | | Relaxed standing pose | `characters/{name}/poses/standing_neutral.png` |
| Gesturing | | Hand extended, explaining | `characters/{name}/poses/gesturing.png` |
| Arms Crossed | | Defensive/listening pose | `characters/{name}/poses/arms_crossed.png` |
| Sitting | | Seated pose (if needed) | `characters/{name}/poses/sitting.png` |

---

## Casey - Current Status

| Asset | Status | Notes |
|-------|--------|-------|
| Main Reference | ✅ Done | `characters/casey/reference.png` |
| Turnaround Sheet | ✅ Done | `characters/casey/turnaround.png` |
| Full Body Standing | ✅ Done | `characters/casey.png` |
| Expression Sheet | ❌ Needed | Generate with pipeline |
| Pose Library | ❌ Needed | Generate with pipeline |

### Casey-Specific Expressions Needed
- [ ] Neutral (reading OP)
- [ ] Exasperated (reacting to chaos)
- [ ] Deadpan (outro delivery)
- [ ] Amused (subtle reactions)
- [ ] Tired (end of episode energy)

---

## Other Characters - Current Status

### Fizz
| Asset | Status | Notes |
|-------|--------|-------|
| Main Reference | ✅ Done | `characters/fizz.png` |
| Turnaround | ❌ Needed | |
| Expressions | ❌ Needed | Excited, manic, mischievous, shocked |

### Harper
| Asset | Status | Notes |
|-------|--------|-------|
| Main Reference | ✅ Done | `characters/harper.png` |
| Turnaround | ❌ Needed | |
| Expressions | ❌ Needed | Warm smile, tearful, hopeful, concerned |

### Rex
| Asset | Status | Notes |
|-------|--------|-------|
| Main Reference | ✅ Done | `characters/rex.png` |
| Turnaround | ❌ Needed | |
| Expressions | ❌ Needed | Deadpan, unimpressed, slight smirk, eye roll |

### Dot
| Asset | Status | Notes |
|-------|--------|-------|
| Main Reference | ✅ Done | `characters/dot.png` |
| Turnaround | ❌ Needed | |
| Expressions | ❌ Needed | Focused, explaining, confused, matter-of-fact |

### Mira
| Asset | Status | Notes |
|-------|--------|-------|
| Main Reference | ✅ Done | `characters/mira.png` |
| Turnaround | ❌ Needed | |
| Expressions | ❌ Needed | Dramatic gasp, tearful, triumphant, shocked |

### Byte
| Asset | Status | Notes |
|-------|--------|-------|
| Main Reference | ❌ Missing | Need to generate |
| Turnaround | ❌ Needed | |
| Expressions | ❌ Needed | Robotic smile, glitchy, processing, error face |

---

## Full Cast Reference

| Asset | Status | Notes |
|-------|--------|-------|
| Full Cast Group Shot | ✅ Done | `characters/fullcast.png` |

---

## Priority Generation Order

### For "The Kevin Identity" Episode

1. **Casey expressions** - Shots 1, 2, 10
   - [ ] Neutral with tablet
   - [ ] Reading/focused
   - [ ] Exasperated
   - [ ] Tired/deadpan outro

2. **Rex** - Shot 3
   - [ ] Deadpan, arms crossed

3. **Fizz** - Shots 4, 6
   - [ ] Excited
   - [ ] Mischievous

4. **Harper** - Shot 5
   - [ ] Warm, encouraging

5. **Byte** - Shot 7
   - [ ] Robotic enthusiasm

6. **Mira** - Shot 8
   - [ ] Theatrical, dramatic

7. **Dot** - Shot 9
   - [ ] Matter-of-fact, serious

---

## Cropped References for img2img

When using img2img, crop your reference images appropriately:

| Input Type | Crop Region | Resolution | Use For |
|------------|-------------|------------|---------|
| Face only | Head + shoulders | 512x512 | Expression changes |
| Upper body | Waist up | 768x1024 | Medium shots |
| Full body | Entire figure | 896x1152 | Full poses |

Store cropped versions in:
```
characters/{name}/crops/
├── face.png
├── upper_body.png
└── full_body.png
```

---

## Quality Standards

Each generated asset should meet these criteria:

- [ ] Matches character design (outfit, colors, proportions)
- [ ] Clean background (solid color, no distractions)
- [ ] Good lighting (warm, even, studio-style)
- [ ] Correct style (Pixar 3D, not photorealistic or 2D)
- [ ] No anatomical errors (correct finger count, proportions)
- [ ] Face clearly visible and recognizable
- [ ] High resolution (minimum 896x1152 for portraits)
