# Crypto Dust Scanner

Find forgotten crypto wallets and unclaimed rewards across Ethereum and BSC networks.

## Features
- 🔍 Scan inactive wallets (30-730 days)
- 💰 Detect dust balances ($1+)
- 🎁 Find unclaimed rewards
- 🚨 Honeypot detection
- 📱 Real-time Firebase updates
- 🤖 Telegram notifications
- ⚡ GitHub Actions (24/7 free)

## Setup Instructions

### 1. Create GitHub Repository
- Go to github.com and create a new repository
- Name it `crypto-dust-scanner`

### 2. Add Secrets to GitHub
Go to Settings → Secrets and variables → Actions → Add these secrets:

| Secret Name | Your Value |
|-------------|------------|
| ETHERSCAN_API | 38RB7BD5A69MEFXUP6DY5RJH7PK8K4BCGC |
| BSCSCAN_API | 60892e7f4b7a4ce39a20664cd3d19535 |
| TELEGRAM_BOT_TOKEN | 8741131861:AAFBi_tN505OlEDF-UEEKfr2fq-5XSXpivY |
| TELEGRAM_CHAT_ID | 6075712635 |
| FIREBASE_CONFIG | (Your Firebase config JSON as string) |
| FIREBASE_SERVICE_ACCOUNT | (Your service account JSON as string) |

### 3. Upload Files
Upload all files from this package to your GitHub repository

### 4. Run Scanner
- Go to Actions tab in GitHub
- The scanner runs automatically every 6 hours
- Or click "Run workflow" to run manually

### 5. View Results
- Open `frontend/index.html` in any browser
- Or host on GitHub Pages / Firebase Hosting

## Files Structure