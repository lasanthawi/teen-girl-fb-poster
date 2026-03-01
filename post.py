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
COMPOSIO_TOKEN = os.getenv("COMPOSIO_TOKEN", "").strip()
RECIPE_ID = "rcp_A9M-wR3IZxUp"
FACEBOOK_PAGE_ID = "1025914070602506"

def log(msg):
    print(f"[{datetime.utcnow().isoformat()}] {msg}")

def generate_image_prompt():
    """Generate teen girl daily log prompts optimized for Lora training"""
    prompts = [
        "Portrait of a teenage girl taking a mirror selfie, smartphone in hand, bedroom background, natural lighting, casual modern clothes, genuine smile, photorealistic",
        "Teen girl sitting cross-legged on bed with laptop, studying, cozy bedroom, afternoon sunlight through window, focused expression, casual outfit, photorealistic style",
        "Portrait of teenage girl relaxing in her room, holding phone, fairy lights background, golden hour lighting, comfortable loungewear, candid moment, photorealistic",
        "Teen girl at her desk journaling, thoughtful expression, aesthetic bedroom setup, warm lamp lighting, casual clothes, natural pose, photorealistic photography",
        "Portrait of teenage girl video calling on laptop, waving and smiling, bedroom background, soft natural light, casual outfit, authentic moment, photorealistic",
        "Teen girl lying on bed taking selfie from above, phone camera view, cozy bedroom, string lights, casual clothes, happy expression, photorealistic style",
        "Portrait of teenage girl standing by window, natural daylight, bedroom interior, casual modern outfit, candid pose, soft focus background, photorealistic",
        "Teen girl sitting on floor with books and laptop, study session, bedroom background, afternoon light, comfortable clothes, concentrated look, photorealistic photography"
    ]
    import random
    return random.choice(prompts)

def generate_image_fal(prompt, lora_url):
    """Generate square image using FAL AI with strong Lora influence"""
    log(f"Generating square image with FAL AI...")
    log(f"Prompt: {prompt[:80]}...")
    log(f"Lora URL: {lora_url[:60]}...")
    
    headers = {
        "Authorization": f"Key {FAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Optimized payload for better Lora usage
    payload = {
        "prompt": prompt,
        "loras": [
            {
                "path": lora_url,
                "scale": 1.2  # Increased for stronger Lora effect
            }
        ],
        "image_size": "square",
        "num_images": 1,
        "num_inference_steps": 28,
        "guidance_scale": 3.5,
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
            log(f"✓ Image generated successfully!")
            log(f"  Image URL: {image_url}")
            log(f"  Dimensions: {width}x{height}")
            return image_url
        else:
            raise Exception(f"No images in response: {result}")
    except Exception as e:
        log(f"✗ Error generating image: {e}")
        raise

def trigger_composio_recipe(image_url):
    """Trigger Composio recipe using SDK"""
    log("\nTriggering Composio recipe...")
    log(f"Recipe ID: {RECIPE_ID}")
    log(f"Image URL: {image_url[:60]}...")
    
    try:
        from composio_rube import Rube
        
        # Initialize Rube client
        rube = Rube(api_key=COMPOSIO_TOKEN)
        
        # Execute recipe
        result = rube.execute_recipe(
            recipe_id=RECIPE_ID,
            params={
                "facebook_page_id": FACEBOOK_PAGE_ID,
                "image_url": image_url
            }
        )
        
        log(f"✓ Recipe executed successfully!")
        
        # Extract result data
        if isinstance(result, dict):
            log(f"  Post ID: {result.get('post_id', 'N/A')}")
            log(f"  Permalink: {result.get('permalink', 'N/A')}")
            caption = result.get('caption', 'N/A')
            log(f"  Caption: {caption[:80]}..." if len(caption) > 80 else f"  Caption: {caption}")
        
        return result
    except ImportError:
        log("✗ composio-rube SDK not installed. Install with: pip install composio-rube")
        raise
    except Exception as e:
        log(f"✗ Error triggering recipe: {e}")
        raise

def main():
    log("="*60)
    log("Teen Girl FB Auto-Poster (Hybrid Mode)")
    log("Square Images | Strong Lora | Context-Aware Captions")
    log("="*60)
    
    # Validate required vars
    if not FAL_API_KEY:
        log("ERROR: FAL_API_KEY is required")
        sys.exit(1)
    if not LORA_MODEL_URL:
        log("ERROR: LORA_MODEL_URL is required")
        sys.exit(1)
    if not COMPOSIO_TOKEN:
        log("ERROR: COMPOSIO_TOKEN is required")
        sys.exit(1)
    
    log(f"\n✓ All environment variables present")
    log(f"  FAL_API_KEY: {FAL_API_KEY[:20]}...")
    log(f"  LORA_MODEL_URL: {LORA_MODEL_URL[:50]}...")
    log(f"  COMPOSIO_TOKEN: {COMPOSIO_TOKEN[:30]}...")
    
    try:
        # Step 1: Generate image with FAL
        log("\n" + "="*60)
        log("STEP 1: Generate Square Image with FAL AI + Lora")
        log("="*60)
        prompt = generate_image_prompt()
        image_url = generate_image_fal(prompt, LORA_MODEL_URL)
        
        # Step 2: Trigger Composio recipe
        log("\n" + "="*60)
        log("STEP 2: Publish to Facebook via Composio Recipe")
        log("="*60)
        result = trigger_composio_recipe(image_url)
        
        log("\n" + "="*60)
        log("✓ SUCCESS! Post published to Nethmi G Facebook page")
        log("="*60)
        
        # Print final summary
        summary = {
            "success": True,
            "image_url": image_url,
            "recipe_result": result
        }
        print("\n" + json.dumps(summary, indent=2))
        
    except Exception as e:
        log("\n" + "="*60)
        log("✗ FAILED")
        log("="*60)
        log(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
