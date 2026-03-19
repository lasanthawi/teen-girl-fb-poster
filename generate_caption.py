"""
Generate a short caption for the post.
Uses OpenAI if OPENAI_API_KEY is set; otherwise picks from template list.
"""
import os
import sys
import random
from datetime import datetime

def log(msg):
    print(f"[{datetime.utcnow().isoformat()}] {msg}")

# Fallback captions (teen / lifestyle style, no API needed)
TEMPLATE_CAPTIONS = [
    "Good vibes only ✨",
    "Feeling cute, might delete later 😌",
    "Living for this moment 🌸",
    "Just another day in paradise ☀️",
    "Coffee and confidence ☕",
    "Outfit check ✓",
    "No filter needed 🌿",
    "Making memories 💫",
    "Chill day best day",
    "Sunset mood 🌅",
    "Good energy only",
    "Living my best life rn",
    "Little moments, big feelings",
    "Today’s vibe: grateful",
    "Here for a good time ✌️",
]

def generate_with_openai():
    """Generate caption via OpenAI if key is set."""
    try:
        from openai import OpenAI
    except ImportError:
        return None
    api_key = (os.environ.get("OPENAI_API_KEY") or "").strip()
    if not api_key:
        return None
    client = OpenAI(api_key=api_key)
    try:
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You write short, casual social media captions for a teen/lifestyle photo. One line, no hashtags, friendly and natural. Reply with only the caption text."
                },
                {
                    "role": "user",
                    "content": "Write a caption for a casual photo (outfit, cafe, or lifestyle). One short sentence only."
                }
            ],
            max_tokens=60,
        )
        text = (r.choices[0].message.content or "").strip()
        return text if text else None
    except Exception as e:
        log(f"OpenAI caption failed: {e}")
        return None

def main():
    log("Generating caption...")
    caption = generate_with_openai()
    if not caption:
        caption = random.choice(TEMPLATE_CAPTIONS)
        log("Using template caption (set OPENAI_API_KEY for AI captions)")
    else:
        log("Using OpenAI-generated caption")
    log(f"Caption: {caption}")
    with open("caption.txt", "w", encoding="utf-8") as f:
        f.write(caption)
    log("✓ Caption saved to caption.txt")
    sys.exit(0)

if __name__ == "__main__":
    main()
