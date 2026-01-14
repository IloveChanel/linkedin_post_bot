# 🤖 LinkedIn Auto-Posting Bot

A production-ready Python bot that automatically posts to LinkedIn daily with smart post rotation from Google Drive. Perfect for social media managers and agencies managing multiple client accounts.

## ✨ Features

- 🕐 **Automated Daily Posting** - Posts at 12:00 PM Eastern Time (customizable)
- 🔄 **Smart Rotation** - Posts newest content first, rotates to oldest, then loops
- ☁️ **Google Drive Integration** - Store unlimited posts in the cloud, zero code clutter
- 🎯 **Multi-Client Ready** - Easy configuration for managing multiple LinkedIn accounts
- 🚀 **GitHub Actions** - Runs automatically in the cloud (your computer stays off!)
- 🔒 **Secure** - API credentials stored safely in GitHub Secrets
- 💰 **Business Scalable** - Built for agencies charging clients for posting services

## 🏗️ Architecture

```
┌─────────────────┐
│  GitHub Actions │  (Triggers daily at noon ET)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Python Bot    │  (Fetches next post)
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌─────────┐ ┌──────────┐
│ Google  │ │ LinkedIn │
│  Drive  │ │   API    │
└─────────┘ └──────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- GitHub account (for Actions)
- Google Cloud account (for Drive API)
- LinkedIn Developer account (for API access)

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

3. **Set up API credentials**
   - Follow [LinkedIn API Setup Guide](docs/LINKEDIN_API_SETUP.md)
   - Follow [Google Drive Setup Guide](docs/GOOGLE_DRIVE_SETUP.md)

4. **Configure your client**
   - Edit `config/config.yaml` with your settings
   - Copy `config/.env.example` to `config/.env` and add credentials

5. **Test locally**
   ```bash
   python src/main.py --dry-run
   ```

6. **Deploy to GitHub Actions**
   - Add secrets to your GitHub repository
   - Push to main branch
   - Bot will run automatically daily at noon ET!

## 📁 Project Structure

```
linkedin_post_bot/
├── .github/workflows/     # GitHub Actions automation
├── src/                   # Core bot code
│   ├── linkedin_poster.py
│   ├── google_drive_manager.py
│   ├── post_rotator.py
│   └── main.py
├── config/                # Configuration files
├── docs/                  # Setup guides
├── tests/                 # Unit tests
└── requirements.txt       # Python dependencies
```

## 📚 Documentation

- [Complete Setup Guide](docs/SETUP.md)
- [LinkedIn API Setup](docs/LINKEDIN_API_SETUP.md)
- [Google Drive Setup](docs/GOOGLE_DRIVE_SETUP.md)
- [Client Onboarding](docs/CLIENT_ONBOARDING.md)

## 🎯 Use Cases

### For Personal Use
Automate your LinkedIn presence with consistent daily posts

### For Agencies
- Manage multiple client accounts
- Charge clients for automated posting services
- Scale without hiring more social media managers
- Easy onboarding with separate configs per client

## 💼 Business Model

This bot is designed for agencies to offer LinkedIn posting services:
- **Setup Fee**: $500-1000 per client
- **Monthly Fee**: $200-500 per client for posting service
- **Time Saved**: 30+ minutes per day per client

## 🔐 Security

- API credentials stored in GitHub Secrets (never in code)
- `.gitignore` prevents accidental credential commits
- OAuth 2.0 authentication for LinkedIn
- Service account authentication for Google Drive

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - feel free to use this for your business!

## 🆘 Support

Having issues? Check the [Setup Guide](docs/SETUP.md) or open an issue.

---

**Built for:** Michelle Vance ([@michelle-vance-ai-engineer](https://www.linkedin.com/in/michelle-vance-ai-engineer/))  
**Purpose:** Scale LinkedIn posting services for multiple clients
