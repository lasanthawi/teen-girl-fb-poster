/**
 * Webhook endpoint to trigger Composio recipe
 * Receives image URL from GitHub Actions and triggers recipe
 */

export default async function handler(req, res) {
  // Only accept POST requests
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  
  try {
    const { image_url, secret } = req.body;
    
    // Validate secret
    if (secret !== process.env.WEBHOOK_SECRET) {
      return res.status(401).json({ error: 'Unauthorized' });
    }
    
    if (!image_url) {
      return res.status(400).json({ error: 'image_url is required' });
    }
    
    console.log(`Received image URL: ${image_url}`);
    
    // Execute Composio recipe
    const composioToken = process.env.COMPOSIO_TOKEN;
    const recipeId = process.env.RECIPE_ID || 'rcp_A9M-wR3IZxUp';
    const pageId = process.env.FACEBOOK_PAGE_ID || '1025914070602506';
    
    const response = await fetch(
      `https://backend.composio.dev/api/v1/rube/recipes/${recipeId}/execute`,
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${composioToken}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          input_data: {
            facebook_page_id: pageId,
            image_url: image_url
          }
        })
      }
    );
    
    const data = await response.json();
    
    console.log(`Recipe response: ${response.status}`, data);
    
    if (response.ok) {
      return res.status(200).json({
        success: true,
        message: 'Post published to Facebook',
        data: data
      });
    } else {
      console.error('Recipe execution failed:', data);
      return res.status(500).json({
        success: false,
        error: 'Recipe execution failed',
        details: data
      });
    }
    
  } catch (error) {
    console.error('Webhook error:', error);
    return res.status(500).json({
      success: false,
      error: error.message
    });
  }
}
