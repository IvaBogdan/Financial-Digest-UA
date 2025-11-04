# Quick Reference Guide - Telegram Crypto Bot

## 🚀 Quick Start

```bash
# 1. Copy project files to your computer
# 2. Create .env file
cp .env.example .env

# 3. Edit .env and add your bot token
nano .env

# 4. Start everything
docker-compose up -d

# 5. Check status
docker-compose ps
```

---

## 📱 Get Bot Token

1. Open Telegram → Search `@BotFather`
2. Send `/newbot`
3. Follow instructions
4. Copy token
5. Add to `.env` file: `TELEGRAM_BOT_TOKEN=your_token`

---

## 🎯 Access Points

| Service | URL | Description |
|---------|-----|-------------|
| **Admin Dashboard** | http://localhost:3000 | Monitor users & revenue |
| **Backend API** | http://localhost:8001/api/ | REST API endpoint |
| **MongoDB** | mongodb://localhost:27017 | Database |
| **Telegram Bot** | Search on Telegram | User interface |

---

## 🐳 Docker Commands

### Start Services
```bash
docker-compose up -d
```

### Stop Services
```bash
docker-compose down
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f telegram-bot
docker-compose logs -f backend

# Last 50 lines
docker-compose logs --tail=50
```

### Check Status
```bash
docker-compose ps
```

### Restart Service
```bash
# All services
docker-compose restart

# Specific service
docker-compose restart telegram-bot
docker-compose restart backend
```

### Rebuild After Changes
```bash
docker-compose up -d --build
```

### Clean Everything
```bash
# Stop and remove containers, networks
docker-compose down

# Also remove volumes (deletes database!)
docker-compose down -v
```

---

## 🤖 Bot Commands

### For Users on Telegram:

| Command | Description | Tier |
|---------|-------------|------|
| `/start` | Start bot & show menu | Free |
| `/help` | Show all commands | Free |
| `/market` | Top 10 crypto overview | Free |
| `/news` | Latest crypto news | Free |
| `/price BTC` | Get price of crypto | Free |
| `/status` | Check subscription | Free |
| `/analyze BTC` | AI analysis | Premium |
| `/subscribe` | Upgrade to premium | - |

### Premium Features ($5/month):
- Detailed AI-powered analysis
- Unlimited AI chat (just message the bot)
- Price predictions
- Personalized reports

---

## 🔧 Configuration (.env file)

```bash
# Required
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# AI (Pre-configured)
EMERGENT_LLM_KEY=sk-emergent-fC6934eD2A55986A6A

# Optional (for enhanced news)
CRYPTOPANIC_API_KEY=your_key
NEWSAPI_KEY=your_key
```

### Update Configuration:
```bash
# 1. Edit .env
nano .env

# 2. Restart services
docker-compose restart telegram-bot backend
```

---

## 🗄️ Database Commands

### Connect to MongoDB
```bash
docker-compose exec mongodb mongosh
```

### Inside MongoDB:
```javascript
// Switch to database
use crypto_bot_db

// View users
db.users.find().pretty()

// Count users
db.users.count()

// View subscriptions
db.subscriptions.find().pretty()

// View chat history
db.chat_history.find().pretty()

// Exit
exit
```

---

## 📊 Monitoring

### Check Service Health
```bash
docker-compose ps
```

### View Resource Usage
```bash
docker stats
```

### Check Disk Space
```bash
docker system df
```

### View Networks
```bash
docker network ls
```

### View Volumes
```bash
docker volume ls
```

---

## 🐛 Troubleshooting

### Bot Not Responding
```bash
# Check if running
docker-compose ps telegram-bot

# View logs
docker-compose logs telegram-bot

# Restart
docker-compose restart telegram-bot
```

### Connection Errors
```bash
# Check MongoDB
docker-compose ps mongodb
docker-compose logs mongodb

# Restart MongoDB
docker-compose restart mongodb
```

### Port Already in Use
```bash
# Find what's using port 3000
lsof -i :3000          # Mac/Linux
netstat -ano | findstr :3000   # Windows

# Change port in docker-compose.yml
# Or stop conflicting service
```

### Service Keeps Restarting
```bash
# Check logs for errors
docker-compose logs --tail=100

# Rebuild
docker-compose down
docker-compose up -d --build
```

