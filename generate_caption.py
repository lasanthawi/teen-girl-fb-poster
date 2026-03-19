"""
Generate a rich, catchy caption that matches the generated image.
Uses the image prompt (exact scene description) so the caption is relevant.
OpenAI: scene-specific, longer caption with many hashtags; else themed templates.
"""
import os
import sys
import random
from datetime import datetime

def log(msg):
    print(f"[{datetime.utcnow().isoformat()}] {msg}")

# Longer themed fallbacks with many hashtags (keyword -> caption)
TEMPLATE_BY_THEME = [
    ("library", "Study mode on — finding my next read between the shelves. 📚✨ #LibraryVibes #Studious #CozyReads #OOTD #StudyGram #BookLover #Aesthetic #CampusLife"),
    ("study", "Grinding with good vibes only. This is the energy. 📖💜 #StudyGram #CampusLife #Aesthetic #Studious #OOTD #CozyVibes #DailyVibes"),
    ("park", "Outdoor therapy hits different. Sunshine and good energy. 🌳☀️ #ParkLife #NatureVibes #FitLife #SunnyDay #OutdoorVibes #GoodVibes #OOTD #ActiveWear"),
    ("beach", "Salt in the air, sand in my hair. Living for summer days. 🏖️🌊 #BeachDay #SummerVibes #GoodLife #BeachVibes #Sunset #OOTD #VacationMode"),
    ("graffiti", "Street art and good vibes. Urban exploration mode. 🎨✨ #StreetStyle #Graffiti #UrbanLife #CityVibes #OOTD #StreetFashion #UrbanExplorer #GoodEnergy"),
    ("alley", "Finding the best spots in the city. Alley vibes. 🏙️👟 #StreetStyle #UrbanLife #CityGirl #OOTD #DailyVibes #UrbanExplorer #StreetFashion"),
    ("cafe", "Coffee and confidence. Best combo. ☕✨ #CafeHopping #LatteArt #CozyVibes #CoffeeLover #OOTD #CafeVibes #GoodVibes"),
    ("gym", "No pain no gain. Showing up for myself. 💪🔥 #GymLife #WorkoutMode #FitnessGirl #FitLife #GymMotivation #OOTD #ActiveWear"),
    ("rooftop", "Views and vibes. Nothing beats this. 🌆✨ #RooftopSeason #CityLights #GoldenHour #UrbanLife #OOTD #CityVibes #GoodEnergy"),
    ("balcony", "Living for these moments. Sunset hits different. 🌅 #BalconyLife #SunsetChill #GoodEnergy #GoldenHour #OOTD #DailyVibes #CozyVibes"),
    ("pool", "Poolside mood only. Summer state of mind. 🏊‍♀️☀️ #PoolDay #SummerGoals #VacationMode #PoolVibes #SummerVibes #OOTD #GoodLife"),
    ("restaurant", "Good food, better company. Date night vibes. 🍽️💕 #Foodie #DateNight #Vibes #GoodFood #OOTD #RestaurantVibes #GoodLife"),
    ("store", "Retail therapy done right. New fits, new me. 🛍️✨ #ShoppingDay #OOTD #Fashion #ShoppingVibes #RetailTherapy #Style #GoodVibes"),
    ("street", "City girl energy. This is the vibe. 🏙️👟 #StreetStyle #UrbanLife #DailyVibes #CityGirl #OOTD #StreetFashion #UrbanExplorer #GoodEnergy"),
    ("sidewalk", "Walking through the city with good energy. 🏙️✨ #StreetStyle #UrbanLife #CityVibes #OOTD #DailyVibes #StreetFashion"),
    ("boardwalk", "Beach boardwalk vibes. Sun, sand, and good times. 🏖️☀️ #Boardwalk #BeachDay #SummerVibes #OOTD #GoodLife #BeachVibes"),
    ("steps", "Found the perfect spot. City steps and good vibes. 📸✨ #StreetStyle #UrbanLife #OOTD #CityVibes #DailyVibes #GoodEnergy"),
]
DEFAULT_TEMPLATE = "Living my best life rn. Good vibes only. ✨💫 #GoodVibes #OOTD #Lifestyle #DailyVibes #Aesthetic #GoodEnergy #Vibes"

def get_image_prompt():
    """Read scene description from generate_image.py output."""
    path = "image_prompt.txt"
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""

def pick_template_caption(image_prompt):
    """Pick a themed template based on image prompt keywords (order matters: more specific first)."""
    prompt_lower = (image_prompt or "").lower()
    for kw, cap in TEMPLATE_BY_THEME:
        if kw in prompt_lower:
            return cap
    return DEFAULT_TEMPLATE

def generate_with_openai(image_prompt):
    """Generate a longer, scene-specific caption. Only describe what is in the scene."""
    try:
        from openai import OpenAI
    except ImportError:
        return None
    api_key = (os.environ.get("OPENAI_API_KEY") or "").strip()
    if not api_key:
        return None
    client = OpenAI(api_key=api_key)
    scene = (image_prompt or "").strip()
    if not scene:
        scene = "casual lifestyle or outfit photo"
    try:
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You write Instagram-style captions for a teen/lifestyle photo. "
                        "CRITICAL: The user will give you the EXACT scene in the image (location, outfit, activity). "
                        "Your caption MUST describe ONLY what is in that scene. "
                        "Do NOT mention coffee, latte, or cafe unless the scene explicitly says cafe, coffee shop, or coffee. "
                        "Do NOT mention beach or pool unless the scene says beach, pool, or similar. "
                        "Match the location (e.g. graffiti wall = street/urban, library = study/books), the outfit, and the vibe. "
                        "Format: 2-3 short sentences (or 1 longer vivid sentence) that fit the scene, then a line break or space, then 5-8 relevant hashtags. "
                        "Use 3-5 emojis that match the scene (e.g. 🎨 for graffiti, 📚 for library, ☀️ for outdoor). "
                        "Output ONLY the caption, no quotes, no 'Caption:' prefix."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Exact scene in the image:\n{scene}\n\n"
                        "Write a caption that describes ONLY this scene. 2-3 sentences, then 5-8 hashtags. Use emojis that match the location and outfit. "
                        "Do not add anything that is not in the scene (e.g. no coffee if it's not a cafe scene)."
                    ),
                },
            ],
            max_tokens=220,
        )
        text = (r.choices[0].message.content or "").strip()
        text = text.strip().strip('"\'')
        if text.startswith("Caption:"):
            text = text[8:].strip()
        return text if text else None
    except Exception as e:
        log(f"OpenAI caption failed: {e}")
        return None

def main():
    log("Generating caption...")
    image_prompt = get_image_prompt()
    if image_prompt:
        log(f"Image scene: {image_prompt[:100]}...")
    caption = generate_with_openai(image_prompt)
    if not caption:
        caption = pick_template_caption(image_prompt)
        log("Using themed template caption (set OPENAI_API_KEY for AI captions)")
    else:
        log("Using OpenAI-generated caption")
    log(f"Caption: {caption}")
    with open("caption.txt", "w", encoding="utf-8") as f:
        f.write(caption)
    log("✓ Caption saved to caption.txt")
    sys.exit(0)

if __name__ == "__main__":
    main()
