# Client Onboarding Guide

This guide is for agencies or consultants managing multiple client LinkedIn accounts with the auto-posting bot.

## Overview

This bot is designed to scale to multiple clients. Each client gets:
- Their own configuration
- Their own Google Drive folder
- Their own LinkedIn credentials
- Independent posting schedules

## Onboarding Workflow

### For Each New Client

1. **Collect Information**
2. **Set Up APIs**
3. **Configure Bot**
4. **Test & Deploy**
5. **Train Client**

---

## Step 1: Collect Client Information

### Information Checklist

- [ ] Client name and company
- [ ] LinkedIn profile URL
- [ ] Preferred posting time and timezone
- [ ] Contact email
- [ ] Number of posts to start with
- [ ] Content approval process

### Client Questionnaire Template

```
Client Onboarding Form
━━━━━━━━━━━━━━━━━━━━

Business Information:
- Company Name: _______________
- Client Contact: _______________
- Email: _______________
- Phone: _______________

LinkedIn Information:
- LinkedIn Profile URL: _______________
- LinkedIn Company Page (if applicable): _______________
- Current posting frequency: _______________

Posting Preferences:
- Preferred posting time: _______________
- Timezone: _______________
- Days to post: Mon-Fri / Daily / Custom: _______________

Content:
- How many posts will you provide initially? _______________
- Who creates content? Client / Agency / Both
- Approval process: Pre-approval / Post-review / Automated
```

---

## Step 2: Set Up APIs for Client

### 2.1 LinkedIn API Setup

**Option A: Client Has Their Own Developer Account**

Guide client through [LinkedIn API Setup](LINKEDIN_API_SETUP.md)

They provide you:
- Access Token
- Person ID

**Option B: You Manage Everything**

1. Ask client to add you as admin to their LinkedIn account (temporarily)
2. Create developer app under their account
3. Generate access token
4. Securely provide token to client or store in your system
5. Remove yourself as admin

### 2.2 Google Drive Setup

**For Each Client:**

1. Create a new folder in your Google Drive:
   ```
   Clients/
   ├── Client1_LinkedIn_Posts/
   ├── Client2_LinkedIn_Posts/
   └── Client3_LinkedIn_Posts/
   ```

2. Share with your service account (one service account can access all)

3. Get folder ID for each client

4. Optionally: Share folder with client for them to add/edit posts

---

## Step 3: Configure Bot

### 3.1 Repository Structure for Multiple Clients

**Option A: Separate Repository Per Client** (Recommended for agencies)

```
client1_linkedin_bot/
├── config/
│   ├── config.yaml
│   └── .env
└── ...

client2_linkedin_bot/
├── config/
│   ├── config.yaml
│   └── .env
└── ...
```

Benefits:
- Complete isolation
- Separate GitHub Actions
- Independent schedules
- Easy to manage

**Option B: Single Repository with Multiple Configs**

```
linkedin_post_bot/
├── config/
│   ├── client1/
│   │   ├── config.yaml
│   │   └── .env
│   ├── client2/
│   │   ├── config.yaml
│   │   └── .env
└── ...
```

Benefits:
- Centralized management
- Easier updates
- Shared codebase

### 3.2 Create Client Configuration

**config/config.yaml** for this client:

```yaml
# Client Information
client:
  name: "Acme Corporation"
  linkedin_profile: "https://www.linkedin.com/in/john-doe/"
  contact_email: "john@acme.com"

# Posting Schedule
schedule:
  timezone: "America/Chicago"  # Client's timezone
  post_time: "09:00"  # 9:00 AM
  enabled: true

# Rotation Settings
rotation:
  strategy: "newest_first"
  reset_on_complete: true

# Rotation State File (unique per client)
rotation_state_file: "rotation_state_acme.json"

# Logging
logging:
  level: "INFO"
  format: "detailed"
```

**config/.env** for this client:

```env
LINKEDIN_ACCESS_TOKEN=client_token_here
LINKEDIN_PERSON_ID=urn:li:person:client_id_here
GOOGLE_CREDENTIALS_PATH=credentials.json
GOOGLE_DRIVE_FOLDER_ID=client_folder_id_here
TZ=America/Chicago
```

### 3.3 Set Up GitHub Secrets

For each client repository, add secrets:

```
LINKEDIN_ACCESS_TOKEN_CLIENT1
LINKEDIN_PERSON_ID_CLIENT1
GOOGLE_DRIVE_FOLDER_ID_CLIENT1
GOOGLE_CREDENTIALS_JSON
```

---

## Step 4: Test & Deploy

### 4.1 Initial Content Setup

1. Ask client to provide 30 posts (1 month of content)
2. Format posts as `.txt` files
3. Upload to client's Google Drive folder
4. Verify bot can access them

### 4.2 Dry Run Test

```bash
cd src
python main.py --dry-run --config ../config/client1/config.yaml
```

Verify:
- ✅ Connects to Google Drive
- ✅ Finds all posts
- ✅ Selects correct post
- ✅ Displays post content

### 4.3 Live Test

```bash
python main.py --config ../config/client1/config.yaml
```

Verify:
- ✅ Posts to correct LinkedIn account
- ✅ Content appears correctly
- ✅ Rotation state saved

### 4.4 Deploy to GitHub Actions

