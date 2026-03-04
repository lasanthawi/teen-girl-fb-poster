import os
import sys
from datetime import datetime

def log(msg):
    print(f"[{datetime.utcnow().isoformat()}] {msg}")

# Read image URL from file
with open('image_url.txt', 'r') as f:
    image_url = f.read().strip()

log(f"✓ Image generated: {image_url}")
log("Image URL saved. Rube will handle publishing.")

# Output for GitHub Actions
print(f"::set-output name=image_url::{image_url}")

# Success - Rube will pick this up and publish
sys.exit(0)