### Cannot Connect to Docker
```bash
# Make sure Docker Desktop is running
# Or on Linux:
sudo systemctl start docker
```

---

## 🧪 Testing Checklist

```bash
# 1. Services running
docker-compose ps
# ✅ All should show "Up"

# 2. Backend responding
curl http://localhost:8001/api/
# ✅ Should return: {"message":"Crypto Analysis Bot API"}

# 3. Frontend loading
# ✅ Open http://localhost:3000 in browser

# 4. Bot responding
# ✅ Send /start on Telegram

# 5. Market data working
# ✅ Send /market on Telegram

# 6. Database working
docker-compose exec mongodb mongosh --eval "db.adminCommand('ping')"
# ✅ Should return: { ok: 1 }
```

---

## 📁 Important Files

```
app/
├── backend/
│   ├── bot_service.py       # Main bot logic
│   ├── crypto_service.py    # Market data
│   ├── news_service.py      # News aggregation
│   ├── ai_service.py        # AI analysis
│   ├── payment_service.py   # Subscriptions
│   └── server.py           # Backend API
├── frontend/
│   └── src/
│       └── pages/
│           └── Dashboard.jsx  # Admin UI
├── docker-compose.yml       # Docker config
├── .env                     # Your config
└── README.md               # Full docs
```

---

## 🔄 Update Workflow

### 1. Make Code Changes
Edit files in `backend/` or `frontend/`

### 2. Rebuild
```bash
docker-compose up -d --build
```

### 3. Test
```bash
# Check logs
docker-compose logs -f

# Test on Telegram
# Check dashboard
```

---

## 💾 Backup & Restore

### Backup Database
```bash
# Create backup
docker-compose exec mongodb mongodump --out=/backup

# Copy to host
docker cp crypto-bot-mongodb:/backup ./backup-$(date +%Y%m%d)
```

### Restore Database
```bash
# Copy backup to container
docker cp ./backup crypto-bot-mongodb:/backup

# Restore
docker-compose exec mongodb mongorestore /backup
```

---

## 🌐 Deploy to Production

### Option 1: Emergent Platform
```bash
# Use "Deploy" button in Emergent interface
# Configure environment variables in dashboard
```

### Option 2: Your Own Server
```bash
# Use production config
docker-compose -f docker-compose.prod.yml up -d
```

### Option 3: Cloud Provider
- AWS ECS, Google Cloud Run, Azure Container Instances
- Railway, Render, Fly.io
- See DOCKER_DEPLOYMENT.md for details

---

## 📞 Getting Help

### View Logs
```bash
docker-compose logs -f
```

### Check Configuration
```bash
cat .env
docker-compose config
```

### Test Connectivity
```bash
# Test backend
curl http://localhost:8001/api/

# Test MongoDB
docker-compose exec mongodb mongosh --eval "db.version()"
```

### Full Documentation
- `LOCAL_SETUP_GUIDE.md` - Complete setup guide
- `DOCKER_DEPLOYMENT.md` - Docker details
- `README.md` - Project overview
- `DEPLOYMENT_OPTIONS.md` - Deployment comparison

---

## 📈 Performance Tips

### View Resource Usage
```bash
docker stats
```

### Scale Services
```bash
# Run multiple bot instances
docker-compose up -d --scale telegram-bot=3
```

### Clean Up
```bash
# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Remove everything unused
docker system prune -a
```

---

## 🔑 Security Checklist

- [ ] Keep `.env` file secure (never commit to git)
- [ ] Use strong MongoDB password in production
- [ ] Enable HTTPS/SSL for production
- [ ] Regularly update dependencies
- [ ] Enable MongoDB authentication
- [ ] Use Docker secrets for sensitive data
- [ ] Set up firewall rules
- [ ] Regular backups

---

## 🎓 Learning Resources

- Docker Docs: https://docs.docker.com/
- Docker Compose: https://docs.docker.com/compose/
- Telegram Bot API: https://core.telegram.org/bots/api
- MongoDB: https://docs.mongodb.com/
- FastAPI: https://fastapi.tiangolo.com/

---

**Need more help?** See the full guides:
- Complete setup: `LOCAL_SETUP_GUIDE.md`
- Docker details: `DOCKER_DEPLOYMENT.md`
- Project info: `README.md`
