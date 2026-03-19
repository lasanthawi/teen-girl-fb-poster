import os
import sys
import requests
from datetime import datetime

def log(msg):
    print(f"[{datetime.utcnow().isoformat()}] {msg}")

# Read image URL and optional caption
with open("image_url.txt", "r") as f:
    image_url = f.read().strip()

caption = ""
if os.path.isfile("caption.txt"):
    with open("caption.txt", "r", encoding="utf-8") as f:
        caption = f.read().strip()
    log(f"Caption: {caption}")

log(f"Publishing image: {image_url}")

# Get webhook configuration
webhook_url = os.environ.get("WEBHOOK_URL")
webhook_secret = os.environ.get("WEBHOOK_SECRET")

if not webhook_url or not webhook_secret:
    log("✗ WEBHOOK_URL or WEBHOOK_SECRET not set in GitHub Actions secrets")
    log("Add WEBHOOK_URL (e.g. https://your-app.vercel.app/api/webhook) and WEBHOOK_SECRET")
    sys.exit(1)

log(f"Calling Vercel webhook: {webhook_url}")

try:
    payload = {
        "image_url": image_url,
        "secret": webhook_secret,
    }
    if caption:
        payload["caption"] = caption

    resp = requests.post(
        webhook_url,
        json=payload,
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
