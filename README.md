# 🤖 LinkedIn Auto-Posting Bot (Selenium Edition)

A production-ready Python bot that automatically posts to LinkedIn daily using Selenium WebDriver with human-like behavior to avoid detection. Features smart post rotation from Google Drive.

## ✨ Features

- 🕐 **Automated Daily Posting** - Posts between 11:00 AM - 12:00 PM Eastern Time (randomized)
- 🎭 **Human-Like Behavior** - Random delays, natural typing, mouse movements, anti-detection
- 🔄 **Smart Rotation** - Posts newest content first, rotates through all, then loops
- ☁️ **Google Drive Integration** - Store unlimited posts in the cloud
- 🚀 **GitHub Actions** - Runs automatically in the cloud with headless Chrome
- 🔒 **Secure** - Credentials stored safely in GitHub Secrets
- 🛡️ **Stealth Mode** - User-agent rotation, viewport randomization, no automation flags

## 🏗️ Architecture

```
┌─────────────────┐
│  GitHub Actions │  (Triggers daily at 11 AM EST + random 0-59 min)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Selenium Bot   │  (Headless Chrome with anti-detection)
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌─────────┐ ┌──────────┐
│ Google  │ │ LinkedIn │
│  Drive  │ │ (Browser)│
└─────────┘ └──────────┘
```

## 🔧 Technical Details

- **Automation Method**: Selenium WebDriver (NOT LinkedIn API)
- **Browser**: Headless Chrome with anti-detection
- **Human Behavior**: Random delays (2-8s), natural typing, scroll simulation
- **Scheduling**: Daily 11:00 AM - 12:00 PM EST (randomized minute)
- **State Management**: JSON file tracking posted content
- **Error Handling**: Screenshots on failure, retry logic, CAPTCHA detection

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- GitHub account (for Actions)
- Google Cloud account (for Drive API)
- LinkedIn account with email/password login

### Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/IloveChanel/linkedin_post_bot.git
   cd linkedin_post_bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google Drive API**
   - Follow [Google Drive Setup Guide](docs/GOOGLE_DRIVE_SETUP.md)
   - Create a service account and download JSON credentials
   - Share your Google Drive folder with the service account email

4. **Configure GitHub Secrets**
   Add the following secrets to your GitHub repository (Settings > Secrets > Actions):
   
   - `LINKEDIN_EMAIL`: Your LinkedIn email (e.g., michelletrendsetters@gmail.com)
   - `LINKEDIN_PASSWORD`: Your LinkedIn password
   - `GOOGLE_CREDENTIALS`: Base64-encoded service account JSON
     ```bash
     cat credentials.json | base64 -w 0
     ```
   - `GOOGLE_DRIVE_FOLDER_ID`: Your Google Drive folder ID (from folder URL)

5. **Add posts to Google Drive**
   - Create `.txt` files with your post content
   - Upload to your Google Drive folder
   - Bot will post newest first, then rotate through all

6. **Test locally (recommended)**
   ```bash
   cd bot
   python main.py --dry-run --no-random-delay --debug
   ```

7. **Deploy to GitHub Actions**
   - Push to main branch
   - Bot will run automatically daily at 11 AM EST (+ random 0-59 min)
   - Or trigger manually from Actions tab

## 📁 Project Structure

```
linkedin_post_bot/
├── .github/workflows/
│   └── post-to-linkedin.yml    # GitHub Actions workflow (Selenium + Chrome)
├── bot/                         # Core bot code
│   ├── __init__.py
│   ├── main.py                  # Main orchestration script
│   ├── linkedin_poster.py       # Selenium automation for LinkedIn
│   ├── drive_reader.py          # Google Drive integration
│   ├── post_tracker.py          # Post rotation state management
│   └── human_behavior.py        # Anti-detection utilities
├── config/                      # Configuration files (optional)
├── docs/                        # Setup guides
├── tests/                       # Unit tests
└── requirements.txt             # Python dependencies
```

## 📚 Documentation

