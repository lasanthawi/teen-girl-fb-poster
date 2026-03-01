#!/usr/bin/env python3
"""
Automated Teen Girl FB Poster
Generates image with FAL + calls Composio recipe
"""
import os
import sys
import requests
from datetime import datetime
import random

def log(msg):
    print(f"[{datetime.utcnow().isoformat()}] {msg}", flush=True)

def main():
    log("=" * 60)
    log("Automated Teen Girl FB Poster")
    log("=" * 60)
    log("")

    fal_key = os.environ.get("FAL_API_KEY", "").strip()
    lora_url = os.environ.get("LORA_MODEL_URL", "").strip()
    composio_token = os.environ.get("COMPOSIO_TOKEN", "").strip()

    if not all([fal_key, lora_url, composio_token]):
        log("✗ Missing required secrets")
        sys.exit(1)

    log("✓ All secrets present")
    log("")

    prompts = [
        "young woman selfie in bedroom, casual outfit, soft natural light, photorealistic",
        "teenage girl sitting on bed with books, studying, natural window light",
        "young woman mirror selfie, casual modern clothes, bedroom setting",
        "teen girl taking photo with phone, relaxed pose, cozy room",
        "young woman portrait, sitting at desk, laptop visible, warm lighting",
        "teenage girl selfie lying on bed, casual style, afternoon light",
        "young woman in bedroom, reading book, natural lighting, candid shot",
        "teen girl with coffee cup, sitting cross-legged, cozy bedroom"
    ]
    prompt = random.choice(prompts)
    log(f"Prompt: {prompt}")
    log("")

    log("=" * 60)
    log("STEP 1: Generate Image (Lora 1.8, Square, 35 steps)")
    log("=" * 60)

    try:
        response = requests.post(
            "https://queue.fal.run/fal-ai/flux-lora",
            headers={
                "Authorization": f"Key {fal_key}",
                "Content-Type": "application/json"
            },
            json={
                "prompt": prompt,
                "image_size": "square",
                "num_inference_steps": 35,
                "guidance_scale": 2.5,
                "num_images": 1,
                "enable_safety_checker": False,
                "loras": [{"path": lora_url, "scale": 1.8}]
            },
            timeout=120
        )
        response.raise_for_status()
        result = response.json()

        request_id = result.get("request_id")
        if not request_id:
            log(f"✗ No request_id in response: {result}")
            sys.exit(1)

        log(f"✓ Request submitted: {request_id}")
        log("Waiting for image generation...")

        import time
        for i in range(60):
            status_response = requests.get(
                f"https://queue.fal.run/fal-ai/flux-lora/requests/{request_id}",
                headers={"Authorization": f"Key {fal_key}"},
                timeout=30
            )
            status_response.raise_for_status()
            status_data = status_response.json()

            if status_data.get("status") == "COMPLETED":
                images = status_data.get("images", [])
                if images:
                    image_url = images[0].get("url")
                    log(f"✓ Image generated!")
                    log(f"  URL: {image_url}")
                    log(f"  Size: 512x512 square")
                    log(f"  Lora scale: 1.8")
                    break
            elif status_data.get("status") in ["FAILED", "ERROR"]:
                log(f"✗ Generation failed: {status_data}")
                sys.exit(1)

            time.sleep(2)
        else:
            log("✗ Timeout waiting for image")
            sys.exit(1)

    except Exception as e:
        log(f"✗ Image generation failed: {e}")
        sys.exit(1)

    log("")
    log("=" * 60)
    log("STEP 2: Call Composio Recipe")
    log("=" * 60)

    try:
        recipe_response = requests.post(
            "https://backend.composio.dev/api/v2/rube/recipe/execute",
            headers={
                "Authorization": f"Bearer {composio_token}",
                "Content-Type": "application/json"
            },
            json={
                "recipeId": "rcp_A9M-wR3IZxUp",
                "params": {
                    "page_id": "1025914070602506",
                    "image_url": image_url
                }
            },
            timeout=60
        )

        log(f"Recipe response status: {recipe_response.status_code}")

        if recipe_response.status_code in [200, 201]:
            log("✓ Recipe executed successfully!")
            log("")
            log("=" * 60)
            log("✓ SUCCESS! Post published to Nethmi G Facebook page")
            log("=" * 60)
        else:
            log(f"⚠ Recipe response: {recipe_response.text}")
            log("")
            log("IMAGE STILL GENERATED SUCCESSFULLY:")
            log(f"Image URL: {image_url}")

    except Exception as e:
        log(f"⚠ Recipe call failed: {e}")
        log("")
        log("IMAGE STILL GENERATED SUCCESSFULLY:")
        log(f"Image URL: {image_url}")

if __name__ == "__main__":
    main()
