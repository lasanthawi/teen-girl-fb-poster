#!/usr/bin/env python3
"""
Teen Girl Daily Log - All-in-One Auto-Poster
Generates images with Lora, creates captions, and posts to Facebook
"""

import os
import sys
import json
import requests
from datetime import datetime

# Configuration
FAL_API_KEY = os.getenv("FAL_API_KEY", "").strip()
LORA_MODEL_URL = os.getenv("LORA_MODEL_URL")
FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID", "1025914070602506")
FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN", "").strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()

def log(msg):
    print(f"[{datetime.utcnow().isoformat()}] {msg}")

def fetch_recent_posts():
    """Fetch recent posts for context"""
    log("Fetching recent Facebook posts for context...")
    url = f"https://graph.facebook.com/v23.0/{FACEBOOK_PAGE_ID}/posts"
    params = {
        "fields": "message,created_time",
        "limit": 5,
        "access_token": FACEBOOK_ACCESS_TOKEN
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        posts = data.get("data", [])
        log(f"Found {len(posts)} recent posts")
        return posts
    except Exception as e:
        log(f"Warning: Couldn't fetch posts: {e}")
        return []

def generate_caption(context):
    """Generate teen girl caption using OpenAI"""
    log("Generating caption with AI...")
    
    context_text = json.dumps(context[:3], indent=2) if context else "Fresh start!"
    
    prompt = f"""
You're writing a Facebook caption for a teen girl's daily log page.

Recent posts context:
{context_text}

Create ONE short, authentic teen caption that:
- Continues the story naturally
- Uses casual language with 2-3 emojis
- Is 2-3 sentences
- Feels genuine and relatable

Return ONLY the caption text (no JSON, no quotes).
"""
    
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-4-turbo-preview",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.8,
        "max_tokens": 150
    }
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        caption = result["choices"][0]["message"]["content"].strip()
        
        # Clean up quotes if added
        if caption.startswith('"') and caption.endswith('"'):
            caption = caption[1:-1]
        if caption.startswith("'") and caption.endswith("'"):
            caption = caption[1:-1]
        
        log(f"Caption: {caption[:60]}..." if len(caption) > 60 else f"Caption: {caption}")
        return caption
    except Exception as e:
        log(f"Error generating caption: {e}")
        return "just vibing today ✨💭"

def generate_image_prompt():
    """Simple prompts for Lora"""
    prompts = [
        "young woman mirror selfie in bedroom",
        "young woman studying with laptop",
        "young woman relaxing with phone",
        "young woman journaling at desk",
        "young woman video calling smiling",
        "young woman taking selfie on bed",
        "young woman by window natural light",
        "young woman with books on floor"
    ]
    import random
    return random.choice(prompts)

def generate_image_fal(prompt, lora_url):
    """Generate square image with MAXIMUM Lora"""
    log(f"Generating image with FAL (Lora scale 1.8)...")
    log(f"Prompt: {prompt}")
    
    headers = {
        "Authorization": f"Key {FAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": prompt + ", casual clothes, photorealistic",
        "loras": [{"path": lora_url, "scale": 1.8}],
        "image_size": "square",
        "num_images": 1,
        "num_inference_steps": 35,
        "guidance_scale": 2.5,
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
            log(f"✓ Image: {image_url}")
            return image_url
        else:
            raise Exception(f"No images: {result}")
    except Exception as e:
        log(f"✗ Error: {e}")
        raise

def publish_to_facebook(image_url, caption):
    """Publish directly to Facebook"""
    log(f"Publishing to Facebook...")
    
    url = f"https://graph.facebook.com/v23.0/{FACEBOOK_PAGE_ID}/photos"
    payload = {
        "url": image_url,
        "message": caption,
        "access_token": FACEBOOK_ACCESS_TOKEN
    }
    
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        result = response.json()
        post_id = result.get("id", result.get("post_id", ""))
        log(f"✓ Published! Post ID: {post_id}")
        log(f"  Link: https://facebook.com/{post_id}")
        return post_id
    except Exception as e:
        log(f"✗ Error: {e}")
        raise

def main():
    log("="*60)
    log("Teen Girl FB Poster - Direct Mode")
    log("Lora 1.8 | Square | Context-Aware")
    log("="*60)
    
    # Validate
    required = {
        "FAL_API_KEY": FAL_API_KEY,
        "LORA_MODEL_URL": LORA_MODEL_URL,
        "FACEBOOK_ACCESS_TOKEN": FACEBOOK_ACCESS_TOKEN,
        "OPENAI_API_KEY": OPENAI_API_KEY
    }
    
    missing = [k for k, v in required.items() if not v]
    if missing:
        log(f"ERROR: Missing: {missing}")
        sys.exit(1)
    
    log(f"\n✓ Config OK")
    log(f"  Lora scale: 1.8 (MAXIMUM)")
    log(f"  Image: square 512x512")
    
    try:
        # Step 1: Fetch context
        log("\n" + "="*60)
        log("STEP 1: Fetch Context")
        log("="*60)
        recent_posts = fetch_recent_posts()
        
        # Step 2: Generate image
        log("\n" + "="*60)
        log("STEP 2: Generate Image (Strong Lora)")
        log("="*60)
        prompt = generate_image_prompt()
        image_url = generate_image_fal(prompt, LORA_MODEL_URL)
        
        # Step 3: Generate caption
        log("\n" + "="*60)
        log("STEP 3: Generate Caption")
        log("="*60)
        caption = generate_caption(recent_posts)
        
        # Step 4: Publish
        log("\n" + "="*60)
        log("STEP 4: Publish to Facebook")
        log("="*60)
        post_id = publish_to_facebook(image_url, caption)
        
        log("\n" + "="*60)
        log("✓ SUCCESS! Nethmi G page updated")
        log("="*60)
        
        print("\n" + json.dumps({
            "success": True,
            "image_url": image_url,
            "post_id": post_id,
            "caption": caption,
            "lora_scale": 1.8
        }, indent=2))
        
    except Exception as e:
        log("\n" + "="*60)
        log("✗ FAILED")
        log("="*60)
        log(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