- [Complete Setup Guide](docs/SETUP.md)
- [Google Drive Setup](docs/GOOGLE_DRIVE_SETUP.md)
- [Troubleshooting Guide](#-troubleshooting)

## 🔐 Required GitHub Secrets

| Secret Name | Description | Example |
|------------|-------------|---------|
| `LINKEDIN_EMAIL` | Your LinkedIn login email | michelletrendsetters@gmail.com |
| `LINKEDIN_PASSWORD` | Your LinkedIn password | YourSecurePassword123! |
| `GOOGLE_CREDENTIALS` | Base64-encoded service account JSON | eyJ0eXBlIjoic2VydmljZV9hY2NvdW50... |
| `GOOGLE_DRIVE_FOLDER_ID` | Google Drive folder ID | 1CVSC-w6uY1zv7-_a_9_zsPRqSAQWhukz |

### How to encode Google credentials:
```bash
# Linux/Mac
cat credentials.json | base64 -w 0

# Windows (PowerShell)
[Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes((Get-Content credentials.json)))
```

## 🎯 Usage

### Local Testing
```bash
# Dry run (no posting, with browser visible)
cd bot
python main.py --dry-run --no-random-delay --no-headless --debug

# Dry run (headless)
python main.py --dry-run --no-random-delay --headless

# Actual post (use with caution!)
python main.py --no-random-delay --headless

# Reset rotation state
python main.py --reset
```

### GitHub Actions
- Runs automatically daily at 11 AM EST (+ random 0-59 minutes)
- Can be triggered manually from Actions tab
- Check Actions tab for logs and screenshots
- Download `post-rotation-state` artifact to see posting history

## 🛡️ Anti-Detection Features

- ✅ **Random Delays**: 2-8 seconds between actions
- ✅ **Natural Typing**: 50-200ms delays between keystrokes  
- ✅ **User-Agent Rotation**: Different browser signatures
- ✅ **Viewport Randomization**: Varying window sizes
- ✅ **Scroll Behavior**: Random scrolling before actions
- ✅ **Thinking Pauses**: 3-5 second delays to appear human
- ✅ **Stealth Mode**: Disabled automation flags
- ✅ **Time Randomization**: Posts at random minute between 11-12 PM EST

## 🐛 Troubleshooting

### Login Fails
- **CAPTCHA detected**: LinkedIn may require manual verification. Check screenshots in Actions artifacts.
- **Wrong credentials**: Verify `LINKEDIN_EMAIL` and `LINKEDIN_PASSWORD` secrets.
- **2FA enabled**: Bot doesn't support 2FA. Disable it or use app-specific password.

### No Posts Found
- Check `GOOGLE_DRIVE_FOLDER_ID` is correct
- Ensure service account has access to the folder
- Verify files are `.txt` format
- Check Google Cloud Console for API errors

### Bot Crashes
- Check GitHub Actions logs for detailed error messages
- Download screenshots artifact to see what happened
- Verify Chrome installed correctly
- Test locally with `--debug` flag

### Post Not Appearing
- LinkedIn may be rate limiting - wait 24 hours
- Check if post was actually submitted (screenshot)
- Verify you're checking the correct profile
- Post might be in "drafts" if submit failed

## 🔐 Security

- ✅ Credentials stored in GitHub Secrets (never in code)
- ✅ `.gitignore` prevents accidental credential commits
- ✅ Service account authentication for Google Drive
- ✅ Credentials cleaned up after each run
- ✅ No logging of passwords or sensitive data

### Security Best Practices
1. **Never commit credentials** to Git
2. **Use strong passwords** for LinkedIn
3. **Rotate credentials** periodically
4. **Monitor account activity** on LinkedIn
5. **Use dedicated service account** for Google Drive
6. **Enable GitHub secret scanning**

## ⚠️ Disclaimer

This bot automates LinkedIn posting using browser automation. Use responsibly:
- ⚠️ Violates LinkedIn's Terms of Service (use at your own risk)
- ⚠️ May result in account restrictions or bans if detected
- ⚠️ No warranty provided - use for educational purposes
- ⚠️ Consider official LinkedIn API for production use

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - feel free to use this for your business!

## 🆘 Support

Having issues? Check the [Setup Guide](docs/SETUP.md) or open an issue.

---

**Built for:** Michelle Vance ([@michelle-vance-ai-engineer](https://www.linkedin.com/in/michelle-vance-ai-engineer/))  
**Purpose:** Scale LinkedIn posting services for multiple clients
