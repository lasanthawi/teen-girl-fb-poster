import os
import sys
from datetime import datetime
from composio import Composio, Action

def log(msg):
    print(f"[{datetime.utcnow().isoformat()}] {msg}")

# Read image URL from file
with open("image_url.txt", "r") as f:
    image_url = f.read().strip()

log(f"Publishing image: {image_url}")

api_key = os.environ.get("COMPOSIO_TOKEN").strip()
facebook_page_id = "1025914070602506"

try:
    # Initialize Composio client
    log("Initializing Composio client...")
    client = Composio(api_key=api_key)
    
    # Step 1: Get recent posts for context
    log("Fetching recent Facebook posts...")
    posts_result = client.execute_action(
        action=Action.FACEBOOK_GET_PAGE_POSTS,
        params={
            "page_id": facebook_page_id,
            "limit": 10,
            "fields": "id,message,created_time"
        }
    )
    
    log(f"Posts result: {posts_result}")
    
    # Step 2: Generate caption (simplified for now)
    caption = "✨ daily chaos update 📚💭 keeping it real"
    
    # Step 3: Publish to Facebook
    log(f"Publishing to Facebook with caption: {caption}")
    result = client.execute_action(
        action=Action.FACEBOOK_CREATE_PHOTO_POST,
        params={
            "page_id": facebook_page_id,
            "url": image_url,
            "message": caption,
            "published": True
        }
    )
    
    log("✓ SUCCESS! Post published to Facebook")
    log(f"Result: {result}")
    
    # Extract post ID
    if hasattr(result, 'data'):
        post_data = result.data
    else:
        post_data = result
    
    log(f"Post data: {post_data}")
    
except Exception as e:
    log(f"✗ Exception: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
