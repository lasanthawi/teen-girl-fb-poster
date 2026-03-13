import os
import sys
import random
import requests
import time
import json
from datetime import datetime

def log(msg):
    print(f"[{datetime.utcnow().isoformat()}] {msg}")

# COLORFUL ATHLETIC WEAR with outdoor locations
PROMPTS = [
    # WHITE & LIGHT COLORS
    "photo of a young woman age 19, sitting on park bench, white sports bra and pink yoga pants, park with trees, sunny day, fitness vibe",
    "photo of a young woman age 18, walking on path, white crop top and purple leggings, city park, athletic outdoor look",
    "photo of a teen woman age 20, stretching on grass, light blue tank and white yoga leggings, park picnic area, workout aesthetic",
    "photo of a young woman age 19, standing by tree, white sports bra and mint green gym leggings, botanical garden, fresh active wear",
    
    # PINK & PURPLE SHADES
    "photo of a young woman age 18, standing on beach, pink sports bra and purple tight shorts, beach sunset, summer fitness vibe",
    "photo of a teen woman age 20, sitting on beach towel, hot pink crop top and white bike shorts, beach, sporty beach look",
    "photo of a young woman age 19, walking on boardwalk, lavender tank top and pink tight shorts, beach pier, colorful style",
    "photo of a young woman age 18, sitting on rocks, magenta fitted top and gray bike shorts, rocky beach, vibrant athleisure",
    
    # BLUE & TEAL VARIATIONS
    "photo of a teen woman age 20, sitting at cafe table, sky blue crop top and navy leggings, outdoor cafe, cool athletic style",
    "photo of a young woman age 19, standing with coffee cup, teal sports bra and black yoga pants, cafe patio, fitness casual",
    "photo of a young woman age 18, sitting by window, royal blue fitted tee and white leggings, cozy cafe interior, fresh look",
    "photo of a teen woman age 20, leaning on counter, turquoise crop top and gray tight leggings, modern cafe, oceanic vibe",
    
    # RED & ORANGE TONES  
    "photo of a young woman age 19, standing in gym, red sports bra and black compression shorts, gym mirror background, bold workout",
    "photo of a young woman age 18, sitting on gym bench, coral crop top and white leggings, fitness center, energetic hot vibe",
    "photo of a teen woman age 20, stretching pose, orange sports bra and gray yoga pants, gym studio, vibrant flexibility",
    "photo of a young woman age 19, holding water bottle, burgundy compression top and black shorts, fitness center, intense look",
    
    # NEON & BRIGHT COLORS
    "photo of a young woman age 18, walking on sidewalk, neon yellow sports bra and black tight shorts, city street, bold athletic",
    "photo of a teen woman age 20, standing by graffiti wall, lime green crop tank and purple leggings, downtown alley, electric fitness",
    "photo of a young woman age 19, sitting on steps, hot pink sports top and white bike shorts, city entrance, vibrant sporty",
    "photo of a young woman age 18, leaning on railing, neon orange crop hoodie and black yoga pants, urban bridge, standout style",
    
    # PATTERNED & COLORFUL PRINTS
    "photo of a teen woman age 20, standing in store, tie-dye sports bra and patterned yoga leggings, boutique shop, fun gym wear",
    "photo of a young woman age 19, trying on clothes, floral fitted tank and colorful leggings, store mirror, playful athletic",
    "photo of a young woman age 18, walking with bags, striped crop top and pink bike shorts, mall corridor, trendy athletic day",
    "photo of a teen woman age 20, sitting in store, geometric print sports dress and white leggings, boutique area, artistic sporty",
    
    # PASTEL COMBINATIONS
    "photo of a young woman age 19, sitting at desk, pastel pink crop sweater and baby blue yoga pants, library study, soft athletic",
    "photo of a young woman age 18, standing by bookshelf, peach fitted tee and lavender leggings, library interior, gentle study wear",
    "photo of a teen woman age 20, reading at table, mint sports crop top and white bike shorts, study lounge, fresh focused vibe",
    "photo of a young woman age 19, walking between shelves, lilac tank top and cream leggings, modern library, dreamy studious",
    
    # TWO-TONE COMBINATIONS
    "photo of a young woman age 18, standing on rooftop, black and white sports bra and pink tight shorts, city skyline, classic contrast",
    "photo of a teen woman age 20, sitting on balcony, red and white crop top and black yoga pants, apartment balcony, bold sunset",
    "photo of a young woman age 19, leaning on edge, blue and yellow fitted tank and gray leggings, rooftop terrace, sporty evening",
    "photo of a young woman age 18, stretching with view, purple and pink sports bra and white bike shorts, city balcony, gradient fit",
    
    # GREEN & EARTH TONES
    "photo of a teen woman age 20, sitting at restaurant, olive green crop top and beige tight jeans, trendy restaurant, natural casual",
    "photo of a young woman age 19, standing by bar, forest green fitted tank and black leggings, restaurant interior, earthy athletic",
    "photo of a young woman age 18, sitting in booth, sage sports crop top and white tight shorts, diner setting, fresh sporty meal",
    "photo of a teen woman age 20, at outdoor dining, emerald fitted top and tan bike shorts, patio restaurant, nature-inspired brunch",
    
    # METALLIC & SHIMMER
    "photo of a young woman age 19, sitting poolside, silver sports bikini and white athletic shorts, hotel pool, luxe vacation workout",
    "photo of a young woman age 18, standing by pool, rose gold crop swimsuit and pink bike shorts, resort pool, glamorous summer",
    "photo of a teen woman age 20, lying on lounge chair, bronze sports bikini and champagne leggings, poolside, shimmery vacation",
    "photo of a young woman age 19, walking around pool, gold swim crop top and white yoga shorts, resort setting, radiant tropical",
]

# Enhanced negative prompt with "black only, monochrome"
NEGATIVE_PROMPT = "child, childish, young child, kid, minor, underage, baby face, deformed, distorted, disfigured, bad anatomy, wrong anatomy, extra limbs, extra arms, missing arms, fused fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, ugly, bad proportions, malformed limbs, blurry, low quality, watermark, text, duplicate, clone, baggy clothes, oversized unfitted, loose clothing, all black outfit, monochrome clothing"

log("Generating HIGH RESOLUTION colorful athletic wear image (Square HD 1024x1024, 35 steps)...")
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
