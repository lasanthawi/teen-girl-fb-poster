// Vercel serverless function to handle webhook and trigger Facebook post
// This is called by GitHub Actions after image generation

module.exports = async (req, res) => {
  // Only accept POST requests
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  
  try {
    const { image_url, secret } = req.body;
    
    // Validate secret
    if (secret !== process.env.WEBHOOK_SECRET) {
      return res.status(401).json({ error: 'Unauthorized - invalid secret' });
    }
    
    if (!image_url) {
      return res.status(400).json({ error: 'image_url is required' });
    }
    
    console.log('[Webhook] Received image:', image_url);
    console.log('[Webhook] Calling Rube recipe directly...');
    
    // Instead of calling the HTTP API endpoint (which doesn't work),
    // we'll call the recipe execution endpoint that Rube uses internally
    const axios = require('axios');
    
    const recipeResponse = await axios.post(
      `https://backend.composio.dev/api/v1/actions/RUBE_EXECUTE_RECIPE/execute`,
      {
        input: {
          recipe_id: process.env.RECIPE_ID || 'rcp_A9M-wR3IZxUp',
          input_data: {
            facebook_page_id: process.env.FACEBOOK_PAGE_ID || '1025914070602506',
            image_url: image_url
          }
        }
      },
      {
        headers: {
          'X-API-KEY': process.env.COMPOSIO_TOKEN,
          'Content-Type': 'application/json'
        },
        timeout: 120000 // 2 minutes
      }
    );
    
    console.log('[Webhook] Recipe execution completed');
    
    const result = recipeResponse.data?.data || recipeResponse.data;
    
    return res.status(200).json({
      success: true,
      message: 'Post published successfully',
      post_id: result.post_id,
      permalink: result.permalink,
      caption: result.caption
    });
    
  } catch (error) {
    console.error('[Webhook] Error:', error.message);
    console.error('[Webhook] Response:', error.response?.data);
    
    return res.status(500).json({
      success: false,
      error: error.message,
      details: error.response?.data
    });
  }
};
