const https = require('https');
const http = require('http');

module.exports = async (req, res) => {
  // Only POST
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
    
    console.log('Received image:', image_url);
    
    // Call Composio recipe
    const recipePayload = JSON.stringify({
      facebook_page_id: process.env.FACEBOOK_PAGE_ID || '1025914070602506',
      image_url: image_url
    });
    
    const options = {
      hostname: 'backend.composio.dev',
      path: `/api/v1/rube/recipes/${process.env.RECIPE_ID || 'rcp_A9M-wR3IZxUp'}/execute`,
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${process.env.COMPOSIO_TOKEN}`,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(recipePayload)
      }
    };
    
    const recipeResult = await new Promise((resolve, reject) => {
      const recipeReq = https.request(options, (recipeRes) => {
        let data = '';
        recipeRes.on('data', chunk => data += chunk);
        recipeRes.on('end', () => {
          try {
            resolve({ status: recipeRes.statusCode, data: JSON.parse(data) });
          } catch (e) {
            resolve({ status: recipeRes.statusCode, data: data });
          }
        });
      });
      
      recipeReq.on('error', reject);
      recipeReq.write(recipePayload);
      recipeReq.end();
    });
    
    console.log('Recipe response:', recipeResult.status);
    
    if (recipeResult.status === 200 || recipeResult.status === 201) {
      return res.status(200).json({
        success: true,
        message: 'Post published',
        data: recipeResult.data
      });
    } else {
      console.error('Recipe failed:', recipeResult);
      return res.status(500).json({
        success: false,
        error: 'Recipe execution failed',
        details: recipeResult
      });
    }
    
  } catch (error) {
    console.error('Webhook error:', error);
    return res.status(500).json({
      success: false,
      error: error.message
    });
  }
};
