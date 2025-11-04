# 🚀 START HERE - Complete Local Setup Guide

Welcome! This guide will help you run the Telegram Crypto Bot on your local computer in just **10 minutes**.

---

## 📺 Watch This Flow

```
1. Install Docker → 2. Get Bot Token → 3. Run Setup → 4. Test Bot → 5. Done! ✨
```

---

## 🎯 Three Ways to Get Started

Choose the method that suits you best:

### 🧙 Method 1: Setup Wizard (Recommended for Beginners)

**Easiest way - Interactive script guides you through everything!**

```bash
# Navigate to project folder
cd crypto-telegram-bot

# Run the wizard
./setup-wizard.sh
```

The wizard will:
- ✅ Check all requirements
- ✅ Guide you through configuration
- ✅ Start all services automatically
- ✅ Verify everything works
- ✅ Show you next steps

**Time: 5-10 minutes**

---

### ⚡ Method 2: Quick Start (For Experienced Users)

**Fast setup if you know Docker:**

```bash
# 1. Navigate to project
cd crypto-telegram-bot

# 2. Create .env file
cp .env.example .env

# 3. Edit .env and add your bot token
nano .env
# Add: TELEGRAM_BOT_TOKEN=your_token_from_botfather

# 4. Start everything
docker-compose up -d

# 5. Check status
docker-compose ps

# 6. View logs
docker-compose logs -f telegram-bot
```

**Time: 3-5 minutes**

---

### 📖 Method 3: Detailed Guide (Step-by-Step Tutorial)

**Complete walkthrough with explanations:**

Read: **`LOCAL_SETUP_GUIDE.md`**

This guide includes:
- Prerequisites explained
- Docker installation for all platforms
- Creating your Telegram bot
- Configuration details
- Testing procedures
- Troubleshooting solutions

**Time: 15-20 minutes (with reading)**

---

## 🔑 Getting Your Bot Token (Required)

**You need this before starting!**

1. Open **Telegram**
2. Search for **@BotFather**
3. Send: `/newbot`
4. Follow prompts:
   - Bot name: `My Crypto Bot` (any name)
   - Username: `my_crypto_analysis_bot` (must end with 'bot')
5. **Copy the token** (looks like: `1234567890:ABCdefGHI...`)
6. Keep it safe - you'll need it in the next step!

---

## 📦 What You'll Get

Once setup is complete, you'll have:

### 1. **Telegram Bot** 🤖
- Live crypto prices (Bitcoin, Ethereum, etc.)
- Market overview with top 10 cryptocurrencies
- Latest crypto news
- AI-powered analysis (Premium)
- Subscription system via Telegram Stars

### 2. **Admin Dashboard** 📊
Access: `http://localhost:3000`
- Monitor total users
- Track premium subscriptions
- View revenue
- See user activity

### 3. **Backend API** 🔌
Access: `http://localhost:8001/api/`
- RESTful API
- User management
- Subscription handling
- Bot statistics

### 4. **Database** 🗄️
Access: `mongodb://localhost:27017`
- MongoDB for data storage
- User profiles
- Subscription records
- Chat history

---

## ✅ Pre-Setup Checklist

Before starting, make sure you have:

