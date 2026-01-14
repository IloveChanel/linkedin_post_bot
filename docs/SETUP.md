# Complete Setup Guide

This guide will walk you through setting up the LinkedIn Auto-Posting Bot from scratch.

## Prerequisites

Before starting, make sure you have:
- Python 3.9 or higher installed
- A GitHub account
- A Google Cloud account
- A LinkedIn Developer account
- Basic command line knowledge

## Step 1: Clone the Repository

```bash
git clone https://github.com/IloveChanel/linkedin_post_bot.git
cd linkedin_post_bot
```

## Step 2: Set Up Python Environment

### Create a virtual environment (recommended)

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## Step 3: Set Up LinkedIn API

Follow the detailed guide: [LinkedIn API Setup](LINKEDIN_API_SETUP.md)

You'll need:
- LinkedIn Developer App created
- OAuth 2.0 Access Token
- Your Person ID (URN format)

## Step 4: Set Up Google Drive API

Follow the detailed guide: [Google Drive Setup](GOOGLE_DRIVE_SETUP.md)

You'll need:
- Google Cloud Project created
- Service Account created
- Service Account JSON credentials file
- Google Drive folder ID for posts

## Step 5: Configure the Bot

### Create configuration file

Copy the example environment file:

```bash
cp config/.env.example config/.env
```

Edit `config/.env` with your credentials:

```env
LINKEDIN_ACCESS_TOKEN=your_actual_token_here
LINKEDIN_PERSON_ID=urn:li:person:ABC123
GOOGLE_CREDENTIALS_PATH=/absolute/path/to/credentials.json
GOOGLE_DRIVE_FOLDER_ID=1a2b3c4d5e6f7g8h9i
```

### Customize config.yaml

Edit `config/config.yaml` to customize:
- Client information
- Posting schedule
- Timezone settings

## Step 6: Prepare Your Posts

1. Create a folder in Google Drive
2. Add text files (.txt) with your LinkedIn post content
3. Name them descriptively (e.g., "post_about_ai.txt")
4. Share the folder with your service account email
5. Copy the folder ID from the URL

**Folder ID Example:**
```
https://drive.google.com/drive/folders/1a2b3c4d5e6f7g8h9i
                                        ↑ This is your folder ID
```

## Step 7: Test Locally

### Test with dry-run (doesn't actually post)

```bash
cd src
python main.py --dry-run
```

This will:
- ✅ Connect to Google Drive
- ✅ List available posts
- ✅ Select the next post to publish
- ✅ Display what would be posted
- ❌ NOT actually post to LinkedIn

### Test real posting

```bash
cd src
python main.py
```

This will actually post to LinkedIn!

## Step 8: Deploy to GitHub Actions

### Add GitHub Secrets

Go to your repository settings → Secrets and variables → Actions

Add these secrets:

1. `LINKEDIN_ACCESS_TOKEN` - Your LinkedIn OAuth token
2. `LINKEDIN_PERSON_ID` - Your LinkedIn person URN
3. `GOOGLE_CREDENTIALS_JSON` - Contents of your service account JSON file (entire file as text)
4. `GOOGLE_DRIVE_FOLDER_ID` - Your Google Drive folder ID

### Push to GitHub

```bash
git add .
git commit -m "Configure bot for deployment"
git push origin main
```

### Enable GitHub Actions

1. Go to the "Actions" tab in your repository
2. Enable workflows if prompted
3. The bot will now run automatically daily at 12 PM ET!

### Manual Trigger

You can also trigger the bot manually:
1. Go to Actions tab
2. Click "LinkedIn Daily Post" workflow
3. Click "Run workflow" button

## Rotation Logic

The bot uses smart rotation:

1. **First run**: Posts newest file first
2. **Subsequent runs**: Works through posts from newest to oldest
3. **After all posts used**: Loops back to newest and starts over
4. **State persisted**: Tracks which posts have been used

## Monitoring

### Check workflow runs

GitHub Actions → LinkedIn Daily Post → View run logs

### Reset rotation

To start over from the beginning:

```bash
cd src
python main.py --reset
```

## Troubleshooting

### "Authentication failed" error

- Check your LinkedIn access token hasn't expired (they expire every 60 days)
- Regenerate token following [LinkedIn API Setup](LINKEDIN_API_SETUP.md)

### "No posts found" error

- Verify Google Drive folder ID is correct
- Check service account has access to the folder
- Ensure files are `.txt` format

### "Permission denied" error

- Make sure service account email has "Viewer" access to the Drive folder
- Check credentials JSON file path is correct

### Posts not rotating correctly

- Delete `rotation_state.json` to reset
- Or run: `python main.py --reset`

## Getting Help

1. Check the [documentation](../docs/)
2. Review GitHub Actions logs
3. Open an issue on GitHub
4. Enable debug logging: `python main.py --debug`

## Next Steps

- [Client Onboarding Guide](CLIENT_ONBOARDING.md) - Set up for multiple clients
- Customize posting schedule in `.github/workflows/daily_post.yml`
- Add more posts to your Google Drive folder

## Tips for Success

- **Token expiration**: Set a calendar reminder to refresh LinkedIn token every 60 days
- **Content pipeline**: Keep at least 30 posts in rotation for a month
- **Testing**: Always use `--dry-run` when testing new content
- **Monitoring**: Check GitHub Actions weekly to ensure posts are going out
- **Backup**: Keep a backup of your rotation_state.json

---

**Congratulations! Your LinkedIn Auto-Posting Bot is now set up!** 🎉
