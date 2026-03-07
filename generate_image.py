import os
import sys
import random
import requests
import time
import json
from datetime import datetime

def log(msg):
    print(f"[{datetime.utcnow().isoformat()}] {msg}")

# IMPROVED: Diverse prompts with mature age, varied poses, outfits, occasions
PROMPTS = [
    # Casual home scenes
    "photo of a young woman age 19, sitting on bed with laptop, casual hoodie and jeans, bedroom, natural daylight, relaxed pose",
    "photo of a young woman age 18, standing by window, oversized sweater and leggings, cozy home interior, morning light",
    "photo of a teen woman age 20, lying on couch reading book, casual t-shirt and shorts, living room, afternoon lighting",
    
    # Getting ready / fashion
    "photo of a young woman age 19, standing in front of mirror, trying on jacket, casual outfit, bedroom, natural light",
    "photo of a young woman age 18, sitting at desk doing makeup, crop top and jeans, vanity mirror, soft lighting",
    "photo of a teen woman age 20, picking outfit from closet, tank top and pants, bedroom, bright daylight",
    
    # Study / work from home
    "photo of a young woman age 19, sitting at desk with books and coffee, casual cardigan, home office, desk lamp lighting",
    "photo of a young woman age 18, lying on floor surrounded by notes, hoodie and sweatpants, bedroom, studying scene",
    "photo of a teen woman age 20, sitting cross-legged with notebook, comfy clothes, bedroom floor, natural light",
    
    # Social / going out prep
    "photo of a young woman age 19, standing full body, cute dress and sneakers, bedroom, getting ready to go out, window light",
    "photo of a young woman age 18, sitting on bed putting on shoes, jeans and nice top, bedroom, evening preparation",
    "photo of a teen woman age 20, checking phone, casual chic outfit, standing pose, bedroom, natural lighting",
    
    # Relaxing / weekend vibes
    "photo of a young woman age 19, lying in bed with phone, pajama top, cozy blankets, bedroom, lazy morning",
    "photo of a young woman age 18, sitting on floor with snacks, oversized tee and shorts, bedroom, Netflix vibes",
    "photo of a teen woman age 20, lounging on bean bag, comfy clothes, bedroom, relaxed weekend afternoon",
    
    # Active / energetic
    "photo of a young woman age 19, standing stretching arms up, athletic wear, bedroom, morning energy",
    "photo of a young woman age 18, sitting on yoga mat, sports bra and leggings, bedroom workout space, bright light",
    "photo of a teen woman age 20, dancing pose with headphones, casual clothes, bedroom, fun mood",
    
    # Different outfits
    "photo of a young woman age 19, sitting on edge of bed, sundress, bedroom, summer day lighting",
    "photo of a young woman age 18, standing casual pose, graphic tee and skirt, bedroom, natural window light",
    "photo of a teen woman age 20, sitting on chair, flannel shirt and jeans, cozy room interior",
    
    # Food / snack time
    "photo of a young woman age 19, sitting with plate of food, casual home clothes, bedroom picnic style, daylight",
    "photo of a young woman age 18, standing holding mug, comfy sweater, kitchen background, morning coffee vibes",
    "photo of a teen woman age 20, sitting eating snacks, casual tee, bedroom, afternoon snack time",
]

# Enhanced negative prompt
NEGATIVE_PROMPT = "child, childish, young child, kid, minor, underage, baby face, deformed, distorted, disfigured, bad anatomy, wrong anatomy, extra limbs, extra arms, missing arms, fused fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, ugly, bad proportions, malformed limbs, blurry, low quality, watermark, text, duplicate, clone"

log("Generating HIGH RESOLUTION image with FAL (Square HD 1024x1024, 35 steps)...")
prompt = random.choice(PROMPTS)
log(f"Prompt: {prompt}")
log(f"Negative prompt: {NEGATIVE_PROMPT[:100]}...")

fal_key = os.environ.get("FAL_API_KEY").strip()
lora_url = os.environ.get("LORA_MODEL_URL").strip()

# Submit to queue
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

if not request_id:
    log(f"✗ No request_id in response: {queue_data}")
    sys.exit(1)

log(f"✓ Queued with request_id: {request_id}")

# Poll status
status_url = f"https://queue.fal.run/fal-ai/flux-lora/requests/{request_id}"
max_wait = 180
start_time = time.time()
checks = 0

while (time.time() - start_time) < max_wait:
    time.sleep(5)
    checks += 1
    
    status_resp = requests.get(
        status_url,
        headers={"Authorization": f"Key {fal_key}"},
        timeout=30,
    )
    
    if status_resp.status_code != 200:
        log(f"Check #{checks}: HTTP {status_resp.status_code}")
        continue
    
    try:
        status_data = status_resp.json()
    except:
        log(f"Check #{checks}: Failed to parse JSON")
        continue
    
    if checks <= 3:
        log(f"Check #{checks} response keys: {list(status_data.keys())}")
    
    # Check for completion
    if "images" in status_data and status_data.get("images"):
        images = status_data["images"]
        if images and len(images) > 0:
            image_url = images[0].get("url")
            if image_url:
                log(f"✓ Image generated: {image_url}")
                
                with open("image_url.txt", "w") as f:
                    f.write(image_url)
                
                gh_out = os.environ.get("GITHUB_OUTPUT")
                if gh_out:
                    with open(gh_out, "a") as f:
                        f.write(f"image_url={image_url}\n")
                
                sys.exit(0)
    
    status = status_data.get("status") or status_data.get("state")
    log(f"Check #{checks}: status={status}")
    
    if status in ["COMPLETED", "completed", "success"]:
        images = status_data.get("images", [])
        if not images:
            log(f"✗ Completed but no images: {status_data}")
            sys.exit(1)
        
        image_url = images[0]["url"]
        log(f"✓ Image generated: {image_url}")
        
        with open("image_url.txt", "w") as f:
            f.write(image_url)
        
        gh_out = os.environ.get("GITHUB_OUTPUT")
        if gh_out:
            with open(gh_out, "a") as f:
                f.write(f"image_url={image_url}\n")
        
        sys.exit(0)
    
    elif status in ["FAILED", "failed", "error"]:
        error = status_data.get("error", "Unknown error")
        log(f"✗ Generation failed: {error}")
        sys.exit(1)

log(f"✗ Timeout after {max_wait}s")
sys.exit(1)
