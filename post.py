#!/usr/bin/env python3
import os, sys, json, time, random
from datetime import datetime
import requests

FAL_API_KEY = os.environ.get("FAL_API_KEY", "").strip()
LORA_MODEL_URL = os.environ.get("LORA_MODEL_URL", "").strip()
COMPOSIO_TOKEN = os.environ.get("COMPOSIO_TOKEN", "").strip()
RECIPE_ID = "rcp_A9M-wR3IZxUp"

PROMPTS = [
    "young woman selfie bedroom, casual outfit, soft natural light",
    "young woman mirror selfie, casual modern clothes",
    "young woman taking photo on bed, cozy room",
]

def log(msg):
    print(f"[{datetime.utcnow().isoformat()}] {msg}", flush=True)

def generate_image_fal(prompt):
    log("Generating image with FAL...")
    headers = {"Authorization": f"Key {FAL_API_KEY}", "Content-Type": "application/json"}
    
    payload = {
        "prompt": prompt,
        "image_size": "square",
        "num_inference_steps": 35,
        "guidance_scale": 2.5,
        "num_images": 1,
        "loras": [{"path": LORA_MODEL_URL, "scale": 1.8}]
    }
    
    # Submit to queue
    resp = requests.post("https://queue.fal.run/fal-ai/flux-lora", headers=headers, json=payload, timeout=30)
    if resp.status_code != 200:
        log(f"Submit error: {resp.status_code} - {resp.text}")
        raise Exception(f"Submit failed: {resp.status_code}")
    
    data = resp.json()
    request_id = data.get("request_id")
    log(f"Request ID: {request_id}")
    
    # Poll for result using queue endpoint
    for i in range(60):
        time.sleep(3)
        try:
            # Use queue.fal.run for status check
            status_resp = requests.get(
                f"https://queue.fal.run/fal-ai/flux-lora/requests/{request_id}/status",
                headers=headers,
                timeout=15
            )
            
            if status_resp.status_code == 200:
                result = status_resp.json()
                state = result.get("status")
                log(f"Status: {state}")
                
                if state == "COMPLETED":
                    response_url = result.get("response_url")
                    if response_url:
                        final_resp = requests.get(response_url, headers=headers, timeout=15)
                        final_data = final_resp.json()
                        images = final_data.get("images", [])
                        if images:
                            return images[0].get("url")
                    raise Exception("No images in completed result")
                elif state in ["FAILED", "CANCELLED"]:
                    error = result.get("error", "Unknown")
                    raise Exception(f"Generation failed: {error}")
            else:
                log(f"Poll returned: {status_resp.status_code}")
        except Exception as e:
            log(f"Poll error: {e}")
    
    raise Exception("Timeout waiting for image")

def call_recipe(image_url):
    log("Calling recipe...")
    resp = requests.post(
        f"https://backend.composio.dev/api/v1/rube/recipes/{RECIPE_ID}/trigger",
        headers={"Authorization": f"Bearer {COMPOSIO_TOKEN}", "Content-Type": "application/json"},
        json={"input": {"image_url": image_url}},
        timeout=60
    )
    log(f"Recipe response: {resp.status_code}")
    if resp.status_code not in [200, 201]:
        log(f"Recipe error: {resp.text}")
        raise Exception(f"Recipe failed: {resp.status_code}")
    return resp.json()

log("Starting...")
prompt = random.choice(PROMPTS)
log(f"Prompt: {prompt}")
image_url = generate_image_fal(prompt)
log(f"✓ Image: {image_url}")
call_recipe(image_url)
log("✓ SUCCESS!")
