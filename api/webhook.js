// Vercel serverless function - Receives image URL and publishes via Rube recipe
// This bridges GitHub Actions → Rube Recipe (since recipe API isn't public HTTP)

module.exports = async (req, res) => {
  // Only POST
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  
  try {
    const { image_url, secret } = req.body;
    
    console.log('[Webhook] Received request');
    console.log('[Webhook] Image URL:', image_url);
    
    // Validate secret
    if (secret !== process.env.WEBHOOK_SECRET) {
      console.log('[Webhook] Invalid secret');
      return res.status(401).json({ error: 'Unauthorized' });
    }
    
    if (!image_url) {
      console.log('[Webhook] Missing image_url');
      return res.status(400).json({ error: 'image_url is required' });
    }
    
    console.log('[Webhook] Calling Composio action to execute recipe...');
    
    // Use fetch (built-in) instead of SDK
    const composioResponse = await fetch(
      'https://backend.composio.dev/api/v1/actions/RUBE_EXECUTE_RECIPE/execute',
      {
        method: 'POST',
        headers: {
          'X-API-KEY': process.env.COMPOSIO_TOKEN,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          input: {
            recipe_id: process.env.RECIPE_ID || 'rcp_A9M-wR3IZxUp',
            input_data: {
              facebook_page_id: process.env.FACEBOOK_PAGE_ID || '1025914070602506',
              image_url: image_url
            }
          }
        })
      }
    );
    
    const resultText = await composioResponse.text();
    console.log('[Webhook] Composio response status:', composioResponse.status);
    console.log('[Webhook] Composio response:', resultText);
    
    if (!composioResponse.ok) {
      console.error('[Webhook] Recipe execution failed:', resultText);
      return res.status(500).json({
        success: false,
        error: 'Recipe execution failed',
        details: resultText
      });
    }
    
    const result = JSON.parse(resultText);
    const recipeData = result?.data?.data || {};
    
    console.log('[Webhook] Success! Post published');
    console.log('[Webhook] Post ID:', recipeData.post_id);
    
    return res.status(200).json({
      success: true,
      message: 'Post published successfully',
      post_id: recipeData.post_id,
      permalink: recipeData.permalink,
      caption: recipeData.caption
    });
    
  } catch (error) {
    console.error('[Webhook] Error:', error.message);
    console.error('[Webhook] Stack:', error.stack);
    
    return res.status(500).json({
      success: false,
      error: error.message,
      stack: error.stack
    });
  }
};
