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

token = os.environ.get("COMPOSIO_TOKEN").strip()
recipe_id = "rcp_A9M-wR3IZxUp"
facebook_page_id = "1025914070602506"

# Composio Recipe API - External endpoint
log("Calling Composio recipe via external API...")

# Try the correct endpoint format
url = f"https://backend.composio.dev/api/v3/recipe/{recipe_id}/execute"
log(f"URL: {url}")

headers = {
    "X-API-KEY": token,
    "Content-Type": "application/json",
}

payload = {
    "input_data": {
        "facebook_page_id": facebook_page_id,
        "image_url": image_url,
    }
}

log(f"Headers: X-API-KEY: {token[:20]}...")
log(f"Payload: {payload}")

try:
    resp = requests.post(url, headers=headers, json=payload, timeout=120)
    log(f"Status Code: {resp.status_code}")
    log(f"Response Headers: {dict(resp.headers)}")
    log(f"Response Text: {resp.text[:500]}")
    
    if resp.status_code not in (200, 201):
        log(f"✗ Recipe failed: {resp.status_code} {resp.text[:500]}")
        sys.exit(1)
    
    result = resp.json()
    log("✓ SUCCESS! Post published to Facebook")
    
    # Extract relevant data from response
    if "data" in result and "data" in result["data"]:
        post_data = result["data"]["data"]
        log(f"Post ID: {post_data.get('post_id', 'N/A')}")
        log(f"Caption: {post_data.get('caption', 'N/A')[:100]}...")
        log(f"Permalink: {post_data.get('permalink', 'N/A')}")
    else:
        log(f"Result: {result}")
        
except Exception as e:
    log(f"✗ Exception: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
