import os
import sys
import requests
from datetime import datetime

def log(msg):
    print(f"[{datetime.utcnow().isoformat()}] {msg}")

# Read image URL from file
with open("image_url.txt", "r") as f:
    image_url = f.read().strip()

log(f"Publishing image: {image_url}")

# Get webhook configuration
webhook_url = os.environ.get("WEBHOOK_URL")
webhook_secret = os.environ.get("WEBHOOK_SECRET")

if not webhook_url or not webhook_secret:
    log("⚠️  WEBHOOK_URL or WEBHOOK_SECRET not set")
    log("Falling back to direct Rube execution (manual trigger needed)")
    log(f"Image URL for manual publishing: {image_url}")
    # Exit successfully so workflow doesn't fail, but note manual action needed
    sys.exit(0)

log(f"Calling Vercel webhook: {webhook_url}")

try:
    resp = requests.post(
        webhook_url,
        json={
            "image_url": image_url,
            "secret": webhook_secret
        },
        timeout=120
    )
    
    log(f"Status Code: {resp.status_code}")
    
    if resp.status_code not in (200, 201):
        log(f"✗ Webhook failed: {resp.status_code}")
        log(f"Response: {resp.text[:500]}")
        sys.exit(1)
    
    result = resp.json()
    log("✓ SUCCESS! Post published to Facebook via webhook")
    
    if "data" in result:
        log(f"Result: {result}")
    else:
        log(f"Result: {result}")
        
except Exception as e:
    log(f"✗ Exception: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
