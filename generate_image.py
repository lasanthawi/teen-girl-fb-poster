import os
import sys
import random
import requests
import time
import json
from datetime import datetime

def log(msg):
    print(f"[{datetime.utcnow().isoformat()}] {msg}")

# OUTDOOR & VARIED LOCATIONS with TIGHT ATHLETIC WEAR: Yoga pants, leggings, tight shorts, sports bras
PROMPTS = [
    # Tight yoga pants & leggings - outdoor
    "photo of a young woman age 19, sitting on park bench, sports bra and tight black yoga pants, park with trees, sunny day, fitness vibe",
    "photo of a young woman age 18, walking on path, crop top and high-waisted leggings, city park, athletic outdoor look",
    "photo of a teen woman age 20, stretching on grass, fitted tank and colorful yoga leggings, park picnic area, workout aesthetic",
    "photo of a young woman age 19, standing by tree, sports bra and tight gym leggings, botanical garden, active wear style",
    
    # Tight shorts & bike shorts - beach/outdoor
    "photo of a young woman age 18, standing on beach, sports bra and tight athletic shorts, beach sunset, summer fitness vibe",
    "photo of a teen woman age 20, sitting on beach towel, crop bikini top and spandex bike shorts, beach, sporty beach look",
    "photo of a young woman age 19, walking on boardwalk, tank top and tight denim shorts, beach pier, casual hot style",
    "photo of a young woman age 18, sitting on rocks, fitted top and black bike shorts, rocky beach, athleisure aesthetic",
    
    # Leggings & tight bottoms - cafe/urban
    "photo of a teen woman age 20, sitting at cafe table, crop sweater and skin-tight leggings, outdoor cafe, cozy athletic style",
    "photo of a young woman age 19, standing with coffee cup, sports bra and high-waisted yoga pants, cafe patio, fitness casual",
    "photo of a young woman age 18, sitting by window, fitted tee and printed leggings, cozy cafe interior, athleisure chic",
    "photo of a teen woman age 20, leaning on counter, crop top and tight black leggings, modern cafe, trendy athletic look",
    
    # Gym wear - tight shorts, leggings, sports bras
    "photo of a young woman age 19, standing in gym, sports bra and compression shorts, gym mirror background, workout ready",
    "photo of a young woman age 18, sitting on gym bench, crop sports top and skin-tight leggings, fitness center, athletic hot vibe",
    "photo of a teen woman age 20, stretching pose, sports bra and tight yoga pants, gym studio, active flexibility",
    "photo of a young woman age 19, holding water bottle, compression top and spandex shorts, fitness center, post-workout look",
    
    # Athletic wear - city streets
    "photo of a young woman age 18, walking on sidewalk, sports bra and high-waisted tight shorts, city street, urban athletic style",
    "photo of a teen woman age 20, standing by graffiti wall, crop tank and skin-tight leggings, downtown alley, streetwear fitness",
    "photo of a young woman age 19, sitting on steps, fitted sports top and bike shorts, city building entrance, sporty urban",
    "photo of a young woman age 18, leaning on railing, crop hoodie and tight yoga pants, urban bridge, street athleisure",
    
    # Yoga pants & tight bottoms - various locations
    "photo of a teen woman age 20, standing in store, sports bra and high-waisted yoga leggings, boutique shop, shopping in gym wear",
    "photo of a young woman age 19, trying on clothes, fitted tank and tight black leggings, clothing store mirror, athletic shopping",
    "photo of a young woman age 18, walking with bags, crop top and spandex bike shorts, mall corridor, casual athletic day",
    "photo of a teen woman age 20, sitting in store, bodycon sports dress and leggings, boutique fitting area, sporty trying on",
    
    # Tight shorts & leggings - library/study
    "photo of a young woman age 19, sitting at desk, crop sweater and tight yoga pants, library study area, comfy study athletic",
    "photo of a young woman age 18, standing by bookshelf, fitted tee and skin-tight leggings, library interior, casual study wear",
    "photo of a teen woman age 20, reading at table, sports crop top and bike shorts, study lounge, focused athletic vibe",
    "photo of a young woman age 19, walking between shelves, tank top and high-waisted leggings, modern library, studious athletic",
    
    # Athletic wear - rooftop/balcony
    "photo of a young woman age 18, standing on rooftop, sports bra and tight shorts, city skyline background, golden hour workout",
    "photo of a teen woman age 20, sitting on balcony railing, crop top and skin-tight yoga pants, apartment balcony, sunset athletic",
    "photo of a young woman age 19, leaning on edge, fitted tank and compression leggings, rooftop terrace, evening workout vibe",
    "photo of a young woman age 18, stretching with view, sports bra and tight bike shorts, balcony overlooking city, fitness aesthetic",
    
    # Tight bottoms - restaurant/dining
    "photo of a teen woman age 20, sitting at restaurant table, crop top and high-waisted tight jeans, trendy restaurant, casual dinner date",
    "photo of a young woman age 19, standing by bar, fitted tank and skin-tight leggings, restaurant interior, athletic dining out",
    "photo of a young woman age 18, sitting in booth, sports crop top and tight shorts, diner setting, sporty casual meal",
    "photo of a teen woman age 20, at outdoor dining, fitted top and spandex bike shorts, patio restaurant, athletic brunch style",
    
    # Swimwear & tight athletic wear - pool/resort
    "photo of a young woman age 19, sitting poolside, sports bikini and tight athletic shorts, hotel pool area, vacation workout mode",
    "photo of a young woman age 18, standing by pool, crop swimsuit top and spandex bike shorts, resort pool, athletic summer getaway",
    "photo of a teen woman age 20, lying on lounge chair, sports bikini and high-waisted leggings, poolside, relaxed athletic vacation",
    "photo of a young woman age 19, walking around pool, swim crop top and tight yoga shorts, resort setting, tropical athletic vibes",
]

# Enhanced negative prompt
NEGATIVE_PROMPT = "child, childish, young child, kid, minor, underage, baby face, deformed, distorted, disfigured, bad anatomy, wrong anatomy, extra limbs, extra arms, missing arms, fused fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, ugly, bad proportions, malformed limbs, blurry, low quality, watermark, text, duplicate, clone, baggy clothes, oversized unfitted, loose clothing"

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
