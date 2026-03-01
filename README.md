# Teen Girl FB Auto-Poster - Full Automation with Webhook

**Fully automated Facebook posting using GitHub + Vercel + Composio**

##  Architecture

```
GitHub Actions (Scheduled 2x daily)
  ↓
1. Generate image with FAL + Lora (scale 1.8, square)
  ↓
2. POST to Vercel Webhook with image URL
  ↓
3. Webhook triggers Composio Recipe
  ↓
4. Recipe: Fetch context → Generate caption → Post to FB
  ↓
5. ✅ Post live on Nethmi G page
```

---

## 🚀 Setup Instructions

### Step 1: Deploy Webhook to Vercel

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel:**
   ```bash
   vercel login
   ```

3. **Navigate to your repo:**
   ```bash
   git clone https://github.com/lasanthawi/teen-girl-fb-poster.git
   cd teen-girl-fb-poster
   ```

4. **Deploy to Vercel:**
   ```bash
   vercel --prod
   ```
   
   You'll get a URL like: `https://teen-girl-fb-webhook-xxx.vercel.app`

5. **Add Environment Variables in Vercel Dashboard:**
   - Go to your Vercel project settings
   - Add these environment variables:
     - `COMPOSIO_TOKEN`: Your JWT token (eyJhbGciOiJIUzI1NiJ9...)
     - `WEBHOOK_SECRET`: Generate a random string (e.g., `wh_secret_12345abc`)
     - `RECIPE_ID`: `rcp_A9M-wR3IZxUp`
     - `FACEBOOK_PAGE_ID`: `1025914070602506`

---

### Step 2: Add GitHub Secrets

Go to [GitHub Secrets](https://github.com/lasanthawi/teen-girl-fb-poster/settings/secrets/actions)

Add these 2 NEW secrets:

| Secret Name | Value |
|------------|-------|
| `WEBHOOK_URL` | `https://YOUR-VERCEL-URL.vercel.app/api/webhook` |
| `WEBHOOK_SECRET` | Same value you used in Vercel |

**Existing secrets** (should already be there):
- ✅ `FAL_API_KEY`
- ✅ `LORA_MODEL_URL`
- ✅ `COMPOSIO_TOKEN`

---

### Step 3: Test It

1. Go to [Actions](https://github.com/lasanthawi/teen-girl-fb-poster/actions)
2. Click "Run workflow"
3. Wait ~2-3 minutes
4. Check [Nethmi G Facebook page](https://www.facebook.com/profile.php?id=61585808243069)

---

## ⏰ Automatic Schedule

**Runs automatically 2x daily:**
- **2:30 PM Sri Lanka Time** (9:00 AM UTC)
- **7:30 PM Sri Lanka Time** (2:00 PM UTC)

---

## 🎨 Image Settings

- **Lora Scale:** 1.8 (MAXIMUM strength for your trained character)
- **Size:** 512x512 (square)
- **Inference Steps:** 35 (high quality)
- **Guidance Scale:** 2.5 (lets Lora dominate)

---

## 📊 Complete Flow

1. **GitHub Actions triggers** (scheduled)
2. **FAL generates** square image with Lora 1.8
3. **GitHub calls** Vercel webhook with image URL
4. **Webhook triggers** Composio recipe
5. **Recipe:**
   - Fetches recent posts for context
   - Generates teen-voice caption with LLM
   - Posts to Nethmi G Facebook page
6. **Done!** Post is live

---

## 🔧 Troubleshooting

### Image generation works but webhook fails
- Check `WEBHOOK_URL` and `WEBHOOK_SECRET` match in GitHub and Vercel
- Check Vercel logs for errors

### Recipe execution fails
- Check `COMPOSIO_TOKEN` is valid in Vercel
- Verify Facebook connection is active in Composio

---

## 🔗 Links

- **GitHub Repo:** https://github.com/lasanthawi/teen-girl-fb-poster
- **GitHub Actions:** https://github.com/lasanthawi/teen-girl-fb-poster/actions
- **Composio Recipe:** https://rube.app/recipe-hub/publish-fb-post-with-image
- **Nethmi G Page:** https://www.facebook.com/profile.php?id=61585808243069

---

## License

MIT
