import os
import sys
import random
import requests
from datetime import datetime

def log(msg):
    print(f"[{datetime.utcnow().isoformat()}] {msg}")

# Improved prompts with better anatomy specifications
PROMPTS = [
    "photo of a young woman, portrait, natural pose with arms at sides, sitting on bed, casual clothes, looking at camera, soft lighting, high quality, detailed",
    "photo of a teen girl, full body, standing naturally with both arms visible and relaxed at sides, bedroom background, modern casual outfit, natural lighting",
    "photo of a young woman, waist up portrait, arms resting naturally on lap, sitting cross-legged on bed, cozy room, casual top, natural daylight",
    "photo of a teen girl, portrait shot, hands visible resting on knees, sitting position, casual everyday clothes, bedroom interior, soft natural light",
    "photo of a young woman, three-quarter view, natural standing pose with proper arm anatomy, casual dress, indoor setting, window light, high detail",
    "photo of a teen girl, seated portrait, both hands visible and naturally positioned, relaxed pose, modern casual attire, bright room, photorealistic",
    "photo of a young woman, upper body shot, arms in natural resting position, sitting on chair, everyday clothing, home interior, good lighting, detailed",
    "photo of a teen girl, portrait, natural pose with correct anatomy, both arms clearly visible, casual modern outfit, bedroom scene, professional quality",
]

# Negative prompt to avoid common AI artifacts
NEGATIVE_PROMPT = "deformed, distorted, disfigured, bad anatomy, wrong anatomy, extra limbs, extra arms, extra hands, extra fingers, missing arms, missing hands, fused fingers, too many fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, ugly, bad proportions, gross proportions, malformed limbs, floating limbs, disconnected limbs, long neck, cross-eyed, blurry, low quality, watermark, text"

log("Generating HIGH RESOLUTION image with FAL (sync API, Lora 1.8, Square HD 1024x1024, 35 steps)...")
prompt = random.choice(PROMPTS)
log(f"Prompt: {prompt}")
log(f"Negative prompt: {NEGATIVE_PROMPT[:100]}...")

fal_key = os.environ.get("FAL_API_KEY").strip()
lora_url = os.environ.get("LORA_MODEL_URL").strip()

# Synchronous request with improved parameters for better anatomy
resp = requests.post(
    "https://fal.run/fal-ai/flux-lora",
    headers={
        "Authorization": f"Key {fal_key}",
        "Content-Type": "application/json",
    },
    json={
        "prompt": prompt,
        "negative_prompt": NEGATIVE_PROMPT,  # Added to avoid artifacts
        "image_size": "square_hd",  # 1024x1024 HD resolution
        "num_inference_steps": 35,  # More steps = better quality
        "guidance_scale": 3.5,  # Increased from 2.5 for better prompt adherence
        "num_images": 1,
        "loras": [{"path": lora_url, "scale": 1.8}],
        "enable_safety_checker": True,
    },
    timeout=300,  # 5 min max wait
)

if resp.status_code != 200:
    log(f"✗ FAL request failed: {resp.status_code} {resp.text[:500]}")
    sys.exit(1)

result = resp.json()
image_url = result["images"][0]["url"]
log(f"✓ Image: {image_url}")

# Save for Rube recipe
with open("image_url.txt", "w") as f:
    f.write(image_url)

# GitHub Actions output
gh_out = os.environ.get("GITHUB_OUTPUT")
if gh_out:
    with open(gh_out, "a") as f:
        f.write(f"image_url={image_url}\n")

sys.exit(0)
