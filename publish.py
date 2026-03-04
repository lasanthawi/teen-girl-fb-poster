import os
import sys
import requests
from datetime import datetime

def log(msg):
    print(f"[{datetime.utcnow().isoformat()}] {msg}")

def main():
    # Read image URL from file
    with open('image_url.txt', 'r') as f:
        image_url = f.read().strip()
    
    log(f"Publishing image: {image_url}")
    
    # Get secrets
    webhook_url = os.environ.get('WEBHOOK_URL')
    webhook_secret = os.environ.get('WEBHOOK_SECRET')
    
    if not webhook_url or not webhook_secret:
        log("✗ Error: WEBHOOK_URL or WEBHOOK_SECRET not set")
        sys.exit(1)
    
    log(f"Calling webhook: {webhook_url}")
    
    try:
        response = requests.post(
            webhook_url,
            json={
                "image_url": image_url,
                "secret": webhook_secret
            },
            timeout=120
        )
        
        log(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            log(f"✓ Success!")
            log(f"Post ID: {result.get('post_id', 'N/A')}")
            log(f"Permalink: {result.get('permalink', 'N/A')}")
            log(f"Caption: {result.get('caption', 'N/A')[:100]}...")
        else:
            log(f"Response: {response.text[:500]}")
            log(f"✗ Failed with status {response.status_code}")
            sys.exit(1)
            
    except Exception as e:
        log(f"✗ Exception: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
