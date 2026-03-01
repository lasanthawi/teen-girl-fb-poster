#!/usr/bin/env python3
"""
Generate image with FAL AI and trigger Composio recipe to publish
"""

import os
import sys
import json
import requests
from datetime import datetime

# Configuration
FAL_API_KEY = os.getenv("FAL_API_KEY", "").strip()
LORA_MODEL_URL = os.getenv("LORA_MODEL_URL")
COMPOSIO_API_KEY = os.getenv("COMPOSIO_API_KEY", "").strip()
RECIPE_ID = "rcp_A9M-wR3IZxUp"
FACEBOOK_PAGE_ID = "1025914070602506"

def log(msg):
    print(f"[{datetime.utcnow().isoformat()}] {msg}")

def generate_image_prompt():
    """Generate a simple teen girl daily log image prompt"""
    prompts = [
        "A teenage girl taking a mirror selfie in her bedroom, warm afternoon lighting, casual outfit, cozy room with posters, photographic style",
        "A teen girl sitting at her desk studying with laptop and books, focused expression, natural window light, modern bedroom, lifestyle photography",
        "A teenage girl relaxing on her bed with phone, comfortable clothes, fairy lights in background, golden hour lighting, candid photography",
        "A teen girl having a video call on laptop, smiling and waving, cozy bedroom setup, soft lighting, authentic moment photography",
        "A teenage girl journaling at her desk, thoughtful expression, aesthetic workspace, natural lighting, lifestyle photography style"
    ]
    import random
    return random.choice(prompts)

def generate_image_fal(prompt, lora_url):
    """Generate image using FAL AI with Lora model"""
    log(f"Generating image: {prompt[:60]}...")
    
    headers = {
        "Authorization": f"Key {FAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": prompt,
        "loras": [{"path": lora_url, "scale": 1.0}],
        "image_size": "landscape_4_3",
        "num_images": 1,
        "enable_safety_checker": False
    }
    
    try:
        response = requests.post(
            "https://fal.run/fal-ai/flux-2/lora",
            headers=headers,
            json=payload,
            timeout=120
        )
        response.raise_for_status()
        result = response.json()
        
        images = result.get("images", [])
        if images:
            image_url = images[0].get("url")
            log(f"✓ Image generated: {image_url}")
            return image_url
        else:
            raise Exception(f"No images in response: {result}")
    except Exception as e:
        log(f"✗ Error generating image: {e}")
        raise

def trigger_composio_recipe(image_url):
    """Trigger Composio recipe to publish post"""
    log("Triggering Composio recipe to publish...")
    
    headers = {
        "X-API-Key": COMPOSIO_API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "recipeId": RECIPE_ID,
        "params": {
            "facebook_page_id": FACEBOOK_PAGE_ID,
            "image_url": image_url
        }
    }
    
    try:
        response = requests.post(
            "https://backend.composio.dev/api/v1/rube/recipe/run",
            headers=headers,
            json=payload,
            timeout=180
        )
        response.raise_for_status()
        result = response.json()
        log(f"✓ Recipe executed: {json.dumps(result, indent=2)}")
        return result
    except Exception as e:
        log(f"✗ Error triggering recipe: {e}")
        if hasattr(e, 'response') and e.response:
            log(f"Response: {e.response.text}")
        raise

def main():
    log("=== Teen Girl FB Auto-Poster (Hybrid Mode) ===")
    
    # Validate required vars
    if not FAL_API_KEY:
        log("ERROR: FAL_API_KEY is required")
        sys.exit(1)
    if not LORA_MODEL_URL:
        log("ERROR: LORA_MODEL_URL is required")
        sys.exit(1)
    if not COMPOSIO_API_KEY:
        log("ERROR: COMPOSIO_API_KEY is required")
        sys.exit(1)
    
    try:
        # Step 1: Generate image with FAL
        prompt = generate_image_prompt()
        image_url = generate_image_fal(prompt, LORA_MODEL_URL)
        
        # Step 2: Trigger Composio recipe
        result = trigger_composio_recipe(image_url)
        
        log("\n=== SUCCESS! Post published ===")
        print(json.dumps({
            "success": True,
            "image_url": image_url,
            "recipe_result": result
        }, indent=2))
        
    except Exception as e:
        log(f"\n=== FAILED ===")
        log(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
