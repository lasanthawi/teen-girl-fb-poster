# Teen Girl Daily Log - Facebook Auto-Poster (Hybrid)

Automated Facebook posting using **GitHub Actions** for image generation and **Composio Recipe** for publishing.

## 🎯 How It Works

**Hybrid Architecture:**
1. **GitHub Actions** → Generates AI image with your custom Lora model (FAL AI)
2. **Composio Recipe** → Fetches context, generates caption, publishes to Facebook

**Process Flow:**
```
GitHub Actions
  ↓
1. Send prompt + Lora URL to FAL API
  ↓
2. FAL generates image → returns URL
  ↓
3. Call Composio recipe with image URL
  ↓
4. Recipe: fetch context → generate caption → publish to FB
  ↓
5. Done! Post live on Nethmi G page
```

## ✨ Features

- 🎨 **Custom Lora Images**: Uses your trained model via FAL AI
- 📝 **Context-Aware Captions**: Analyzes previous posts for continuity
- ⏰ **Scheduled**: Runs daily at 7:30 PM Sri Lanka time
- 🚀 **Fully Automated**: Zero manual intervention

## 🛠️ Setup

### Step 1: Fix FAL_API_KEY Secret

**This is CRITICAL - the secret must have NO extra whitespace!**

1. Go to [GitHub Secrets](https://github.com/lasanthawi/teen-girl-fb-poster/settings/secrets/actions)
2. **Delete** the existing `FAL_API_KEY` (if exists)
3. Click **"New repository secret"**
4. Name: `FAL_API_KEY`
5. Value: Paste your FAL key
6. **IMPORTANT:** Do NOT press Enter after pasting
7. Just click "Add secret"

---

### Step 2: Add COMPOSIO_TOKEN Secret

1. **Get your Composio token:**
   - Go to [Rube Settings](https://rube.app/settings)
   - You should see a JWT token (starts with `eyJ...`)
   - Copy the entire token

2. **Add to GitHub:**
   - Go to [GitHub Secrets](https://github.com/lasanthawi/teen-girl-fb-poster/settings/secrets/actions)
   - Click **"New repository secret"**
   - Name: `COMPOSIO_TOKEN`
   - Value: Paste your JWT token
   - Click "Add secret"

---

### Step 3: LORA_MODEL_URL (Already Set)

The secret should already be there:
```
https://v3b.fal.media/files/b/0a906a2b/-4g_jteoSNzng2aNcWAQT_pytorch_lora_weights.safetensors
```

If not, add it as a secret ✅

---

### Step 4: Test Run

1. Go to [Actions Tab](https://github.com/lasanthawi/teen-girl-fb-poster/actions)
2. Click **"Teen Girl Daily Log Auto-Poster"**
3. Click **"Run workflow"** → **"Run workflow"**
4. Wait 2-3 minutes and watch the logs

**Expected Output:**
```
✓ Image generated successfully!
  Image URL: https://fal.media/files/...
✓ Recipe executed successfully!
✓ SUCCESS! Post published to Facebook
```

5. Check [Nethmi G Facebook page](https://www.facebook.com/profile.php?id=61585808243069)

---

## ⏰ Schedule

**Runs automatically once per day:**
- **7:30 PM Sri Lanka Time** (2:00 PM UTC)
- Posts **1 image** with caption to Nethmi G page

**Change schedule:** Edit `.github/workflows/post.yml` and modify the cron expression

---

## 🔍 Monitoring

### Check Run History
1. Go to [Actions tab](https://github.com/lasanthawi/teen-girl-fb-poster/actions)
2. See all runs (green ✅ = success, red ❌ = failed)
3. Click any run to see detailed logs

### What to Look For in Logs
- ✅ **STEP 1**: "Image generated successfully!"
- ✅ **STEP 2**: "Recipe executed successfully!"
- ✅ **Final**: "SUCCESS! Post published to Facebook"

---

## 🐛 Troubleshooting

### "Invalid header value" (FAL_API_KEY)
**Cause:** Extra whitespace/newline in the secret

**Fix:**
1. Delete `FAL_API_KEY` secret
2. Create new one
3. Paste key WITHOUT pressing Enter
4. Just click "Add secret"

---

### "401 Unauthorized" (Composio)
**Cause:** COMPOSIO_TOKEN is invalid or expired

**Fix:**
1. Go to [Rube Settings](https://rube.app/settings)
2. Copy the JWT token
3. Update `COMPOSIO_TOKEN` secret in GitHub

---

### "Recipe execution failed"
**Check:**
1. Is Facebook connected in your [Composio recipe](https://rube.app/recipe-hub/publish-fb-post-with-image)?
2. Is the recipe ID correct? (Should be `rcp_A9M-wR3IZxUp`)
3. Check recipe logs in Rube dashboard

---

### "No images in response" (FAL)
**Check:**
1. Is `FAL_API_KEY` valid and active?
2. Is `LORA_MODEL_URL` accessible?
3. Does your FAL account have credits?
4. Check [FAL API status](https://status.fal.ai/)

---

## 📊 Architecture Diagram

```
┌─────────────────────────────────────────┐
│   GitHub Actions (Scheduled Daily)      │
│   Runs at 7:30 PM SL Time               │
└─────────────────┬───────────────────────┘
                  │
                  ▼
         ┌────────────────┐
         │  Generate      │
         │  Random Prompt │
         └────────┬───────┘
                  │
                  ▼
    ┌─────────────────────────────┐
    │  FAL AI API                 │
    │  POST /fal-ai/flux-2/lora   │
    │  + Prompt                   │
    │  + Lora URL (trained model) │
    └─────────────┬───────────────┘
                  │
                  ▼
         ┌────────────────┐
         │  Image URL     │
         │  Returned      │
         └────────┬───────┘
                  │
                  ▼
    ┌─────────────────────────────┐
    │  Composio Recipe API        │
    │  POST /recipe/run           │
    │  Recipe: rcp_A9M-wR3IZxUp   │
    │  Params: { image_url, ... } │
    └─────────────┬───────────────┘
                  │
                  ▼
    ┌─────────────────────────────┐
    │  Recipe Execution:          │
    │  1. Fetch FB posts (context)│
    │  2. Generate caption (LLM)  │
    │  3. Publish to FB page      │
    └─────────────┬───────────────┘
                  │
                  ▼
         ┌────────────────┐
         │  Post Live!    │
         │  Nethmi G Page │
         └────────────────┘
```

---

## 📝 Recipe Details

**Recipe Name:** Publish FB Post with Image  
**Recipe ID:** `rcp_A9M-wR3IZxUp`  
**Recipe URL:** [View in Rube](https://rube.app/recipe-hub/publish-fb-post-with-image)

**What it does:**
1. Fetches last 10 posts from Nethmi G page (for context)
2. Analyzes context to maintain story continuity
3. Generates teen-voice caption with emojis using LLM
4. Publishes image + caption to Facebook

---

## 🔧 Local Testing

```bash
# Clone repo
git clone https://github.com/lasanthawi/teen-girl-fb-poster.git
cd teen-girl-fb-poster

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export FAL_API_KEY="your_fal_key_here"
export LORA_MODEL_URL="https://v3b.fal.media/files/b/0a906a2b/-4g_jteoSNzng2aNcWAQT_pytorch_lora_weights.safetensors"
export COMPOSIO_TOKEN="eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQi..."

# Run
python post.py
```

---

## 🎉 Success Criteria

Your setup is working when:
1. ✅ Workflow runs without errors
2. ✅ Image generated with your custom Lora model
3. ✅ Caption matches your page's teen girl voice
4. ✅ Post appears on Nethmi G Facebook page
5. ✅ Runs automatically every day at 7:30 PM SL time

---

## 🔗 Important Links

- **GitHub Repo:** https://github.com/lasanthawi/teen-girl-fb-poster
- **Composio Recipe:** https://rube.app/recipe-hub/publish-fb-post-with-image
- **GitHub Secrets:** https://github.com/lasanthawi/teen-girl-fb-poster/settings/secrets/actions
- **GitHub Actions:** https://github.com/lasanthawi/teen-girl-fb-poster/actions
- **Nethmi G Page:** https://www.facebook.com/profile.php?id=61585808243069

---

## 💬 Support

If you need help:
1. Check [Actions logs](https://github.com/lasanthawi/teen-girl-fb-poster/actions) for detailed error messages
2. Verify all 3 secrets are correctly added
3. Test the [Composio recipe](https://rube.app/recipe-hub/publish-fb-post-with-image) manually in Rube
4. Check FAL account has credits

---

## 📄 License

MIT
