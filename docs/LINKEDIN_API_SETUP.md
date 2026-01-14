# LinkedIn API Setup Guide

This guide walks you through setting up LinkedIn API access for the auto-posting bot.

## Overview

LinkedIn uses OAuth 2.0 for authentication. You'll need to:
1. Create a LinkedIn Developer App
2. Get permissions for posting
3. Generate an access token
4. Get your Person ID

## Step 1: Create LinkedIn Developer App

### 1.1 Go to LinkedIn Developers

Visit: https://www.linkedin.com/developers/apps

### 1.2 Create New App

1. Click **"Create app"**
2. Fill in the form:
   - **App name**: "LinkedIn Auto Poster" (or your choice)
   - **LinkedIn Page**: Select your company page (or create one)
   - **App logo**: Upload a logo (optional but recommended)
   - **Legal agreement**: Check the box
3. Click **"Create app"**

### 1.3 Verify Your App

1. You may need to verify your app via email
2. Follow the verification steps sent to your email

## Step 2: Configure App Settings

### 2.1 Request API Access

1. In your app dashboard, go to the **"Products"** tab
2. Request access to:
   - ✅ **"Share on LinkedIn"** - For posting content
   - ✅ **"Sign In with LinkedIn"** - For authentication

3. Wait for approval (usually instant for personal use)

### 2.2 Set Up OAuth 2.0

1. Go to the **"Auth"** tab
2. Add **Redirect URLs**:
   ```
   http://localhost:8080/callback
   https://www.linkedin.com/developers/tools/oauth/redirect
   ```
3. Note down:
   - **Client ID**
   - **Client Secret**

## Step 3: Generate Access Token

### Method 1: Using LinkedIn OAuth Tool (Easiest)

1. Go to: https://www.linkedin.com/developers/tools/oauth
2. Select your app
3. Select scopes:
   - ✅ `r_liteprofile` - Read profile
   - ✅ `w_member_social` - Post on behalf of user
4. Click **"Request access token"**
5. Authorize the app
6. Copy the **Access Token**

⚠️ **Important**: Tokens expire after 60 days!

### Method 2: Using Authorization Code Flow (Advanced)

#### Step 3.1: Get Authorization Code

Build this URL (replace with your values):

```
https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=http://localhost:8080/callback&scope=r_liteprofile%20w_member_social
```

1. Open in browser
2. Authorize the app
3. You'll be redirected to: `http://localhost:8080/callback?code=AUTHORIZATION_CODE`
4. Copy the `code` parameter

#### Step 3.2: Exchange for Access Token

Use curl or Postman:

```bash
curl -X POST https://www.linkedin.com/oauth/v2/accessToken \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "code=YOUR_AUTHORIZATION_CODE" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET" \
  -d "redirect_uri=http://localhost:8080/callback"
```

Response:
```json
{
  "access_token": "YOUR_ACCESS_TOKEN",
  "expires_in": 5184000
}
```

## Step 4: Get Your Person ID

### Method 1: Using API Call

```bash
curl -X GET https://api.linkedin.com/v2/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Response:
```json
{
  "id": "ABC123xyz",
  ...
}
```

Your Person ID is: `urn:li:person:ABC123xyz`

### Method 2: Using LinkedIn Profile URL

If your profile URL is:
```
https://www.linkedin.com/in/michelle-vance-ai-engineer/
```

You can try (may require additional API calls):
1. Use the `/me` endpoint (shown above)
2. The `id` field is what you need
3. Format as: `urn:li:person:{id}`

## Step 5: Add to Configuration

Add these to your `config/.env` file:

```env
LINKEDIN_ACCESS_TOKEN=AQV...your_token_here
LINKEDIN_PERSON_ID=urn:li:person:ABC123xyz
```

## Step 6: Test Your Setup

Run the test command:

```bash
cd src
python -c "
from linkedin_poster import LinkedInPoster
import os
from dotenv import load_dotenv

load_dotenv('../config/.env')
token = os.getenv('LINKEDIN_ACCESS_TOKEN')
person_id = os.getenv('LINKEDIN_PERSON_ID')

poster = LinkedInPoster(token, person_id)
if poster.validate_token():
    print('✅ LinkedIn API setup successful!')
    profile = poster.get_profile_info()
    print(f'Connected as: {profile.get(\"localizedFirstName\")} {profile.get(\"localizedLastName\")}')
else:
    print('❌ LinkedIn API setup failed!')
"
```

## Token Refresh Strategy

LinkedIn access tokens expire after 60 days. Here are strategies:

### Strategy 1: Manual Refresh (Simple)

1. Set a calendar reminder for every 55 days
2. Regenerate token using OAuth tool
3. Update GitHub secret: `LINKEDIN_ACCESS_TOKEN`

### Strategy 2: Automated Refresh (Advanced)

Implement token refresh in your bot:
- Store refresh token
- Check expiration before posting
- Auto-refresh when needed
- Update stored token

*Note: This requires additional implementation*

## Troubleshooting

### "Invalid access token" error

- Token may have expired (60-day limit)
- Regenerate token following Step 3

### "Insufficient permissions" error

- Make sure you requested "Share on LinkedIn" product
- Check scopes include `w_member_social`

### "Invalid person ID" error

- Verify format: `urn:li:person:YOUR_ID`
- Double-check ID from `/me` endpoint

### Can't create app

- You need a LinkedIn Page (company page)
- Create a page if you don't have one: https://www.linkedin.com/company/setup/new/

## Security Best Practices

✅ **DO:**
- Store tokens in environment variables
- Use GitHub Secrets for production
- Regenerate tokens regularly
- Restrict API permissions to minimum needed

❌ **DON'T:**
- Commit tokens to Git
- Share tokens publicly
- Use tokens in client-side code
- Grant unnecessary permissions

## Rate Limits

LinkedIn API has rate limits:
- **Posts**: 100 per day per user
- **API calls**: Varies by endpoint

For this bot (1 post/day), you'll never hit limits.

## Additional Resources

- [LinkedIn API Documentation](https://docs.microsoft.com/en-us/linkedin/)
- [OAuth 2.0 Guide](https://docs.microsoft.com/en-us/linkedin/shared/authentication/authentication)
- [Share on LinkedIn API](https://docs.microsoft.com/en-us/linkedin/marketing/integrations/community-management/shares/share-api)

## Next Steps

Once you have your LinkedIn credentials:
1. ✅ Add to `config/.env`
2. ✅ Test locally with `--dry-run`
3. ✅ Add to GitHub Secrets
4. ✅ Move on to [Google Drive Setup](GOOGLE_DRIVE_SETUP.md)

---

**Need Help?** Open an issue on GitHub with your error message (don't include tokens!)
