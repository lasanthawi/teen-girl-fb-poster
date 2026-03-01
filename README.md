# Teen Girl Daily Log - Facebook Auto-Poster

Automated Facebook posting system that generates AI images using custom Lora models and posts to your Facebook page.

## Features

- 🎨 **Custom AI Images**: Uses your trained Lora model via FAL AI
- 📝 **Context-Aware Captions**: Analyzes previous posts for story continuity
- ⏰ **Scheduled Posting**: Runs 3x daily via GitHub Actions
- 🚀 **Fully Automated**: Zero manual intervention required

## Setup

### 1. Configure Secrets

Go to Settings → Secrets and variables → Actions → New repository secret

Add these secrets:

| Secret Name | Value | Description |
|------------|-------|-------------|
| `FACEBOOK_PAGE_ID` | `1025914070602506` | Your Facebook Page ID |
| `FACEBOOK_ACCESS_TOKEN` | `your_token_here` | Facebook Page Access Token |
| `FAL_API_KEY` | `your_key_here` | FAL AI API Key |
| `LORA_MODEL_URL` | `https://v3b.fal.media/files/...` | Your Lora model URL |
| `OPENAI_API_KEY` | `sk-...` | OpenAI API key for prompt generation |
| `POSTS_TO_GENERATE` | `1` | Number of posts per run (optional, default: 1) |

### 2. Get Facebook Access Token

1. Go to [Facebook Graph API Explorer](https://developers.facebook.com/tools/explorer/)
2. Select your app (or create one)
3. Add permissions: `pages_manage_posts`, `pages_read_engagement`
4. Generate Token
5. **Important**: Get a **long-lived token** (lasts 60 days)

### 3. Get OpenAI API Key

1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Create new secret key
3. Copy and save it

### 4. Enable & Test

1. Go to Actions tab
2. Click "I understand my workflows, go ahead and enable them"
3. Run workflow manually to test

## Schedule

Runs automatically 3 times per day:
- **9 AM UTC** (2:30 PM Sri Lanka Time)
- **2 PM UTC** (7:30 PM Sri Lanka Time)
- **7 PM UTC** (12:30 AM Sri Lanka Time next day)

Edit `.github/workflows/post.yml` to change schedule.

## Monitoring

- Check Actions tab for run history and logs
- Each run shows published posts
- Failed runs show error details

## Troubleshooting

### "Missing required environment variables"
Make sure all secrets are added in repo settings

### "Image generation failed"
- Check FAL API key is valid
- Verify Lora model URL is accessible

### "Facebook API error"
- Token may have expired (get new long-lived token)
- Check page ID is correct
- Verify page permissions

## License

MIT
