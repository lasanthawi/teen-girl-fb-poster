import os
import sys
import random
import requests
import time
import json
from datetime import datetime

def log(msg):
    print(f"[{datetime.utcnow().isoformat()}] {msg}")

# STYLISH & FASHIONABLE: Trendy outfits with shorts, crop tops, leggings, gym wear
PROMPTS = [
    # Crop tops with bottoms
    "photo of a young woman age 19, sitting on bed, white crop top and denim shorts, bedroom, casual summer vibe, natural lighting",
    "photo of a young woman age 18, standing mirror pose, black crop top and high-waisted skinny jeans, bedroom, fashion photo style",
    "photo of a teen woman age 20, sitting on floor, oversized crop tee and biker shorts, bedroom, relaxed streetwear look",
    "photo of a young woman age 19, standing pose, fitted crop top and pleated mini skirt, bedroom, getting ready to go out vibe",

    # Leggings & athletic wear
    "photo of a young woman age 18, sitting cross-legged, sports bra and high-waisted leggings, bedroom yoga mat, fitness aesthetic",
    "photo of a teen woman age 20, standing stretch pose, crop sports top and gym leggings, bedroom, workout outfit",
    "photo of a young woman age 19, sitting on bed, athletic crop top and tight leggings, bedroom, athleisure style",
    "photo of a young woman age 18, lying on floor, sports bra and yoga leggings, bedroom, post-workout relaxed",

    # Shorts varieties
    "photo of a teen woman age 20, standing casual, oversized tee and tight denim shorts, bedroom, summer casual look",
    "photo of a young woman age 19, sitting on chair, tank top and high-waisted shorts, bedroom, laid-back summer style",
    "photo of a young woman age 18, mirror selfie pose, crop top and athletic shorts, bedroom, sporty chic",
    "photo of a teen woman age 20, sitting on bed edge, hoodie and bike shorts, bedroom, comfy streetwear",

    # Skinny jeans & tight bottoms
    "photo of a young woman age 19, standing full body, fitted top and black skinny jeans, bedroom, sleek casual style",
    "photo of a young woman age 18, sitting pose, crop sweater and ripped skinny jeans, bedroom, trendy fall look",
    "photo of a teen woman age 20, standing by window, tank top and tight jeans, bedroom, effortless chic",
    "photo of a young woman age 19, sitting on floor, off-shoulder top and skinny jeans, bedroom, casual date outfit",

    # Skirts & dresses
    "photo of a young woman age 18, standing twirl pose, crop top and tight mini skirt, bedroom, going out look",
    "photo of a teen woman age 20, sitting on bed, fitted top and denim skirt, bedroom, summer day outfit",
    "photo of a young woman age 19, standing mirror, bodycon dress, bedroom, evening ready style",
    "photo of a young woman age 18, sitting pose, flowy mini dress and sneakers, bedroom, casual cute aesthetic",

    # Gym & sports outfits
    "photo of a teen woman age 20, standing ready pose, sports bra and gym shorts, bedroom, pre-workout energy",
    "photo of a young woman age 19, sitting on yoga mat, crop sports top and bike shorts, bedroom, active lifestyle",
    "photo of a young woman age 18, stretching pose, athletic tank and tight workout shorts, bedroom, fitness vibe",
    "photo of a teen woman age 20, standing confident, compression top and leggings, bedroom, gym outfit of the day",

    # Mix & match trendy
    "photo of a young woman age 19, sitting casual, graphic crop tee and cargo pants, bedroom, streetwear style",
    "photo of a young woman age 18, standing pose, halter top and high-waisted jeans, bedroom, trendy summer look",
    "photo of a teen woman age 20, lying on bed, sports bra and sweatpants, bedroom, cozy athletic wear",
    "photo of a young woman age 19, sitting on floor, oversized tee tucked into biker shorts, bedroom, effortless style",

    # More fashion-forward
    "photo of a young woman age 18, standing full length, fitted tank and pleated tennis skirt, bedroom, preppy chic",
    "photo of a teen woman age 20, mirror pose, crop cardigan and high-waisted shorts, bedroom, cute layered look",
    "photo of a young woman age 19, sitting on chair, tube top and skinny jeans, bedroom, night out ready",
    "photo of a young woman age 18, standing confident, crop hoodie and leggings, bedroom, athleisure street style",

    # Bedroom casual stylish
    "photo of a teen woman age 20, sitting relaxed, sports crop top and joggers, bedroom, comfy but cute",
    "photo of a young woman age 19, standing by desk, fitted tee and denim cutoffs, bedroom, casual summer home",
    "photo of a young woman age 18, lying on couch, crop top and athletic shorts, bedroom, lazy day chic",
    "photo of a teen woman age 20, sitting on bed, tank top and tight shorts, bedroom, relaxed weekend style",
]

# Enhanced negative prompt
NEGATIVE_PROMPT = "child, childish, young child, kid, minor, underage, baby face, deformed, distorted, disfigured, bad anatomy, wrong anatomy, extra limbs, extra arms, missing arms, fused fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, ugly, bad proportions, malformed limbs, blurry, low quality, watermark, text, duplicate, clone, baggy clothes, oversized unfitted"

log("Generating HIGH RESOLUTION stylish image with FAL (Square HD 1024x1024, 35 steps)...")
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
