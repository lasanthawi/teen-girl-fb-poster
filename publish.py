import os
import sys
from datetime import datetime
from composio import ComposioToolSet, App

def log(msg):
    print(f"[{datetime.utcnow().isoformat()}] {msg}")

# Read image URL from file
with open("image_url.txt", "r") as f:
    image_url = f.read().strip()

log(f"Publishing image: {image_url}")

api_key = os.environ.get("COMPOSIO_TOKEN").strip()
facebook_page_id = "1025914070602506"

try:
    # Initialize Composio
    log("Initializing Composio...")
    toolset = ComposioToolSet(api_key=api_key)
    
    # Get Facebook tools
    log("Getting Facebook tools...")
    tools = toolset.get_tools(apps=[App.FACEBOOK])
    
    # Find the tools we need
    get_posts_tool = next((t for t in tools if "GET_PAGE_POSTS" in t.name), None)
    create_photo_tool = next((t for t in tools if "CREATE_PHOTO_POST" in t.name), None)
    
    if not get_posts_tool or not create_photo_tool:
        log("✗ Required Facebook tools not found")
        sys.exit(1)
    
    log(f"Found tools: {get_posts_tool.name}, {create_photo_tool.name}")
    
    # Step 1: Get recent posts for context
    log("Fetching recent posts...")
    posts_result = get_posts_tool.invoke({
        "page_id": facebook_page_id,
        "limit": 10,
        "fields": "id,message,created_time"
    })
    
    log(f"Posts fetched: {len(posts_result.get('data', {}).get('data', []))} posts")
    
    # Step 2: Generate caption (simplified - you can enhance with LLM)
    log("Using simple caption for now...")
    caption = "✨ daily update from the chaos zone 📚💭"
    
    # Step 3: Publish to Facebook
    log("Publishing to Facebook...")
    result = create_photo_tool.invoke({
        "page_id": facebook_page_id,
        "url": image_url,
        "message": caption,
        "published": True
    })
    
    log("✓ SUCCESS! Post published to Facebook")
    
    # Extract post details
    post_data = result.get('data', {})
    if 'data' in post_data:
        post_data = post_data['data']
    
    post_id = post_data.get('id', post_data.get('post_id', 'N/A'))
    log(f"Post ID: {post_id}")
    log(f"Result: {result}")
    
except Exception as e:
    log(f"✗ Exception: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
