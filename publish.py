import os
import sys
import requests
from datetime import datetime
from composio import Composio

def log(msg):
    print(f"[{datetime.utcnow().isoformat()}] {msg}")

# Read image URL from file
with open("image_url.txt", "r") as f:
    image_url = f.read().strip()

log(f"Publishing image: {image_url}")

token = os.environ.get("COMPOSIO_TOKEN").strip()
client = Composio(api_key=token)

log("Calling recipe...")
result = client.rube.execute_recipe(
    recipe_id="rcp_A9M-wR3IZxUp",
    params={
        "facebook_page_id": "1025914070602506",
        "image_url": image_url
    }
)

log("✓ SUCCESS! Post published to Facebook")
log(f"Result: {result}")
