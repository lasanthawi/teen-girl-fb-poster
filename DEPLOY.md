# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod

# After deploy, you'll get a URL like:
# https://teen-girl-fb-webhook.vercel.app

# Add these secrets to GitHub:
# WEBHOOK_URL: https://teen-girl-fb-webhook.vercel.app/api/webhook
# WEBHOOK_SECRET: (generate a random string)

# Add these environment variables to Vercel:
# COMPOSIO_TOKEN
# WEBHOOK_SECRET
# RECIPE_ID
# FACEBOOK_PAGE_ID
