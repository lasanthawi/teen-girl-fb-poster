#!/usr/bin/env python3
"""
Teen Girl Daily Log - Facebook Auto-Poster
Generates AI images with custom Lora and posts to Facebook
"""

import os
import sys
import json
import time
import requests
from datetime import datetime

# Configuration from environment variables
FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")
FAL_API_KEY = os.getenv("FAL_API_KEY", "").strip()  # Remove any whitespace/newlines
LORA_MODEL_URL = os.getenv("LORA_MODEL_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
POSTS_TO_GENERATE = int(os.getenv("POSTS_TO_GENERATE", "1"))

def log(msg):
    """Timestamped logging"""
    print(f"[{datetime.utcnow().isoformat()}] {msg}")

def fetch_recent_posts():
    """Fetch recent Facebook posts for context"""
    log("Fetching recent Facebook posts...")
    url = f"https://graph.facebook.com/v23.0/{FACEBOOK_PAGE_ID}/posts"
    params = {
        "fields": "id,message,created_time",
        "limit": 10,
        "access_token": FACEBOOK_ACCESS_TOKEN
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        posts = data.get("data", [])
        log(f"Found {len(posts)} previous posts")
        return posts
    except Exception as e:
        log(f"Warning: Could not fetch posts: {e}")
        return []

def generate_prompts(context, count):
    """Generate image prompts and captions using OpenAI"""
    log(f"Generating {count} prompts and captions...")
    
    prompt = f"""
You are creating content for a teen girl's daily log Facebook page.

PREVIOUS POSTS CONTEXT:
{json.dumps(context[:5], indent=2) if context else "No previous posts - fresh start!"}

Generate {count} NEW daily log prompts that:
1. Continue the story naturally
2. Represent authentic teen girl daily activities
3. Are diverse (different settings, moods, times)
4. Feel genuine and relatable

Return ONLY valid JSON array:
[{{"image_prompt": "detailed prompt", "caption": "teen caption with emojis"}}]

Image prompts should be detailed: character, setting, activity, mood, lighting, style.
"""
    
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-4-turbo-preview",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.8
    }
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        result = response.json()
        content = result["choices"][0]["message"]["content"].strip()
        
        # Clean markdown
        if content.startswith("```"):
            content = "\n".join(content.split("\n")[1:-1])
        
        prompts_data = json.loads(content)
        log(f"Generated {len(prompts_data)} prompts")
        return prompts_data
    except Exception as e:
        log(f"Error generating prompts: {e}")
        raise

def generate_image_fal(prompt, lora_url):
    """Generate image using FAL AI with Lora model"""
    log(f"Generating image with FAL: {prompt[:60]}...")
    
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
        # Submit request
        response = requests.post(
            "https://fal.run/fal-ai/flux-2/lora",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        result = response.json()
        
        images = result.get("images", [])
        if images:
            image_url = images[0].get("url")
            log(f"Image generated: {image_url}")
            return image_url
        else:
            raise Exception(f"No images in response: {result}")
    except Exception as e:
        log(f"Error generating image: {e}")
        raise

def publish_to_facebook(image_url, caption):
    """Publish photo post to Facebook page"""
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
        log(f"Published! Post ID: {post_id}")
        return post_id
    except Exception as e:
        log(f"Error publishing to Facebook: {e}")
        raise

def main():
    """Main workflow"""
    log("=== Teen Girl Daily Log Auto-Poster Started ===")
    
    # Validate env vars
    required_vars = {
        "FACEBOOK_PAGE_ID": FACEBOOK_PAGE_ID,
        "FACEBOOK_ACCESS_TOKEN": FACEBOOK_ACCESS_TOKEN,
        "FAL_API_KEY": FAL_API_KEY,
        "LORA_MODEL_URL": LORA_MODEL_URL,
        "OPENAI_API_KEY": OPENAI_API_KEY
    }
    
    missing = [k for k, v in required_vars.items() if not v]
    if missing:
        log(f"ERROR: Missing required environment variables: {missing}")
        sys.exit(1)
    
    try:
        # Step 1: Fetch context
        recent_posts = fetch_recent_posts()
        
        # Step 2: Generate prompts
        prompts_data = generate_prompts(recent_posts, POSTS_TO_GENERATE)
        
        # Step 3 & 4: Generate images and publish
        published = []
        for i, item in enumerate(prompts_data, 1):
            log(f"\n--- Processing post {i}/{len(prompts_data)} ---")
            
            try:
                # Generate image
                image_url = generate_image_fal(item["image_prompt"], LORA_MODEL_URL)
                
                # Publish
                post_id = publish_to_facebook(image_url, item["caption"])
                
                published.append({
                    "post_id": post_id,
                    "caption": item["caption"]
                })
                
                # Rate limit pause
                if i < len(prompts_data):
                    time.sleep(5)
                    
            except Exception as e:
                log(f"Failed to process post {i}: {e}")
                continue
        
        log(f"\n=== Complete! Published {len(published)} posts ===")
        
        # Output summary
        summary = {
            "success": True,
            "posts_published": len(published),
            "details": published
        }
        print(json.dumps(summary, indent=2))
        
    except Exception as e:
        log(f"FATAL ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
