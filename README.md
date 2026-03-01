# Teen Girl Daily Log - Facebook Auto-Poster (Hybrid)

Automated Facebook posting using **GitHub Actions** for image generation and **Composio Recipe** for publishing.

## 🎯 How It Works

**Hybrid Architecture:**
1. **GitHub Actions** → Generates AI image with your custom Lora model (FAL AI)
2. **Composio Recipe** → Fetches context, generates caption, publishes to Facebook

## ✨ Features

- 🎨 **Custom Lora Images**: Uses your trained model via FAL AI
- 📝 **Context-Aware Captions**: Analyzes previous posts for continuity
- ⏰ **Scheduled**: Runs daily at 7:30 PM Sri Lanka time
- 🚀 **Fully Automated**: Zero manual intervention

## 🛠️ Setup

### Step 1: Add GitHub Secrets

Go to [Settings → Secrets → Actions](https://github.com/lasanthawi/teen-girl-fb-poster/settings/secrets/actions)

Add these **3 secrets**:

| Secret Name | Value | Where to Get |
|------------|-------|-------------|
| `FAL_API_KEY` | Your FAL key | [fal.ai](https://fal.ai/) → Settings → API Keys |
| `LORA_MODEL_URL` | `https://v3b.fal.media/files/b/0a906a2b/-4g_jteoSNzng2aNcWAQT_pytorch_lora_weights.safetensors` | Already provided |
| `COMPOSIO_API_KEY` | Your Composio key | [Get it from Step 2](#step-2-get-composio-api-key) |

**IMPORTANT for FAL_API_KEY:**
- Paste the key WITHOUT pressing Enter
- No extra spaces or newlines
- If you get "Invalid header" error, delete and re-add the secret

---

### Step 2: Get Composio API Key

1. Go to [Rube Dashboard](https://rube.app/)
2. Click on your profile (top right)
3. Go to **Settings** → **API Keys**
4. Click **"Create New API Key"**
5. Copy the key (starts with `rube_...`)
6. Add as `COMPOSIO_API_KEY` secret in GitHub

---

### Step 3: Test the Workflow

1. Go to [Actions Tab](https://github.com/lasanthawi/teen-girl-fb-poster/actions)
2. Click **"Teen Girl Daily Log Auto-Poster"**
3. Click **"Run workflow"** → **"Run workflow"**
4. Wait 2-3 minutes
5. Check the logs:
   - ✅ "Image generated: https://..."
   - ✅ "Recipe executed"
   - ✅ "Post published"
6. Check your [Nethmi G Facebook page](https://www.facebook.com/profile.php?id=61585808243069)

---

## ⏰ Schedule

**Runs automatically once per day:**
- **7:30 PM Sri Lanka Time** (2:00 PM UTC)
- Posts **1 image** with caption

**Change schedule:** Edit `.github/workflows/post.yml` and modify the cron expression

---

## 🔍 How to Monitor

### Check Run History
1. Go to [Actions tab](https://github.com/lasanthawi/teen-girl-fb-poster/actions)
2. See all runs (green = success, red = failed)
3. Click any run to see detailed logs

### What to Look For
- ✅ **Image generation**: Should show FAL API response with image URL
- ✅ **Recipe execution**: Should show Composio recipe result
- ✅ **Post published**: Should show Facebook post ID and permalink

---

## 🐛 Troubleshooting

### "Invalid header value" (FAL_API_KEY)
**Fix:** The key has extra whitespace
1. Delete `FAL_API_KEY` secret
2. Create new secret
3. Paste key carefully (no Enter, no spaces)

### "Facebook 400 Bad Request"
**Issue:** Recipe needs Facebook connection
**Fix:** Make sure your [Composio recipe](https://rube.app/recipe-hub/publish-fb-post-with-image) has Facebook connected

### "Recipe execution failed"
**Check:**
1. Is `COMPOSIO_API_KEY` correct?
2. Is recipe ID correct in `post.py`? (Should be `rcp_A9M-wR3IZxUp`)
3. Does your Composio account have Facebook connected?

### "No images in response"
**Issue:** FAL API error
**Check:**
1. Is `FAL_API_KEY` valid?
2. Is `LORA_MODEL_URL` accessible?
3. Check FAL API status

---

## 📊 Architecture

```
GitHub Actions (every day 7:30 PM SL)
  ↓
1. Generate Image
   - Uses FAL AI API
   - Custom Lora model
   - Random teen girl scene
  ↓
2. Call Composio Recipe (rcp_A9M-wR3IZxUp)
   - Fetch recent FB posts (context)
   - Generate caption with LLM
   - Publish to Facebook
  ↓
3. Done! Post published
```

---

## 📝 Recipe Details

**Recipe Name:** Publish FB Post with Image  
**Recipe ID:** `rcp_A9M-wR3IZxUp`  
**Recipe URL:** [View in Rube](https://rube.app/recipe-hub/publish-fb-post-with-image)

**What it does:**
1. Fetches last 10 posts from Nethmi G page
2. Analyzes context for story continuity
3. Generates teen-voice caption with emojis
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
export FAL_API_KEY="your_fal_key"
export LORA_MODEL_URL="https://v3b.fal.media/files/..."
export COMPOSIO_API_KEY="rube_..."

# Run
python post.py
```

---

## 🎉 Success Criteria

Your setup is working when:
1. ✅ Workflow runs without errors
2. ✅ Image is generated with your Lora model
3. ✅ Caption matches your previous post style
4. ✅ Post appears on Nethmi G Facebook page
5. ✅ Runs automatically every day at 7:30 PM

---

## 📞 Support

If you need help:
1. Check the [Actions logs](https://github.com/lasanthawi/teen-girl-fb-poster/actions) for error details
2. Verify all secrets are added correctly
3. Test the [Composio recipe](https://rube.app/recipe-hub/publish-fb-post-with-image) manually in Rube

---

## License

MIT
