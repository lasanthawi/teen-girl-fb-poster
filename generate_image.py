import os
import sys
import time
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

log("Generating image with FAL (Lora 1.8, Square, 35 steps)...")
prompt = random.choice(PROMPTS)
log(f"Prompt: {prompt}")

fal_key = os.environ.get("FAL_API_KEY").strip()
lora_url = os.environ.get("LORA_MODEL_URL").strip()

# Submit
resp = requests.post(
    "https://queue.fal.run/fal-ai/flux-lora",
    headers={"Authorization": f"Key {fal_key}", "Content-Type": "application/json"},
    json={
        "prompt": prompt,
        "image_size": "square",
        "num_inference_steps": 35,
        "guidance_scale": 2.5,
        "num_images": 1,
        "loras": [{"path": lora_url, "scale": 1.8}]
    }
)
request_id = resp.json()["request_id"]
log(f"Request ID: {request_id}")

# Poll (allow up to ~10 min: 120 * 5s) — FAL queue can take 4–6+ min under load
for _ in range(120):
    time.sleep(5)
    status = requests.get(
        f"https://queue.fal.run/fal-ai/flux-lora/requests/{request_id}",
        headers={"Authorization": f"Key {fal_key}"}
    )
    if status.status_code == 200:
        result = status.json()
        if result.get("status") == "COMPLETED":
            image_url = result["images"][0]["url"]
            log(f"✓ Image: {image_url}")
            
            # Save to file for next step (publish.py)
            with open("image_url.txt", "w") as f:
                f.write(image_url)
            
            # Output for GitHub Actions (GITHUB_OUTPUT)
            gh_out = os.environ.get("GITHUB_OUTPUT")
            if gh_out:
                with open(gh_out, "a") as f:
                    f.write(f"image_url={image_url}\n")
            sys.exit(0)

log("✗ Timeout")
sys.exit(1)
