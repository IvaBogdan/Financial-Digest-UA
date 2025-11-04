# Crypto Bot - Deployment Options Guide

This guide explains **two ways** to deploy your Telegram Crypto Analysis Bot.

---

## Option 1: Deploy on Emergent Platform (Recommended)

### Advantages:
- ✅ One-click deployment
- ✅ 24/7 uptime with auto-restart
- ✅ Managed infrastructure
- ✅ No server management needed
- ✅ Easy configuration updates
- ✅ Built-in monitoring

### How to Deploy:

1. **Test First (Preview Mode)**
   - Click "Preview" button in your chat
   - Test all bot features
   - Make sure everything works

2. **Deploy to Production**
   - Click "Deploy" button in chat interface
   - Wait ~10 minutes for deployment
   - Get your production URL

3. **Configure Environment Variables**
   - Go to Home → Deployments
   - Select your bot deployment
   - Click "Environment Variables"
   - Add/Update:
     - `TELEGRAM_BOT_TOKEN` (from @BotFather)
     - `CRYPTOPANIC_API_KEY` (optional)
     - `NEWSAPI_KEY` (optional)
   - `EMERGENT_LLM_KEY` is already configured

4. **Update Bot Token on Telegram**
   - Your bot needs the token in environment variables
   - Changes apply immediately without redeployment

### Cost:
- 50 credits per month per deployed app
- Includes hosting, database, and infrastructure

### Configuration Management:
- **Easy Updates**: Change any environment variable anytime
- **No Downtime**: Updates apply without restart
- **Secure Storage**: All API keys encrypted
- **Access Method**: Home → Deployments → Your App → Environment Variables

### Best For:
- Quick deployment
- Production use
- No DevOps experience needed
- Want managed infrastructure

---

## Option 2: Deploy Locally with Docker

### Advantages:
- ✅ Full control over infrastructure
- ✅ Run on your own server/computer
- ✅ No ongoing hosting costs
- ✅ Easy to test locally
- ✅ Can deploy to any cloud provider

### Prerequisites:
- Docker Desktop installed ([download here](https://www.docker.com/products/docker-desktop))
- Docker Compose installed (included with Docker Desktop)
- Terminal/Command line access

### Quick Start:

```bash
# 1. Navigate to project directory
cd /path/to/app

# 2. Copy environment template
cp .env.example .env

# 3. Edit .env and add your tokens
nano .env  # or use any text editor

# 4. Run the startup script
./docker-start.sh

# OR manually:
docker-compose up -d
```

### What Gets Deployed:

The Docker setup includes **4 services**:

1. **MongoDB** (Port 27017)
   - Database for users and subscriptions
   - Persistent data storage

2. **Backend API** (Port 8001)
   - FastAPI REST API
   - Serves admin dashboard

3. **Telegram Bot** (No exposed port)
   - Runs your Telegram bot
   - Handles user interactions

4. **Frontend Dashboard** (Port 3000)
   - React admin interface
   - Monitor users and revenue

### Configuration (.env file):

```bash
# Required: Get from @BotFather
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Pre-configured for AI features
EMERGENT_LLM_KEY=sk-emergent-fC6934eD2A55986A6A

# Optional: Enhanced news features
CRYPTOPANIC_API_KEY=your_key
NEWSAPI_KEY=your_key
```

### Access Your Application:

After starting (`docker-compose up -d`):

- **Admin Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8001/api/
- **MongoDB**: mongodb://localhost:27017
- **Telegram Bot**: Search on Telegram

### Common Commands:

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
docker-compose logs -f telegram-bot

# Stop all services
docker-compose down

# Restart a service
docker-compose restart telegram-bot

# Rebuild after code changes
docker-compose up -d --build

# Stop and remove everything
docker-compose down -v
```

### Production Deployment:

For production with optimizations:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

Production features:
- Nginx for frontend (port 80)
- Multiple backend workers
- Better logging
- Automatic restarts
- Optimized builds

### Deploy to Cloud:

This Docker setup works on:
- **VPS**: DigitalOcean, Linode, AWS EC2, Vultr
- **Cloud**: AWS ECS, Google Cloud Run, Azure
- **PaaS**: Railway, Render, Fly.io

### Updating Configuration:

```bash
# 1. Edit .env file
nano .env

# 2. Restart affected services
docker-compose restart telegram-bot backend
```

### Best For:
- Local development/testing
- Self-hosted deployment
- Full infrastructure control
- Deploy to your own cloud

---

## Comparison Table

| Feature | Emergent Platform | Docker (Self-Hosted) |
|---------|------------------|---------------------|
| **Setup Time** | 10 minutes | 15-30 minutes |
| **Ease of Use** | Very Easy (1-click) | Moderate (technical) |
| **Cost** | 50 credits/month | Server costs only |
| **Maintenance** | Managed | Self-managed |
| **Uptime** | 24/7 automatic | Depends on hosting |
| **Updates** | Easy (no code needed) | Manual restart needed |
| **Monitoring** | Built-in | Setup required |
| **Scaling** | Automatic | Manual |
| **SSL/HTTPS** | Included | Setup required |
| **Backups** | Automatic | Setup required |
| **Support** | Platform support | Self-support |

---

## Getting Your Bot Token (Both Options)

1. Open Telegram
2. Search for **@BotFather**
3. Send `/newbot` command
4. Choose a name (e.g., "Crypto Analysis Bot")
5. Choose username (must end with "bot", e.g., "my_crypto_bot")
6. Copy the token provided
7. Add to `.env` file or Emergent environment variables

---

## Optional API Keys

### CryptoPanic (Crypto News)
- Sign up: https://cryptopanic.com/developers/api/
- Free tier: 500 requests/month
- Add to: `CRYPTOPANIC_API_KEY`

### NewsAPI (Financial News)
- Sign up: https://newsapi.org/
- Free tier: 100 requests/day
- Add to: `NEWSAPI_KEY`

**Note**: Bot works without these, but with limited news features.

---

## Troubleshooting

### Emergent Platform:
- Check deployment logs in dashboard
- Verify environment variables are set
- Use Preview mode to test first

### Docker:
```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs -f telegram-bot

# Test MongoDB
docker-compose exec mongodb mongosh

# Restart services
docker-compose restart
```

---

## Which Option Should You Choose?

### Choose Emergent Platform if you:
- Want fastest deployment
- Prefer managed infrastructure
- Don't want to manage servers
- Need reliable 24/7 uptime
- Want easy configuration updates

### Choose Docker if you:
- Want to test locally first
- Have your own server/VPS
- Need full infrastructure control
- Want to minimize hosting costs
- Have DevOps experience

---

## Need Help?

- **Emergent Platform**: Contact support through platform
- **Docker Issues**: See `DOCKER_DEPLOYMENT.md` for detailed guide
- **Bot Issues**: Check logs and README.md

Both deployment methods are fully supported and production-ready!
