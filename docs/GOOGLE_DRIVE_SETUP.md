# Google Drive API Setup Guide

This guide walks you through setting up Google Drive API access for storing and managing LinkedIn posts.

## Overview

The bot uses Google Drive to store your LinkedIn posts as text files. You'll need to:
1. Create a Google Cloud Project
2. Enable the Google Drive API
3. Create a Service Account
4. Download credentials JSON
5. Create a Drive folder and share it with the service account

## Step 1: Create Google Cloud Project

### 1.1 Go to Google Cloud Console

Visit: https://console.cloud.google.com/

### 1.2 Create New Project

1. Click **"Select a project"** dropdown (top of page)
2. Click **"New Project"**
3. Enter project details:
   - **Project name**: "LinkedIn Post Bot" (or your choice)
   - **Organization**: Leave as-is (optional)
4. Click **"Create"**
5. Wait for project creation (takes a few seconds)

### 1.3 Select Your Project

Make sure your new project is selected in the top dropdown.

## Step 2: Enable Google Drive API

### 2.1 Navigate to API Library

1. In the left sidebar, click **"APIs & Services"** → **"Library"**
2. Or visit: https://console.cloud.google.com/apis/library

### 2.2 Enable Drive API

1. Search for "Google Drive API"
2. Click on **"Google Drive API"**
3. Click **"Enable"**
4. Wait for activation

## Step 3: Create Service Account

### 3.1 Navigate to Service Accounts

1. In the left sidebar: **"APIs & Services"** → **"Credentials"**
2. Or visit: https://console.cloud.google.com/apis/credentials

### 3.2 Create Service Account

1. Click **"+ Create Credentials"** → **"Service Account"**
2. Fill in details:
   - **Service account name**: "linkedin-bot" (or your choice)
   - **Service account ID**: Auto-generated (or customize)
   - **Description**: "Service account for LinkedIn posting bot"
3. Click **"Create and Continue"**

### 3.3 Grant Permissions (Optional)

1. **Role**: Can leave blank for Drive API
2. Click **"Continue"**
3. Click **"Done"**

## Step 4: Download Credentials

### 4.1 Create Key

1. Find your service account in the list
2. Click on the service account email
3. Go to **"Keys"** tab
4. Click **"Add Key"** → **"Create new key"**
5. Select **"JSON"** format
6. Click **"Create"**

### 4.2 Save Credentials File

1. JSON file will download automatically
2. Rename to something memorable: `linkedin-bot-credentials.json`
3. Move to a secure location (NOT in your git repository!)

⚠️ **IMPORTANT**: Keep this file secure! It grants access to your Drive.

### 4.3 Note the Service Account Email

In the JSON file, find the `client_email` field:

```json
{
  "type": "service_account",
  "project_id": "your-project",
  "client_email": "linkedin-bot@your-project.iam.gserviceaccount.com",
  ...
}
```

You'll need this email in the next step!

## Step 5: Create Drive Folder

### 5.1 Create Folder

1. Go to Google Drive: https://drive.google.com/
2. Click **"+ New"** → **"Folder"**
3. Name it: "LinkedIn Posts" (or your choice)
4. Click **"Create"**

### 5.2 Get Folder ID

1. Open the folder you just created
2. Look at the URL:
   ```
   https://drive.google.com/drive/folders/1a2b3c4d5e6f7g8h9i0j
                                           ↑ This is your folder ID
   ```
3. Copy the folder ID (the random string after `/folders/`)

### 5.3 Share Folder with Service Account

1. Right-click the folder → **"Share"**
2. In the "Add people and groups" field, paste your service account email:
   ```
   linkedin-bot@your-project.iam.gserviceaccount.com
   ```
