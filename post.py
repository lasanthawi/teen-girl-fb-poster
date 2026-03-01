#!/usr/bin/env python3
import os
import sys
import random
import fal_client
from datetime import datetime

def log(msg):
    print(f"[{datetime.utcnow().isoformat()}] {msg}")

def main():
    log("="*60)
    log("FAL Image Generator - Teen Girl Lora")
    log("="*60)
    log("")
    
    # Get credentials
    fal_key = os.environ.get("FAL_API_KEY", "").strip()
    lora_url = os.environ.get("LORA_MODEL_URL", "").strip()
    
    if not fal_key or not lora_url:
        log("✗ Missing FAL_API_KEY or LORA_MODEL_URL")
        sys.exit(1)
    
    log(f"✓ FAL_API_KEY: {fal_key[:20]}...")
    log(f"✓ LORA_MODEL_URL: {lora_url[:50]}...")
    log("")
    
    # Teen girl portrait prompts optimized for Lora
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
    log(f"Selected prompt: {prompt}")
    log("")
    
    log("Generating image with FAL AI + Lora...")
    log(f"  Model: fal-ai/flux-lora")
    log(f"  Lora scale: 1.8 (MAXIMUM)")
    log(f"  Size: square (512x512)")
    log(f"  Steps: 35")
    log("")
    
    try:
        # Configure FAL client
        os.environ["FAL_KEY"] = fal_key
        
        # Generate with strong Lora
        result = fal_client.subscribe(
            "fal-ai/flux-lora",
            arguments={
                "prompt": prompt,
                "loras": [{
                    "path": lora_url,
                    "scale": 1.8  # MAXIMUM strength
                }],
                "image_size": "square",
                "num_inference_steps": 35,
                "guidance_scale": 2.5,
                "num_images": 1,
                "enable_safety_checker": False
            }
        )
        
        image_url = result["images"][0]["url"]
        dimensions = result["images"][0]
        
        log("="*60)
        log("✓ SUCCESS! IMAGE GENERATED")
        log("="*60)
        log(f"Image URL: {image_url}")
        log(f"Size: {dimensions.get('width', 512)}x{dimensions.get('height', 512)}")
        log(f"Lora scale: 1.8 (VERY STRONG)")
        log("")
        log("COPY THIS IMAGE URL TO USE IN YOUR COMPOSIO RECIPE:")
        log(image_url)
        log("="*60)
        
    except Exception as e:
        log(f"✗ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
