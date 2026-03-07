import os
import sys
import random
import requests
import time
from datetime import datetime

def log(msg):
    print(f"[{datetime.utcnow().isoformat()}] {msg}")

# Improved prompts with better anatomy specifications
PROMPTS = [
    "photo of a young woman, portrait, natural pose with arms at sides, sitting on bed, casual clothes, looking at camera, soft lighting, high quality, detailed",
    "photo of a teen girl, full body, standing naturally with both arms visible and relaxed at sides, bedroom background, modern casual outfit, natural lighting",
    "photo of a young woman, waist up portrait, arms resting naturally on lap, sitting cross-legged on bed, cozy room, casual top, natural daylight",
    "photo of a teen girl, portrait shot, hands visible resting on knees, sitting position, casual everyday clothes, bedroom interior, soft natural light",
    "photo of a young woman, three-quarter view, natural standing pose with proper arm anatomy, casual dress, indoor setting, window light, high detail",
    "photo of a teen girl, seated portrait, both hands visible and naturally positioned, relaxed pose, modern casual attire, bright room, photorealistic",
    "photo of a young woman, upper body shot, arms in natural resting position, sitting on chair, everyday clothing, home interior, good lighting, detailed",
    "photo of a teen girl, portrait, natural pose with correct anatomy, both arms clearly visible, casual modern outfit, bedroom scene, professional quality",
]

# Negative prompt to avoid common AI artifacts
NEGATIVE_PROMPT = "deformed, distorted, disfigured, bad anatomy, wrong anatomy, extra limbs, extra arms, extra hands, extra fingers, missing arms, missing hands, fused fingers, too many fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, ugly, bad proportions, gross proportions, malformed limbs, floating limbs, disconnected limbs, long neck, cross-eyed, blurry, low quality, watermark, text"

log("Generating HIGH RESOLUTION image with FAL (async queue, Lora 1.8, Square HD 1024x1024, 35 steps)...")
prompt = random.choice(PROMPTS)
log(f"Prompt: {prompt}")
log(f"Negative prompt: {NEGATIVE_PROMPT[:100]}...")

fal_key = os.environ.get("FAL_API_KEY").strip()
lora_url = os.environ.get("LORA_MODEL_URL").strip()

# Step 1: Submit to queue (async) - returns immediately with request_id
log("Submitting to FAL queue...")
submit_resp = requests.post(
    "https://queue.fal.run/fal-ai/flux-lora",
    headers={
        "Authorization": f"Key {fal_key}",
        "Content-Type": "application/json",
    },
    json={
        "prompt": prompt,
        "negative_prompt": NEGATIVE_PROMPT,
        "image_size": "square_hd",  # 1024x1024 HD
        "num_inference_steps": 35,
        "guidance_scale": 3.5,
        "num_images": 1,
        "loras": [{"path": lora_url, "scale": 1.8}],
        "enable_safety_checker": True,
    },
    timeout=30,
)

if submit_resp.status_code != 200:
    log(f"✗ FAL queue submit failed: {submit_resp.status_code} {submit_resp.text[:500]}")
    sys.exit(1)

queue_data = submit_resp.json()
request_id = queue_data.get("request_id")
response_url = queue_data.get("response_url")  # Use this for polling

if not request_id or not response_url:
    log(f"✗ Missing request_id or response_url: {queue_data}")
    sys.exit(1)

log(f"✓ Queued with request_id: {request_id}")
log(f"Response URL: {response_url}")

# Step 2: Poll result from response_url (not status_url)
max_wait = 120  # 2 minutes should be enough
start_time = time.time()
checks = 0

while (time.time() - start_time) < max_wait:
    time.sleep(5)  # Check every 5 seconds
    checks += 1
    
    try:
        # Use response_url which returns the actual result when ready
        result_resp = requests.get(
            response_url,
            headers={"Authorization": f"Key {fal_key}"},
            timeout=30,
        )
        
        if result_resp.status_code == 200:
            result_data = result_resp.json()
            
            # Check if we have the final result with images
            if "images" in result_data and len(result_data["images"]) > 0:
                image_url = result_data["images"][0]["url"]
                log(f"✓ Image generated (check #{checks}): {image_url}")
                
                # Save for Rube recipe
                with open("image_url.txt", "w") as f:
                    f.write(image_url)
                
                # GitHub Actions output
                gh_out = os.environ.get("GITHUB_OUTPUT")
                if gh_out:
                    with open(gh_out, "a") as f:
                        f.write(f"image_url={image_url}\n")
                
                sys.exit(0)
            
            # Check for errors
            if "error" in result_data:
                log(f"✗ Generation failed: {result_data['error']}")
                sys.exit(1)
            
            # Still in queue/processing
            status = result_data.get("status", "processing")
            log(f"Check #{checks}: {status}")
        
        elif result_resp.status_code == 404:
            # Request not ready yet
            log(f"Check #{checks}: Request not ready (404)")
        else:
            log(f"Check #{checks}: HTTP {result_resp.status_code}")
    
    except Exception as e:
        log(f"Check #{checks}: Exception - {str(e)[:100]}")

log(f"✗ Timeout after {max_wait}s (image not generated in time)")
sys.exit(1)
