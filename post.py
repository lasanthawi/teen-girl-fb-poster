import os
import time
import random
import requests
from datetime import datetime
from composio import Composio

def log(msg):
    print(f"[{datetime.utcnow().isoformat()}] {msg}")

# Diverse prompts
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

def generate_image():
    log("Generating image with FAL (Lora 1.8)...")
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
    
    # Poll
    for _ in range(60):
        time.sleep(3)
        status = requests.get(
            f"https://queue.fal.run/fal-ai/flux-lora/requests/{request_id}",
            headers={"Authorization": f"Key {fal_key}"}
        )
        if status.status_code == 200:
            result = status.json()
            if result.get("status") == "COMPLETED":
                return result["images"][0]["url"]
    raise Exception("Timeout")

def publish(image_url):
    log(f"\nPublishing: {image_url}")
    
    # Use Composio SDK
    client = Composio(api_key=os.environ.get("COMPOSIO_TOKEN").strip())
    
    result = client.rube.execute_recipe(
        recipe_id="rcp_A9M-wR3IZxUp",
        params={
            "facebook_page_id": "1025914070602506",
            "image_url": image_url
        }
    )
    
    log(f"\n✓ SUCCESS! Posted to Facebook")
    return result

log("Teen Girl FB Auto-Poster")
image_url = generate_image()
log(f"✓ Image: {image_url}")
publish(image_url)
log("\n✅ COMPLETE!")
