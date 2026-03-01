#!/usr/bin/env python3
import os
import sys
import json
import random
import requests
import fal_client
from datetime import datetime

def log(msg):
    print(f"[{datetime.utcnow().isoformat()}] {msg}")

def main():
    log("="*60)
    log("Automated Teen Girl FB Poster")
    log("="*60)
    log("")
    
    # Get all credentials
    fal_key = os.environ.get("FAL_API_KEY", "").strip()
    lora_url = os.environ.get("LORA_MODEL_URL", "").strip()
    composio_token = os.environ.get("COMPOSIO_TOKEN", "").strip()
    
    if not all([fal_key, lora_url, composio_token]):
        log("✗ Missing required secrets")
        sys.exit(1)
    
    log(f"✓ All secrets present")
    log("")
    
    # Teen girl prompts for Lora
    prompts = [
        "young woman selfie in bedroom, casual outfit, soft natural light, photorealistic",
        "teen girl studying at desk, books and laptop, focused expression, natural lighting",
        "girl sitting on bed with phone, relaxed pose, modern bedroom, soft lighting",
        "young woman mirror selfie, casual clothes, bedroom background, natural light",
        "teen girl laying on bed, comfortable outfit, reading book, cozy atmosphere",
        "girl at desk with laptop, evening light through window, concentrated expression",
        "young woman taking photo in room, casual style, warm lighting, photorealistic",
        "teen girl relaxing on floor with pillow, casual outfit, soft bedroom lighting"
    ]
    
    prompt = random.choice(prompts)
    log(f"Prompt: {prompt}")
    log("")
    
    # STEP 1: Generate image with FAL
    log("="*60)
    log("STEP 1: Generate Image (Lora 1.8, Square, 35 steps)")
    log("="*60)
    
    try:
        os.environ["FAL_KEY"] = fal_key
        
        result = fal_client.subscribe(
            "fal-ai/flux-lora",
            arguments={
                "prompt": prompt,
                "loras": [{"path": lora_url, "scale": 1.8}],
                "image_size": "square",
                "num_inference_steps": 35,
                "guidance_scale": 2.5,
                "num_images": 1,
                "enable_safety_checker": False
            }
        )
        
        image_url = result["images"][0]["url"]
        log(f"✓ Image generated: {image_url}")
        log(f"  Size: 512x512 square")
        log("")
        
    except Exception as e:
        log(f"✗ Image generation failed: {e}")
        sys.exit(1)
    
    # STEP 2: Call Composio recipe
    log("="*60)
    log("STEP 2: Publish via Composio Recipe")
    log("="*60)
    
    headers = {
        "Authorization": f"Bearer {composio_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "facebook_page_id": "1025914070602506",
        "image_url": image_url
    }
    
    try:
        response = requests.post(
            "https://backend.composio.dev/api/v1/actions/rcp_A9M-wR3IZxUp/execute",
            headers=headers,
            json=payload,
            timeout=180
        )
        
        if response.status_code == 200:
            result = response.json()
            log(f"✓ Recipe executed!")
            
            if "data" in result:
                data = result.get("data", {})
                log(f"  Post ID: {data.get('post_id', 'N/A')}")
                log(f"  Link: {data.get('permalink', 'N/A')}")
                log(f"  Caption: {data.get('caption', 'N/A')[:60]}...")
        else:
            log(f"✗ Recipe API returned {response.status_code}")
            log(f"  Response: {response.text[:200]}")
            raise Exception(f"Recipe failed: {response.status_code}")
        
        log("")
        log("="*60)
        log("✓ SUCCESS! Post published to Nethmi G")
        log("="*60)
        
    except Exception as e:
        log(f"✗ Recipe execution failed: {e}")
        log("")
        log("Image was generated successfully!")
        log(f"You can manually post it using: {image_url}")
        sys.exit(1)

if __name__ == "__main__":
    main()