- [ ] **Computer** (Windows, Mac, or Linux)
- [ ] **Docker Desktop** installed ([Get it here](https://www.docker.com/products/docker-desktop))
- [ ] **Telegram account**
- [ ] **Bot token** from @BotFather
- [ ] **Project files** in a folder
- [ ] **10 minutes** of time

---

## 🎬 Quick Start Video Script

*Follow these exact steps:*

### Step 1: Open Terminal
- **Mac**: Cmd+Space → type "Terminal"
- **Windows**: Win+R → type "powershell"
- **Linux**: Ctrl+Alt+T

### Step 2: Navigate to Project
```bash
cd /path/to/crypto-telegram-bot
```

### Step 3: Run Setup Wizard
```bash
./setup-wizard.sh
```

### Step 4: Follow Prompts
The wizard will ask you:
1. ✅ Verify Docker is installed
2. ✅ Check project files
3. ✅ Setup .env configuration
4. ✅ Enter your bot token
5. ✅ Optional: Add news API keys
6. ✅ Start all services
7. ✅ Verify everything works

### Step 5: Test Your Bot
1. Open Telegram
2. Search for your bot
3. Send `/start`
4. Try `/market` to see crypto prices

**Done! 🎉**

---

## 📱 Testing Your Bot

After setup, test these commands on Telegram:

### Free Features:
```
/start          → Welcome message
/market         → Top 10 crypto overview
/price BTC      → Bitcoin price
/price ETH      → Ethereum price
/news           → Latest crypto news
/status         → Check subscription
```

### Premium Features (requires subscription):
```
/analyze BTC    → AI-powered analysis
[Just message]  → Chat with AI assistant
```

---

## 🌐 Access Your Services

After running `docker-compose up -d`:

| Service | URL | What It Does |
|---------|-----|--------------|
| **Admin Dashboard** | http://localhost:3000 | Monitor users & revenue |
| **Backend API** | http://localhost:8001/api/ | REST API endpoint |
| **MongoDB** | mongodb://localhost:27017 | Database |
| **Bot on Telegram** | Search for your bot | User interface |

---

## 🔧 Common Commands

### View Logs (See What's Happening)
```bash
docker-compose logs -f
```

### Check Status (Are Services Running?)
```bash
docker-compose ps
```

### Restart Bot (After Config Changes)
```bash
docker-compose restart telegram-bot
```

### Stop Everything
```bash
docker-compose down
```

### Start Again
```bash
docker-compose up -d
```

---

## 🐛 Quick Troubleshooting

### "Bot not responding on Telegram"
```bash
docker-compose logs telegram-bot
docker-compose restart telegram-bot
```

### "Cannot connect to Docker"
- Make sure Docker Desktop is running
- Look for green icon in system tray

### "Port already in use"
```bash
# Find what's using port 3000
lsof -i :3000        # Mac/Linux
netstat -ano | findstr :3000   # Windows
```

### "Services keep restarting"
```bash
docker-compose logs --tail=100
# Look for error messages
```

---

## 📚 Full Documentation

Depending on your needs, check these guides:

### For Quick Reference:
📄 **`QUICK_REFERENCE.md`**
- Common commands
- Bot commands
- Quick fixes
- Configuration reference

### For Complete Setup Guide:
📄 **`LOCAL_SETUP_GUIDE.md`**
- Step-by-step tutorial
- Docker installation
- Telegram bot creation
- Testing procedures
- Troubleshooting

### For Docker Details:
📄 **`DOCKER_DEPLOYMENT.md`**
- Docker architecture
- Production deployment
- Scaling options
- Advanced configuration

### For Project Overview:
📄 **`README.md`**
- Feature list
- Architecture
- API documentation
- Development guide

### For Deployment Options:
📄 **`DEPLOYMENT_OPTIONS.md`**
- Emergent Platform vs Docker
- Cloud deployment
- Cost comparison

---

## 🎓 Learning Path

### Beginner Path:
1. Run `./setup-wizard.sh`
2. Test bot on Telegram
3. Check admin dashboard
4. Read `QUICK_REFERENCE.md` for commands

### Intermediate Path:
1. Read `LOCAL_SETUP_GUIDE.md`
2. Manually configure `.env`
3. Run `docker-compose up -d`
4. Explore Docker commands
5. Customize bot messages

### Advanced Path:
1. Read `DOCKER_DEPLOYMENT.md`
2. Modify `docker-compose.yml` for production
3. Set up monitoring
4. Configure backups
5. Deploy to cloud

---

## 🎯 What's Next?

After successful setup:

### 1. **Customize Your Bot**
Edit bot messages in:
- `backend/bot_service.py`

### 2. **Add News API Keys** (Optional)
Get better news coverage:
- CryptoPanic: https://cryptopanic.com/developers/api/
- NewsAPI: https://newsapi.org/

### 3. **Test Premium Features**
- Send `/subscribe` on Telegram
- Configure Telegram Stars payments

### 4. **Monitor Usage**
- Open dashboard: http://localhost:3000
- View user growth
- Track revenue

### 5. **Deploy to Production**
When ready:
- Use Emergent Platform (easiest)
- Deploy to your VPS
- Use cloud provider (AWS, Google Cloud)

---

## 💡 Tips & Best Practices

### For Development:
```bash
# Always check logs when something doesn't work
docker-compose logs -f telegram-bot

# Restart after code changes
docker-compose restart telegram-bot

# Rebuild after dependency changes
docker-compose up -d --build
```

### For Production:
```bash
# Use production config
docker-compose -f docker-compose.prod.yml up -d

# Set up backups
docker-compose exec mongodb mongodump --out=/backup

# Monitor resources
docker stats
```

### For Security:
- Keep `.env` file secure
- Never commit `.env` to git
- Use strong passwords in production
- Enable MongoDB authentication
- Set up SSL/HTTPS

---

## 🆘 Need Help?

### Check Logs First:
```bash
docker-compose logs -f
```

### Common Issues:
1. **Bot not responding** → Check token in `.env`
2. **Port conflicts** → Change ports in `docker-compose.yml`
3. **MongoDB errors** → Restart: `docker-compose restart mongodb`
4. **Build failures** → Clean rebuild: `docker-compose up -d --build`

### Documentation:
- `LOCAL_SETUP_GUIDE.md` - Complete walkthrough
- `QUICK_REFERENCE.md` - Command reference
- `DOCKER_DEPLOYMENT.md` - Docker details

### Still Stuck?
1. Check all logs: `docker-compose logs`
2. Verify config: `cat .env`
3. Check Docker: `docker-compose ps`
4. Review documentation above

---

## 🎉 Success Indicators

You're all set when you see:

- ✅ 4 services running (`docker-compose ps`)
- ✅ Backend API responding (http://localhost:8001/api/)
- ✅ Dashboard loading (http://localhost:3000)
- ✅ Bot responding on Telegram (`/start`)
- ✅ Market data working (`/market`)
- ✅ Your user in dashboard

---

## 🚀 Ready to Start?

### Choose Your Path:

**🧙 Beginner?** Run the wizard:
```bash
./setup-wizard.sh
```

**⚡ Experienced?** Quick start:
```bash
cp .env.example .env
nano .env  # Add bot token
docker-compose up -d
```

**📖 Want details?** Read the full guide:
```bash
cat LOCAL_SETUP_GUIDE.md
```

---

**🎊 That's it! Your Telegram Crypto Bot is ready to launch! 🎊**

Happy bot building! 🤖💰📈
