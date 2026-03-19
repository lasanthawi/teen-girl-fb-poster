// Vercel serverless function - Publishes image + caption directly to Facebook Page via Graph API

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { image_url, caption, secret } = req.body;

    console.log('[Webhook] Received request');
    console.log('[Webhook] Image URL:', image_url);
    if (caption) console.log('[Webhook] Caption:', caption);

    if (secret !== process.env.WEBHOOK_SECRET) {
      console.log('[Webhook] Invalid secret');
      return res.status(401).json({ error: 'Unauthorized' });
    }

    if (!image_url) {
      console.log('[Webhook] Missing image_url');
      return res.status(400).json({ error: 'image_url is required' });
    }

    const pageId = process.env.FACEBOOK_PAGE_ID;
    const accessToken = process.env.FACEBOOK_ACCESS_TOKEN;

    if (!pageId || !accessToken) {
      console.error('[Webhook] FACEBOOK_PAGE_ID or FACEBOOK_ACCESS_TOKEN not set');
      return res.status(500).json({
        success: false,
        error: 'Server misconfiguration: set FACEBOOK_PAGE_ID and FACEBOOK_ACCESS_TOKEN in Vercel',
      });
    }

    const message = (caption && typeof caption === 'string' && caption.trim()) ? caption.trim() : '';
    const form = new URLSearchParams();
    form.set('url', image_url);
    form.set('access_token', accessToken);
    if (message) form.set('message', message);

    console.log('[Webhook] Posting to Facebook Graph API...');
    const fbRes = await fetch(
      `https://graph.facebook.com/v21.0/${pageId}/photos`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: form.toString(),
      }
    );

    const resultText = await fbRes.text();
    console.log('[Webhook] Facebook response status:', fbRes.status);
    console.log('[Webhook] Facebook response:', resultText);

    if (!fbRes.ok) {
      console.error('[Webhook] Facebook API error:', resultText);
      return res.status(500).json({
        success: false,
        error: 'Facebook post failed',
        details: resultText,
      });
    }

    let data;
    try {
      data = JSON.parse(resultText);
    } catch {
      return res.status(500).json({
        success: false,
        error: 'Invalid Facebook response',
        details: resultText,
      });
    }

    const postId = data.id || data.post_id;
    console.log('[Webhook] Success! Post ID:', postId);

    return res.status(200).json({
      success: true,
      message: 'Post published successfully',
      post_id: postId,
      caption: message || null,
    });
  } catch (error) {
    console.error('[Webhook] Error:', error.message);
    console.error('[Webhook] Stack:', error.stack);
    return res.status(500).json({
      success: false,
      error: error.message,
      stack: error.stack,
    });
  }
};