1. Push client config to repository
2. Verify GitHub secrets are set
3. Trigger workflow manually to test
4. Confirm post appears on LinkedIn
5. Check for any errors in Actions log

---

## Step 5: Train Client

### 5.1 Show Client How to Add Posts

**Video Tutorial Script:**

```
1. Go to Google Drive
2. Open your "LinkedIn Posts" folder
3. Click "+ New" → "Google Docs" or "File upload"
4. If using Docs:
   - Write your post
   - File → Download → Plain text (.txt)
   - Upload the .txt file
5. If uploading directly:
   - Create .txt file on your computer
   - Drag and drop to Drive folder
6. That's it! The bot will pick it up automatically
```

### 5.2 Provide Client Documentation

Create a simplified guide for clients:

**ClientName_LinkedIn_Bot_Guide.pdf** should include:

1. **How to add new posts**
2. **Posting schedule** (when posts go live)
3. **How to check if posts went out** (LinkedIn activity)
4. **Who to contact for support** (your email/phone)
5. **How rotation works** (newest to oldest)
6. **Content best practices**

### 5.3 Set Expectations

**What client should expect:**

✅ Posts go live automatically at scheduled time
✅ Content rotates through all posts then loops
✅ No maintenance needed once set up
✅ Can add new posts anytime to Drive folder

**What client should NOT expect:**

❌ Image posting (text only in this version)
❌ Immediate posting (scheduled only)
❌ Post editing after published
❌ Analytics/insights (LinkedIn provides this separately)

---

## Pricing Model for Agencies

### Setup Fees

- **Initial Setup**: $500-1,000 per client
  - LinkedIn API setup
  - Google Drive configuration
  - Repository deployment
  - Initial content upload
  - Testing

### Monthly Recurring

- **Posting Service**: $200-500/month per client
  - Automated daily posting
  - Content rotation management
  - API token management
  - Technical support

### Additional Services

- **Content Creation**: $50-100 per post
- **Content Calendar Management**: $100-300/month
- **Analytics Report**: $100-200/month
- **Emergency Post**: $50 per post

---

## Maintenance Checklist

### Weekly

- [ ] Check all GitHub Actions ran successfully
- [ ] Verify posts are going out for all clients
- [ ] Review any error notifications

### Monthly

- [ ] Verify clients have upcoming content in Drive
- [ ] Send content reminder to clients low on posts
- [ ] Review and optimize posting times if needed

### Every 60 Days

- [ ] Refresh LinkedIn access tokens (they expire!)
- [ ] Update GitHub secrets with new tokens
- [ ] Notify clients of token refresh

### Quarterly

- [ ] Review client satisfaction
- [ ] Discuss additional services
- [ ] Optimize posting strategy based on engagement

---

## Troubleshooting Common Client Issues

### "My post didn't go out today"

1. Check GitHub Actions logs
2. Verify LinkedIn token is valid (not expired)
3. Check Google Drive folder has posts
4. Verify client didn't delete/move files

### "Wrong post was published"

1. Check rotation_state.json
2. Explain rotation logic (newest to oldest)
3. If needed: `python main.py --reset` to restart rotation

### "I want to change posting time"

1. Update `config.yaml` schedule section
2. Update `.github/workflows/daily_post.yml` cron schedule
3. Commit and push changes

### "Can I post images?"

- Not supported in current version
- Requires LinkedIn image upload API
- Consider as future enhancement

---

## Scaling to 10+ Clients

### Infrastructure

- Use separate repositories per client (easier isolation)
- Consider client management dashboard (future enhancement)
- Automate onboarding with scripts
- Use monitoring tools (GitHub Actions notifications)

### Team Management

- Designate team member for onboarding
- Create internal wiki with processes
- Set up escalation procedures
- Use ticketing system for client requests

### Client Communication

- Monthly email: "Your posts this month"
- Quarterly check-ins
- Automated alerts for token expiration
- Client portal for self-service (future)

---

## Offboarding Clients

### When Client Leaves

1. **Stop bot**: Disable GitHub Actions workflow
2. **Backup data**: Save rotation state and config
3. **Transfer data**: Provide client with all post content
4. **Revoke access**: Remove service account from their Drive folder
5. **Documentation**: Provide export of what was posted

### Data Retention

- Keep configs for 90 days (for reactivation)
- Delete rotation states after 30 days
- Archive posted content per your policy

---

## Next-Level Features (Future Enhancements)

Ideas for expanding the service:

- 📸 **Image posting** - Support image uploads
- 📊 **Analytics dashboard** - Track engagement
- 🤖 **AI content generation** - Auto-generate posts
- 📅 **Multi-time posting** - Post multiple times per day
- 🔗 **Multi-platform** - Twitter, Facebook, etc.
- 💬 **Comment management** - Auto-respond to comments
- 📱 **Mobile app** - Client mobile app for posting

---

## Resources for Clients

- [LinkedIn Content Best Practices](https://business.linkedin.com/marketing-solutions/blog/linkedin-b2b-marketing/2021/10-linkedin-post-tips-for-b2b-marketers)
- [Hashtag Research Tools](https://www.linkedin.com/help/linkedin/answer/a524335)
- [LinkedIn Algorithm Insights](https://www.linkedin.com/business/marketing/blog/linkedin-ads/understanding-linkedin-algorithm)

---

**Questions?** Contact your bot administrator or open an issue on GitHub.
