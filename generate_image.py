import os
import sys
import random
import requests
import time
import json
from datetime import datetime

def log(msg):
    print(f"[{datetime.utcnow().isoformat()}] {msg}")

# OUTDOOR & VARIED LOCATIONS: Parks, cafes, streets, beach, gym, etc.
PROMPTS = [
    # Park & outdoor nature
    "photo of a young woman age 19, sitting on park bench, white crop top and denim shorts, park with trees, sunny day, natural lighting",
    "photo of a young woman age 18, walking on path, black crop top and high-waisted skinny jeans, city park, casual outdoor vibe",
    "photo of a teen woman age 20, sitting on grass, oversized crop tee and biker shorts, park picnic area, relaxed outdoor look",
    "photo of a young woman age 19, standing by tree, fitted crop top and pleated mini skirt, botanical garden, spring vibes",

    # Beach & waterfront
    "photo of a young woman age 18, standing on beach, sports bra and high-waisted shorts, beach sunset, summer aesthetic",
    "photo of a teen woman age 20, sitting on beach towel, crop bikini top and denim cutoffs, beach, vacation vibes",
    "photo of a young woman age 19, walking on boardwalk, tank top and athletic shorts, beach pier, coastal style",
    "photo of a young woman age 18, sitting on rocks, crop top and yoga leggings, rocky beach, ocean background",

    # Coffee shop & cafe
    "photo of a teen woman age 20, sitting at cafe table, oversized tee and tight denim shorts, outdoor cafe, coffee date style",
    "photo of a young woman age 19, standing with coffee cup, tank top and high-waisted jeans, cafe patio, casual chic",
    "photo of a young woman age 18, sitting by window, crop sweater and skinny jeans, cozy cafe interior, autumn vibes",
    "photo of a teen woman age 20, leaning on counter, fitted top and bike shorts, modern cafe, trendy look",

    # Urban streets & city
    "photo of a young woman age 19, walking on sidewalk, crop top and black skinny jeans, city street, urban style",
    "photo of a young woman age 18, standing by graffiti wall, fitted tank and ripped jeans, downtown alley, streetwear aesthetic",
    "photo of a teen woman age 20, sitting on steps, off-shoulder top and tight jeans, city building entrance, edgy look",
    "photo of a young woman age 19, leaning on railing, crop hoodie and leggings, urban bridge, street fashion",

    # Gym & fitness center
    "photo of a young woman age 18, standing in gym, sports bra and tight shorts, gym mirror background, workout ready",
    "photo of a teen woman age 20, sitting on gym bench, crop sports top and leggings, fitness center, athletic vibe",
    "photo of a young woman age 19, stretching pose, athletic tank and bike shorts, gym studio, active lifestyle",
    "photo of a young woman age 18, holding water bottle, compression top and gym shorts, fitness center, post-workout",

    # Shopping & retail
    "photo of a teen woman age 20, standing in store, crop top and mini skirt, boutique shop, shopping spree vibe",
    "photo of a young woman age 19, trying on clothes, fitted top and denim skirt, clothing store mirror, fashion shopping",
    "photo of a young woman age 18, walking with bags, tank top and shorts, mall corridor, shopping day",
    "photo of a teen woman age 20, sitting in store, bodycon dress, boutique fitting area, trying outfits",

    # Library & study spaces
    "photo of a young woman age 19, sitting at desk, crop sweater and jeans, library study area, student life",
    "photo of a young woman age 18, standing by bookshelf, fitted tee and leggings, library interior, casual academic",
    "photo of a teen woman age 20, reading at table, tank top and bike shorts, study lounge, focused vibe",
    "photo of a young woman age 19, walking between shelves, crop cardigan and shorts, modern library, studious look",

    # Rooftop & balcony
    "photo of a young woman age 18, standing on rooftop, crop top and high-waisted jeans, city skyline background, golden hour",
    "photo of a teen woman age 20, sitting on balcony railing, sports bra and shorts, apartment balcony, sunset vibes",
    "photo of a young woman age 19, leaning on edge, tank top and skinny jeans, rooftop terrace, evening lights",
    "photo of a young woman age 18, standing with view, fitted dress, balcony overlooking city, dreamy aesthetic",

    # Restaurant & dining
    "photo of a teen woman age 20, sitting at restaurant table, halter top and jeans, trendy restaurant, dinner date",
    "photo of a young woman age 19, standing by bar, crop top and mini skirt, restaurant interior, going out look",
    "photo of a young woman age 18, sitting in booth, tube top and shorts, diner setting, casual meal vibes",
    "photo of a teen woman age 20, at outdoor dining, fitted tank and skirt, patio restaurant, brunch style",

    # Pool & resort
    "photo of a young woman age 19, sitting poolside, bikini top and shorts, hotel pool area, vacation mode",
    "photo of a young woman age 18, standing by pool, crop swimsuit and sarong, resort pool, summer getaway",
    "photo of a teen woman age 20, lying on lounge chair, sports bikini and sunglasses, poolside, relaxed vacation",
    "photo of a young woman age 19, walking around pool, swim top and cover-up shorts, resort setting, tropical vibes",
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
