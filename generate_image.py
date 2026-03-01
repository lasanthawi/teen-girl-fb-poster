import os
import sys
import random
import requests
from datetime import datetime

def log(msg):
    print(f"[{datetime.utcnow().isoformat()}] {msg}")

PROMPTS = [
    "young woman full body mirror selfie, casual outfit, bedroom",
    "teen girl sitting on bed with phone, relaxed pose",
    "young woman standing by window, natural light, full body",
    "girl mirror selfie, casual modern clothes",
    "young woman sitting on floor with books, study vibe",
    "teen girl lying on bed taking selfie",
    "young woman at desk with laptop, studying",
    "girl standing full body outfit photo, mirror",
]

log("Generating image with FAL (sync API, Lora 1.8, Square, 35 steps)...")
prompt = random.choice(PROMPTS)
log(f"Prompt: {prompt}")

fal_key = os.environ.get("FAL_API_KEY").strip()
lora_url = os.environ.get("LORA_MODEL_URL").strip()

# Synchronous request: one call, result returned when ready (typically 1–2 min)
# No polling or webhook needed; connection stays open until FAL returns the image.
resp = requests.post(
    "https://fal.run/fal-ai/flux-lora",
    headers={
        "Authorization": f"Key {fal_key}",
        "Content-Type": "application/json",
    },
    json={
        "prompt": prompt,
        "image_size": "square",
        "num_inference_steps": 35,
        "guidance_scale": 2.5,
        "num_images": 1,
        "loras": [{"path": lora_url, "scale": 1.8}],
    },
    timeout=300,  # 5 min max wait (FAL usually 1–2 min)
)

if resp.status_code != 200:
    log(f"✗ FAL request failed: {resp.status_code} {resp.text[:500]}")
    sys.exit(1)

result = resp.json()
image_url = result["images"][0]["url"]
log(f"✓ Image: {image_url}")

# Save for next step (publish.py)
with open("image_url.txt", "w") as f:
    f.write(image_url)

# GitHub Actions output
gh_out = os.environ.get("GITHUB_OUTPUT")
if gh_out:
    with open(gh_out, "a") as f:
        f.write(f"image_url={image_url}\n")

sys.exit(0)