3. Set permission to **"Viewer"** (read-only is sufficient)
4. Uncheck **"Notify people"** (service accounts don't get emails)
5. Click **"Share"**

## Step 6: Add Sample Posts

### 6.1 Create Text Files

In your "LinkedIn Posts" folder, create some test posts:

**File 1: test_post_1.txt**
```
🚀 Excited to share my latest project!

I've been working on an AI-powered solution that helps businesses automate their social media presence.

Key features:
✨ Smart content rotation
📅 Automated scheduling
🔒 Secure credential management

What automation tools do you use for social media?

#AI #Automation #SocialMedia #LinkedIn
```

**File 2: test_post_2.txt**
```
💡 Pro tip for developers:

Always use environment variables for sensitive credentials.

Never commit:
❌ API keys
❌ Passwords
❌ Access tokens

Use:
✅ .env files (gitignored)
✅ GitHub Secrets
✅ Environment managers

Security first! 🔐

#CodingBestPractices #DevSecOps #Python
```

### 6.2 Upload to Drive

1. Drag and drop the `.txt` files into your "LinkedIn Posts" folder
2. Or use **"+ New"** → **"File upload"**

## Step 7: Configure the Bot

Add these to your `config/.env` file:

```env
GOOGLE_CREDENTIALS_PATH=/absolute/path/to/linkedin-bot-credentials.json
GOOGLE_DRIVE_FOLDER_ID=1a2b3c4d5e6f7g8h9i0j
```

**Important**: Use absolute path for credentials file!

### For Local Development

```env
GOOGLE_CREDENTIALS_PATH=/Users/yourname/secrets/linkedin-bot-credentials.json
GOOGLE_DRIVE_FOLDER_ID=1a2b3c4d5e6f7g8h9i0j
```

### For GitHub Actions

You'll add the entire JSON file contents as a secret (see main setup guide).

## Step 8: Test Your Setup

Run this test command:

```bash
cd src
python -c "
from google_drive_manager import GoogleDriveManager
import os
from dotenv import load_dotenv

load_dotenv('../config/.env')
creds_path = os.getenv('GOOGLE_CREDENTIALS_PATH')
folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID')

manager = GoogleDriveManager(creds_path, folder_id)
posts = manager.list_posts()

print(f'✅ Found {len(posts)} posts in Drive folder!')
for post in posts:
    print(f'  - {post[\"name\"]}')
"
```

Expected output:
```
✅ Found 2 posts in Drive folder!
  - test_post_1.txt
  - test_post_2.txt
```

## Folder Organization Tips

### Single Client

```
LinkedIn Posts/
├── post_about_ai.txt
├── post_about_automation.txt
├── post_about_python.txt
└── motivational_monday.txt
```

### Multiple Clients (Separate Bots)

```
Client 1 - LinkedIn Posts/
├── post_1.txt
└── post_2.txt

Client 2 - LinkedIn Posts/
├── post_1.txt
└── post_2.txt
```

Use different folder IDs in separate config files.

## Post Content Guidelines

### File Format

- **Extension**: Must be `.txt`
- **Encoding**: UTF-8
- **Line endings**: Any (will work)

### Content Format

```
[Attention grabber or emoji]

[Main content paragraphs]

[Call to action or question]

#Hashtag1 #Hashtag2 #Hashtag3
```

### Best Practices

✅ **DO:**
- Keep posts under 3,000 characters (LinkedIn limit)
- Use line breaks for readability
- Include 3-5 relevant hashtags
- Add emojis for engagement
- Ask questions to encourage comments

❌ **DON'T:**
- Use special formatting (LinkedIn API posts as plain text)
- Include images (not supported in this version)
- Use external links without context
- Exceed character limits

## Troubleshooting

### "Authentication failed"

- Check credentials file path is correct and absolute
- Verify JSON file is valid (not corrupted)
- Ensure service account is created correctly

### "No posts found"

- Verify folder ID is correct (check Drive URL)
- Ensure folder is shared with service account email
- Check files are `.txt` format (not `.doc`, `.docx`)
- Files must not be in trash

### "Permission denied"

- Share folder with service account email (check spam/sharing settings)
- Ensure permission is at least "Viewer"
- Service account email ends with `.iam.gserviceaccount.com`

### "Invalid folder ID"

- Folder ID is the random string in the URL
- Don't include `https://` or `/folders/`
- Just the alphanumeric ID

## Security Best Practices

✅ **DO:**
- Store credentials file outside git repository
- Use `.gitignore` to prevent accidental commits
- Set folder permissions to minimum needed (Viewer)
- Regularly audit service account access

❌ **DON'T:**
- Commit credentials JSON to Git
- Share service account key publicly
- Give service account unnecessary permissions
- Use personal account instead of service account

## Advanced: Multiple Folders

To manage multiple clients with one service account:

1. Create separate folders for each client
2. Share all folders with the same service account
3. Use different `GOOGLE_DRIVE_FOLDER_ID` for each client's config

## Rate Limits

Google Drive API quotas:
- **Queries per day**: 1,000,000,000 (yes, 1 billion!)
- **Queries per 100 seconds**: 1,000

For this bot (1 post/day), you'll never hit limits.

## Additional Resources

- [Google Drive API Documentation](https://developers.google.com/drive/api/v3/about-sdk)
- [Service Accounts Guide](https://cloud.google.com/iam/docs/service-accounts)
- [Python Quickstart](https://developers.google.com/drive/api/v3/quickstart/python)

## Next Steps

Once you have your Google Drive setup:
1. ✅ Add credentials to `config/.env`
2. ✅ Test locally with sample posts
3. ✅ Add to GitHub Secrets for deployment
4. ✅ Return to [Setup Guide](SETUP.md)

---

**Need Help?** Open an issue on GitHub (don't share your credentials!)
