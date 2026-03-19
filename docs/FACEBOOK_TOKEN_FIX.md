# Fix "publish_actions deprecated" (500 from webhook)

Your setup (Publisher system user with Full control on **Nethmi G** Page and **Postbot page manager** App) is correct. The error happens because the **token** or the **app** is still using the deprecated `publish_actions` permission.

## 1. Regenerate the System User token (right permissions)

1. **Meta Business Suite** → **Business settings** → **Users** → **System users** → **Publisher**.
2. Click **Revoke tokens** (so the old token stops working).
3. Click **Generate token**.
4. Select the app **Postbot page manager**.
5. In the **permissions** list, select **only**:
   - **Manage and post to Pages** (or `pages_manage_posts`)
   - **Pages show list** (`pages_show_list`) if shown  
   Do **not** select anything like "publish_actions" or "Post on behalf of the user".
6. Generate and **copy the new token**.
7. In **Vercel** → your project → **Settings** → **Environment Variables** → set **`FACEBOOK_ACCESS_TOKEN`** to this new token. Redeploy if needed.

## 2. Remove deprecated permission from the App (if needed)

1. Go to [developers.facebook.com/apps](https://developers.facebook.com/apps/).
2. Open the app **Postbot page manager** (App ID: 1322909699321425).
3. Go to **App Review** → **Permissions and features** (or **Use cases**).
4. If you see **publish_actions**, remove it or do not use it. Page posting does **not** use `publish_actions`; it uses **pages_manage_posts**.
5. Ensure the app has **pages_manage_posts** (and optionally **pages_show_list**) for the Page.

## 3. Confirm env in Vercel

- **`FACEBOOK_ACCESS_TOKEN`** = the **new** system user token (from step 1).
- **`FACEBOOK_PAGE_ID`** = `1025914070602506` (Nethmi G).

Then run the workflow again from GitHub Actions.

## Optional: test with a user-based Page token first

To confirm the webhook and Page ID work:

1. [Graph API Explorer](https://developers.facebook.com/tools/explorer/) → select **Postbot page manager**.
2. Add permissions: **pages_show_list**, **pages_manage_posts** → **Generate User Token**.
3. Call **GET** `me/accounts`.
4. In the response, find the page **Nethmi G** and copy its **`access_token`**.
5. Put that token in Vercel **`FACEBOOK_ACCESS_TOKEN`** and run the workflow.

If it works with this token, the only remaining issue is generating a system user token with the same Page permissions (steps 1–2 above).
