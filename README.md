# Teen Girl FB Auto-Poster - Full Automation with Webhook

**Fully automated Facebook posting: GitHub Actions → Vercel webhook → Facebook Graph API**

## Architecture

```
GitHub Actions (scheduled or manual)
  ↓
1. Generate image with FAL + LoRA (square HD, 35 steps)
  ↓
2. Generate caption (OpenAI if key set, else template)
  ↓
3. POST to Vercel webhook: image_url + caption
  ↓
4. Webhook posts directly to Facebook Page via Graph API (token + page ID from Vercel env)
  ↓
5. ✅ Post live on page
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
   - Go to your Vercel project settings → Environment Variables
   - Add:
     - `WEBHOOK_SECRET`: A random string (e.g. `wh_secret_xxxx`) — **same value** as in GitHub Secrets
     - `FACEBOOK_PAGE_ID`: Your Facebook Page ID (numeric, e.g. `1025914070602506`)
     - `FACEBOOK_ACCESS_TOKEN`: A **Page access token** with `pages_manage_posts` (and optionally `pages_read_engagement`) for that page. Use a long-lived token so it doesn’t expire quickly.

---

### Step 2: Add GitHub Secrets

Go to [GitHub Secrets](https://github.com/lasanthawi/teen-girl-fb-poster/settings/secrets/actions)

Add these secrets:

| Secret Name | Value |
|------------|-------|
| `WEBHOOK_URL` | `https://YOUR-VERCEL-URL.vercel.app/api/webhook` |
| `WEBHOOK_SECRET` | Same value you set in Vercel |
| `FAL_API_KEY` | FAL API key |
| `LORA_MODEL_URL` | Your LoRA model URL |
| `OPENAI_API_KEY` | (Optional) For AI-generated captions; omit to use template captions |

---

### Step 3: Test It

1. Go to [Actions](https://github.com/lasanthawi/teen-girl-fb-poster/actions)
2. Click "Run workflow"
3. Wait ~2-3 minutes
4. Check [Nethmi G Facebook page](https://www.facebook.com/profile.php?id=61585808243069)

---

## ⏰ Schedule

**Runs every 3 hours** (cron: `0 */3 * * *`). You can also trigger manually via **Actions → Run workflow**.

---

## 🎨 Image Settings

- **Lora Scale:** 1.8 (MAXIMUM strength for your trained character)
- **Size:** 512x512 (square)
- **Inference Steps:** 35 (high quality)
- **Guidance Scale:** 2.5 (lets Lora dominate)

---

## 📊 Complete Flow

1. **GitHub Actions** runs (schedule or manual).
2. **Generate image** — FAL (flux-lora + your LoRA) produces an image; URL is saved.
3. **Generate caption** — OpenAI if `OPENAI_API_KEY` is set, otherwise a random template caption.
4. **Publish** — `publish.py` sends `image_url` and `caption` to your Vercel webhook.
5. **Webhook** — Validates secret, then POSTs to Facebook Graph API `/{page-id}/photos` with the image URL and caption using `FACEBOOK_ACCESS_TOKEN` and `FACEBOOK_PAGE_ID` from Vercel env.
6. **Done!** Post is live on your page.

---

## 🔧 Troubleshooting

### Image generation works but webhook fails
- Check `WEBHOOK_URL` and `WEBHOOK_SECRET` match in GitHub and Vercel
- Check Vercel function logs for the exact error

### Facebook post fails (401, 403, or error from Graph API)
- Ensure `FACEBOOK_ACCESS_TOKEN` is a **Page access token** (not a User access token). Get it from [Graph API Explorer](https://developers.facebook.com/tools/explorer/) → select your app → Page → “Get Page Access Token”, or via your app’s login flow.
- Ensure the token has `pages_manage_posts` permission.
- Use a long-lived Page token so it doesn’t expire in 1–2 hours.
- Ensure `FACEBOOK_PAGE_ID` is the numeric Page ID (not the username).

---

## 🔗 Links

- **GitHub Repo:** https://github.com/lasanthawi/teen-girl-fb-poster
- **GitHub Actions:** https://github.com/lasanthawi/teen-girl-fb-poster/actions
- **Facebook Graph API – Page Photos:** https://developers.facebook.com/docs/graph-api/reference/page/photos/

---

## License

MIT
