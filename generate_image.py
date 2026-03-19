import os
import sys
import random
import requests
import time
import json
from datetime import datetime

def log(msg):
    print(f"[{datetime.utcnow().isoformat()}] {msg}")

# COLORFUL TIGHT ATHLETIC WEAR in OUTDOOR LOCATIONS
PROMPTS = [
    # Colorful yoga pants & leggings - outdoor
    "photo of a young woman age 19, sitting on park bench, white sports bra and bright pink yoga pants, park with trees, sunny day, fitness vibe",
    "photo of a young woman age 18, walking on path, purple crop top and teal high-waisted leggings, city park, colorful athletic look",
    "photo of a teen woman age 20, stretching on grass, yellow fitted tank and blue yoga leggings, park picnic area, vibrant workout aesthetic",
    "photo of a young woman age 19, standing by tree, coral sports bra and grey tight gym leggings, botanical garden, active wear style",
    
    # Bright colored tight shorts - beach/outdoor
    "photo of a young woman age 18, standing on beach, red sports bra and white tight athletic shorts, beach sunset, summer fitness vibe",
    "photo of a teen woman age 20, sitting on beach towel, orange bikini top and green spandex bike shorts, beach, sporty beach look",
    "photo of a young woman age 19, walking on boardwalk, pink tank top and light blue tight denim shorts, beach pier, casual hot style",
    "photo of a young woman age 18, sitting on rocks, lavender fitted top and navy bike shorts, rocky beach, athleisure aesthetic",
    
    # Patterned & colorful leggings - cafe/urban
    "photo of a teen woman age 20, sitting at cafe table, beige crop sweater and geometric print leggings, outdoor cafe, cozy athletic style",
    "photo of a young woman age 19, standing with coffee cup, mint green sports bra and burgundy yoga pants, cafe patio, fitness casual",
    "photo of a young woman age 18, sitting by window, grey fitted tee and floral printed leggings, cozy cafe interior, athleisure chic",
    "photo of a teen woman age 20, leaning on counter, sky blue crop top and charcoal tight leggings, modern cafe, trendy athletic look",
    
    # Vibrant gym wear - multi-colored
    "photo of a young woman age 19, standing in gym, neon yellow sports bra and purple compression shorts, gym mirror background, workout ready",
    "photo of a young woman age 18, sitting on gym bench, hot pink crop sports top and white skin-tight leggings, fitness center, athletic hot vibe",
    "photo of a teen woman age 20, stretching pose, turquoise sports bra and coral tight yoga pants, gym studio, active flexibility",
    "photo of a young woman age 19, holding water bottle, lime green compression top and black spandex shorts, fitness center, post-workout look",
    
    # Colorful athletic wear - city streets
    "photo of a young woman age 18, walking on sidewalk, orange sports bra and blue high-waisted tight shorts, city street, urban athletic style",
    "photo of a teen woman age 20, standing by graffiti wall, red crop tank and grey skin-tight leggings, downtown alley, streetwear fitness",
    "photo of a young woman age 19, sitting on steps, white fitted sports top and maroon bike shorts, city building entrance, sporty urban",
    "photo of a young woman age 18, leaning on railing, pink crop hoodie and olive tight yoga pants, urban bridge, street athleisure",
    
    # Bright colored bottoms - shopping
    "photo of a teen woman age 20, standing in store, black sports bra and rainbow ombre yoga leggings, boutique shop, shopping in gym wear",
    "photo of a young woman age 19, trying on clothes, peach fitted tank and emerald tight leggings, clothing store mirror, athletic shopping",
    "photo of a young woman age 18, walking with bags, yellow crop top and purple spandex bike shorts, mall corridor, casual athletic day",
    "photo of a teen woman age 20, sitting in store, rose gold bodycon sports dress and nude leggings, boutique fitting area, sporty trying on",
    
    # Multi-colored athletic wear - library/study
    "photo of a young woman age 19, sitting at desk, sage green crop sweater and camel tight yoga pants, library study area, comfy study athletic",
    "photo of a young woman age 18, standing by bookshelf, white fitted tee and pastel rainbow leggings, library interior, casual study wear",
    "photo of a teen woman age 20, reading at table, baby blue sports crop top and tan bike shorts, study lounge, focused athletic vibe",
    "photo of a young woman age 19, walking between shelves, lavender tank top and wine red high-waisted leggings, modern library, studious athletic",
    
    # Sunset colored athletic wear - rooftop/balcony
    "photo of a young woman age 18, standing on rooftop, peach sports bra and dusty rose tight shorts, city skyline background, golden hour workout",
    "photo of a teen woman age 20, sitting on balcony railing, cream crop top and terracotta skin-tight yoga pants, apartment balcony, sunset athletic",
    "photo of a young woman age 19, leaning on edge, aqua fitted tank and lilac compression leggings, rooftop terrace, evening workout vibe",
    "photo of a young woman age 18, stretching with view, fuchsia sports bra and silver tight bike shorts, balcony overlooking city, fitness aesthetic",
    
    # Pastel & bright tight bottoms - restaurant/dining
    "photo of a teen woman age 20, sitting at restaurant table, powder blue crop top and white high-waisted tight jeans, trendy restaurant, casual dinner date",
    "photo of a young woman age 19, standing by bar, mint fitted tank and blush pink skin-tight leggings, restaurant interior, athletic dining out",
    "photo of a young woman age 18, sitting in booth, lemon sports crop top and sky blue tight shorts, diner setting, sporty casual meal",
    "photo of a teen woman age 20, at outdoor dining, coral fitted top and sage spandex bike shorts, patio restaurant, athletic brunch style",
    
    # Tropical colored swimwear & athletic wear - pool/resort
    "photo of a young woman age 19, sitting poolside, tropical print sports bikini and orange tight athletic shorts, hotel pool area, vacation workout mode",
    "photo of a young woman age 18, standing by pool, turquoise crop swimsuit top and white spandex bike shorts, resort pool, athletic summer getaway",
    "photo of a teen woman age 20, lying on lounge chair, hot pink sports bikini and neon green high-waisted leggings, poolside, relaxed athletic vacation",
    "photo of a young woman age 19, walking around pool, yellow swim crop top and aqua tight yoga shorts, resort setting, tropical athletic vibes",
]

# Enhanced negative prompt
NEGATIVE_PROMPT = "child, childish, young child, kid, minor, underage, baby face, deformed, distorted, disfigured, bad anatomy, wrong anatomy, extra limbs, extra arms, missing arms, fused fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, ugly, bad proportions, malformed limbs, blurry, low quality, watermark, text, duplicate, clone, baggy clothes, oversized unfitted, loose clothing, all black outfit, dark colors only"

log("Generating HIGH RESOLUTION stylish image with FAL (Square HD 1024x1024, 35 steps)...")
prompt = random.choice(PROMPTS)
log(f"Prompt: {prompt}")
log(f"RUBE_IMAGE_PROMPT_START:{prompt}:RUBE_IMAGE_PROMPT_END")  # Special marker for recipe
log(f"Negative prompt: {NEGATIVE_PROMPT[:100]}...")

# Save prompt for caption generator (scene-specific captions)
with open("image_prompt.txt", "w", encoding="utf-8") as f:
    f.write(prompt)

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
