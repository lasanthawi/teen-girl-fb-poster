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

# Composio v3 API (v1 endpoint returned 410 deprecated)
log("Calling Composio recipe...")
resp = requests.post(
    f"https://backend.composio.dev/api/v3/rube/recipes/{recipe_id}/execute",
    headers={
        "x-api-key": token,
        "Content-Type": "application/json",
    },
    json={
        "facebook_page_id": facebook_page_id,
        "image_url": image_url,
    },
    timeout=60,
)

if resp.status_code not in (200, 201):
    log(f"✗ Recipe failed: {resp.status_code} {resp.text[:500]}")
    sys.exit(1)

result = resp.json()
log("✓ SUCCESS! Post published to Facebook")
log(f"Result: {result}")
