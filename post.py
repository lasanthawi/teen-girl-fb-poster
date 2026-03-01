import os
import time
import random
import requests
from datetime import datetime

def log(msg):
    print(f"[{datetime.utcnow().isoformat()}] {msg}")

# Diverse prompts for variety
PROMPTS = [
    "young woman full body mirror selfie, casual outfit, bedroom",
    "teen girl sitting on bed with phone, relaxed pose, cozy room",
    "young woman standing by window, natural light, full body shot",
    "girl taking mirror selfie, casual modern clothes, bedroom background",
    "young woman sitting on floor with books, study vibe, warm lighting",
    "teen girl lying on bed taking selfie, casual outfit, soft lighting",
    "young woman at desk with laptop, studying, cozy bedroom",
    "girl standing full body outfit photo, mirror selfie, modern room",
    "young woman selfie bedroom, casual outfit, soft natural light",
    "teen girl sitting cross-legged on bed, phone in hand, relaxed",
    "young woman full length mirror photo, showing outfit, bedroom",
    "girl taking photo on bed, cozy aesthetic, warm lighting",
    "young woman standing pose, casual clothes, natural bedroom lighting",
    "teen girl sitting at vanity mirror, getting ready, soft light",
    "young woman lying down taking selfie, comfortable casual outfit",
    "girl full body photo in room, natural pose, modern bedroom"
]

def generate_image():
    log("="*60)
    log("STEP 1: Generate Image with FAL")
    log("="*60)
    
    prompt = random.choice(PROMPTS)
    log(f"Prompt: {prompt}")
    log(f"Lora: 1.8 (MAXIMUM strength)")
    log(f"Size: Square 512x512")
    log(f"Steps: 35")
    log("")
    
    fal_key = os.environ.get("FAL_API_KEY").strip()
    lora_url = os.environ.get("LORA_MODEL_URL").strip()
    
    payload = {
        "prompt": prompt,
        "image_size": "square",
        "num_inference_steps": 35,
        "guidance_scale": 2.5,
        "num_images": 1,
        "loras": [{"path": lora_url, "scale": 1.8}],
        "enable_safety_checker": False
    }
    
    # Submit request
    resp = requests.post(
        "https://queue.fal.run/fal-ai/flux-lora",
        headers={"Authorization": f"Key {fal_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=30
    )
    resp.raise_for_status()
    data = resp.json()
    request_id = data["request_id"]
    log(f"✓ Request ID: {request_id}")
    
    # Poll for result
    status_url = f"https://queue.fal.run/fal-ai/flux-lora/requests/{request_id}"
    for _ in range(60):
        time.sleep(3)
        status_resp = requests.get(status_url, headers={"Authorization": f"Key {fal_key}"}, timeout=10)
        if status_resp.status_code == 200:
            result = status_resp.json()
            if result.get("status") == "COMPLETED":
                image_url = result["images"][0]["url"]
                log(f"✓ Image generated: {image_url}")
                return image_url
    
    raise Exception("Timeout waiting for image")

def publish_to_facebook(image_url):
    log("")
    log("="*60)
    log("STEP 2: Publish to Facebook via Composio")
    log("="*60)
    log("")
    log(f"Image: {image_url}")
    log("Calling recipe to generate caption and post...")
    
    token = os.environ.get("COMPOSIO_TOKEN").strip()
    
    payload = {
        "recipeId": "rcp_A9M-wR3IZxUp",
        "params": {
            "page_id": "1025914070602506",
            "image_url": image_url
        }
    }
    
    resp = requests.post(
        "https://backend.composio.dev/api/v2/rube/recipe/execute",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=120
    )
    
    log(f"Recipe response: {resp.status_code}")
    
    if resp.status_code == 200:
        log("✓ SUCCESS! Post published to Facebook")
        log("")
        log("="*60)
        log("✅ COMPLETE!")
        log("="*60)
        return
    else:
        log(f"✗ Recipe failed: {resp.status_code}")
        log(f"Response: {resp.text}")
        raise Exception(f"Recipe execution failed: {resp.status_code}")

if __name__ == "__main__":
    log("="*60)
    log("Teen Girl FB Auto-Poster (Direct Mode)")
    log("="*60)
    log("")
    
    # Generate image
    image_url = generate_image()
    
    # Publish directly to Facebook
    publish_to_facebook(image_url)
