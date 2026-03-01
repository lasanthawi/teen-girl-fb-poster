#!/usr/bin/env python3
"""
Generate image with FAL AI and trigger Composio recipe to publish
"""

import os
import sys
import json
import requests
import time
from datetime import datetime

# Configuration
FAL_API_KEY = os.getenv("FAL_API_KEY", "").strip()
LORA_MODEL_URL = os.getenv("LORA_MODEL_URL")
COMPOSIO_TOKEN = os.getenv("COMPOSIO_TOKEN", "").strip()
RECIPE_ID = "rcp_A9M-wR3IZxUp"
FACEBOOK_PAGE_ID = "1025914070602506"

def log(msg):
    print(f"[{datetime.utcnow().isoformat()}] {msg}")

def generate_image_prompt():
    """Generate prompts with strong Lora activation"""
    # Add trigger word or consistent description for Lora
    base_prompts = [
        "young woman mirror selfie in bedroom",
        "young woman studying with laptop in cozy room",
        "young woman relaxing with phone in bedroom",
        "young woman journaling at desk in aesthetic room",
        "young woman video call on laptop smiling",
        "young woman taking selfie lying on bed",
        "young woman by window in bedroom natural light",
        "young woman with books and laptop on floor"
    ]
    import random
    base = random.choice(base_prompts)
    return f"{base}, casual modern clothes, natural lighting, photorealistic, high quality"

def generate_image_fal(prompt, lora_url):
    """Generate square image with MAXIMUM Lora influence"""
    log(f"Generating image with STRONG Lora...")
    log(f"Prompt: {prompt}")
    log(f"Lora URL: {lora_url[:70]}...")
    
    headers = {
        "Authorization": f"Key {FAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Maximum Lora influence settings
    payload = {
        "prompt": prompt,
        "loras": [
            {
                "path": lora_url,
                "scale": 1.8  # VERY STRONG - increased from 1.2 to 1.8
            }
        ],
        "image_size": "square",
        "num_images": 1,
        "num_inference_steps": 35,  # More steps for better Lora blend
        "guidance_scale": 2.5,  # Lower for more Lora influence
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
            width = images[0].get("width", "unknown")
            height = images[0].get("height", "unknown")
            log(f"✓ Image generated!")
            log(f"  URL: {image_url}")
            log(f"  Size: {width}x{height}")
            log(f"  Lora scale: 1.8 (VERY STRONG)")
            return image_url
        else:
            raise Exception(f"No images in response: {result}")
    except Exception as e:
        log(f"✗ Error: {e}")
        raise

def trigger_composio_recipe(image_url):
    """Trigger recipe - try multiple endpoint formats"""
    log("\nPublishing to Facebook...")
    log(f"Recipe: {RECIPE_ID}")
    log(f"Image: {image_url[:60]}...")
    
    headers = {
        "Authorization": f"Bearer {COMPOSIO_TOKEN}",
        "Content-Type": "application/json",
        "x-api-key": COMPOSIO_TOKEN  # Try both auth methods
    }
    
    # Try multiple payload formats
    payloads_to_try = [
        # Format 1: Direct params
        {
            "facebook_page_id": FACEBOOK_PAGE_ID,
            "image_url": image_url
        },
        # Format 2: Wrapped in input_data
        {
            "input_data": {
                "facebook_page_id": FACEBOOK_PAGE_ID,
                "image_url": image_url
            }
        }
    ]
    
    # Try multiple endpoints
    endpoints = [
        f"https://backend.composio.dev/api/v1/rube/recipes/{RECIPE_ID}/execute",
        f"https://backend.composio.dev/api/v1/recipes/{RECIPE_ID}/execute",
        f"https://backend.composio.dev/api/v1/rube/recipe/{RECIPE_ID}/run"
    ]
    
    for endpoint in endpoints:
        for payload in payloads_to_try:
            try:
                log(f"Trying: {endpoint}")
                response = requests.post(
                    endpoint,
                    headers=headers,
                    json=payload,
                    timeout=180
                )
                
                if response.status_code == 200:
                    result = response.json()
                    log(f"✓ Success!")
                    
                    if "data" in result:
                        recipe_data = result.get("data", {})
                        log(f"  Post ID: {recipe_data.get('post_id', 'N/A')}")
                        log(f"  Link: {recipe_data.get('permalink', 'N/A')}")
                        caption = recipe_data.get('caption', '')
                        if caption:
                            log(f"  Caption: {caption[:60]}...")
                    return result
                else:
                    log(f"  Status {response.status_code}: {response.text[:100]}")
                    
            except Exception as e:
                continue
    
    raise Exception("All API endpoints failed. Recipe may need manual execution.")

def main():
    log("="*60)
    log("Teen Girl FB Poster - STRONG Lora Mode")
    log("="*60)
    
    if not all([FAL_API_KEY, LORA_MODEL_URL, COMPOSIO_TOKEN]):
        log("ERROR: Missing environment variables")
        sys.exit(1)
    
    log(f"\n✓ Config loaded")
    log(f"  Lora scale: 1.8 (MAXIMUM)")
    log(f"  Image size: square (512x512)")
    log(f"  Inference steps: 35")
    
    try:
        # Generate image
        log("\n" + "="*60)
        log("STEP 1: Generate Image with STRONG Lora")
        log("="*60)
        prompt = generate_image_prompt()
        image_url = generate_image_fal(prompt, LORA_MODEL_URL)
        
        # Publish
        log("\n" + "="*60)
        log("STEP 2: Publish to Facebook")
        log("="*60)
        result = trigger_composio_recipe(image_url)
        
        log("\n" + "="*60)
        log("✓ COMPLETE!")
        log("="*60)
        
        print("\n" + json.dumps({
            "success": True,
            "image_url": image_url,
            "lora_scale": 1.8,
            "result": result
        }, indent=2))
        
    except Exception as e:
        log("\n" + "="*60)
        log("✗ FAILED")
        log("="*60)
        log(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
