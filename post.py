#!/usr/bin/env python3
import os, sys, json, time, random, requests
from datetime import datetime

FAL_API_KEY = os.environ.get("FAL_API_KEY", "").strip()
LORA_MODEL_URL = os.environ.get("LORA_MODEL_URL", "").strip()
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "").strip()
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "").strip()

PROMPTS = [
    "young woman selfie bedroom, casual outfit, soft natural light",
    "young woman mirror selfie, casual modern clothes",
    "young woman taking photo on bed, cozy room",
]

def log(msg):
    print(f"[{datetime.utcnow().isoformat()}] {msg}", flush=True)

def generate_image_fal(prompt):
    log("Generating image with FAL (Lora 1.8, Square, 35 steps)...")
    headers = {"Authorization": f"Key {FAL_API_KEY}", "Content-Type": "application/json"}
    
    # Submit to queue
    resp = requests.post(
        "https://queue.fal.run/fal-ai/flux-lora",
        headers=headers,
        json={
            "prompt": prompt,
            "image_size": "square",
            "num_inference_steps": 35,
            "guidance_scale": 2.5,
            "num_images": 1,
            "loras": [{"path": LORA_MODEL_URL, "scale": 1.8}]
        },
        timeout=30
    )
    if resp.status_code != 200:
        raise Exception(f"Submit failed: {resp.status_code} - {resp.text}")
    
    request_id = resp.json().get("request_id")
    log(f"Request ID: {request_id}")
    
    # Poll for completion
    for i in range(60):
        time.sleep(3)
        status_resp = requests.get(
            f"https://queue.fal.run/fal-ai/flux-lora/requests/{request_id}/status",
            headers=headers,
            timeout=15
        )
        
        if status_resp.status_code == 200:
            result = status_resp.json()
            if result.get("status") == "COMPLETED":
                response_url = result.get("response_url")
                if response_url:
                    final = requests.get(response_url, headers=headers).json()
                    return final["images"][0]["url"]
        elif status_resp.status_code == 202:
            continue
    
    raise Exception("Timeout")

def trigger_webhook(image_url):
    log("Triggering webhook to publish...")
    resp = requests.post(
        WEBHOOK_URL,
        json={"image_url": image_url, "secret": WEBHOOK_SECRET},
        timeout=120
    )
    log(f"Webhook response: {resp.status_code}")
    if resp.status_code in [200, 201]:
        data = resp.json()
        log(f"✓ Published! {json.dumps(data, indent=2)}")
        return data
    else:
        log(f"Webhook error: {resp.text}")
        raise Exception(f"Webhook failed: {resp.status_code}")

log("="*60)
log("Teen Girl FB Poster - Automated")
log("="*60)
prompt = random.choice(PROMPTS)
log(f"Prompt: {prompt}\n")
image_url = generate_image_fal(prompt)
log(f"✓ Image: {image_url}\n")
trigger_webhook(image_url)
log("\n✓ SUCCESS! Post published to Nethmi G")
