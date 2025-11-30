# img2img Settings for Character Consistency

## Overview

img2img takes an existing image (your Casey reference) and generates variations while maintaining identity. The key parameter is **denoising strength**.

## Denoising Strength Guide

| Strength | Effect | Use Case |
|----------|--------|----------|
| **0.3-0.4** | Minimal changes | Same pose, tweak expression or lighting |
| **0.45-0.55** | Moderate changes | New expression, slight pose variation |
| **0.55-0.65** | Significant changes | Different pose, same identity |
| **0.65-0.75** | Major changes | New angle/composition, identity may drift |

## Recommended Settings for Casey

### Expression Change (Same Pose)
```json
{
  "denoising_strength": 0.4,
  "cfg_scale": 7,
  "steps": 20,
  "sampler": "DPM++ 2M Karras"
}
```
Use Casey's reference.png as input. Prompt changes focus on expression only.

### Pose Variation
```json
{
  "denoising_strength": 0.5,
  "cfg_scale": 7,
  "steps": 25,
  "sampler": "DPM++ 2M Karras"
}
```
Use closest matching pose from turnaround. Prompt describes new pose.

### New Scene/Angle
```json
{
  "denoising_strength": 0.6,
  "cfg_scale": 8,
  "steps": 30,
  "sampler": "DPM++ 2M Karras"
}
```
Higher CFG helps maintain character details. May need multiple attempts.

## Best Practices

1. **Always use the closest reference**: If generating Casey from a 3/4 angle, use the 3/4 view from turnaround.png as your input.

2. **Keep identity tags consistent**: Always include the full identity description in your prompt, even for img2img.

3. **Batch and select**: Generate 4 images, pick the best one that maintains Casey's look.

4. **Bank good seeds**: When you get a perfect Casey, save that seed. Reuse it with the same reference image for consistent results.

5. **Iterative refinement**: If identity drifts, take your best result and run it through img2img again at lower denoising (0.3-0.4) to refine.

## Input Image Recommendations

| Source Image | Resolution | When to Use |
|--------------|------------|-------------|
| `casey/reference.png` | Native | 3/4 view shots, default |
| `casey/turnaround.png` (cropped) | Crop to 896x1152 | Specific angle needed |
| Previous generation | 896x1152 | Iterative refinement |

## Troubleshooting

**Problem: Face looks different**
- Lower denoising to 0.4
- Increase CFG to 8
- Add "same face, consistent character" to prompt

**Problem: Outfit changes**
- Explicitly describe outfit in prompt
- Use lower denoising (0.45)
- Add outfit details to negative prompt if wrong items appear

**Problem: Style drifts to photorealistic**
- Emphasize "3D animated, Pixar style, stylized" in prompt
- Add "photorealistic, photograph, real human" to negative prompt
