# Complete Guide: Run Telegram Bot Locally with Docker

This is a **complete step-by-step guide** for beginners to run the Crypto Analysis Telegram Bot on your local computer using Docker.

---

## 📋 Prerequisites

Before starting, you need:

1. **A Computer** running:
   - Windows 10/11
   - macOS (Intel or Apple Silicon)
   - Linux (Ubuntu, Debian, etc.)

2. **Docker Desktop** installed
3. **A Telegram account**
4. **Basic command line knowledge** (we'll guide you!)

---

## Step 1: Install Docker Desktop

### For Windows:

1. Go to https://www.docker.com/products/docker-desktop
2. Download "Docker Desktop for Windows"
3. Run the installer
4. Follow the installation wizard
5. Restart your computer if prompted
6. Open Docker Desktop and wait for it to start (you'll see a green icon)

### For Mac:

1. Go to https://www.docker.com/products/docker-desktop
2. Download "Docker Desktop for Mac" (choose Intel or Apple Silicon)
3. Open the downloaded .dmg file
4. Drag Docker to Applications folder
5. Open Docker from Applications
6. Wait for Docker to start (green icon in menu bar)

### For Linux (Ubuntu/Debian):

```bash
# Update package index
sudo apt-get update

# Install Docker
sudo apt-get install docker.io docker-compose

# Start Docker
sudo systemctl start docker
sudo systemctl enable docker

# Add your user to docker group (to run without sudo)
sudo usermod -aG docker $USER

# Log out and log back in for changes to take effect
```

### Verify Docker Installation:

Open Terminal (Mac/Linux) or PowerShell (Windows) and run:

```bash
docker --version
docker-compose --version
```

You should see version numbers. If not, Docker is not installed correctly.

---

## Step 2: Get the Project Files

### Option A: If you have the code on Emergent

You need to download/copy all files from `/app/` directory to your local machine.

**Files you need:**
```
app/
├── backend/
│   ├── server.py
│   ├── bot_service.py
│   ├── crypto_service.py
│   ├── news_service.py
│   ├── ai_service.py
│   ├── payment_service.py
│   ├── requirements.txt
│   └── .env (will create this)
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ... (all React files)
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.bot
├── Dockerfile.frontend
├── .env.example
├── .dockerignore
└── docker-start.sh
```

### Option B: Create project folder manually

```bash
# Create project folder
mkdir crypto-telegram-bot
cd crypto-telegram-bot

# Copy all files from the Emergent workspace to this folder
```

For the rest of this guide, we'll assume your project is in a folder called `crypto-telegram-bot`.

---

## Step 3: Open Terminal/Command Prompt

### Windows:
- Press `Win + R`
- Type `powershell`
- Press Enter

### Mac:
- Press `Cmd + Space`
- Type `terminal`
- Press Enter

### Linux:
- Press `Ctrl + Alt + T`

### Navigate to project folder:

```bash
cd path/to/crypto-telegram-bot

# For example:
# Windows: cd C:\Users\YourName\Documents\crypto-telegram-bot
# Mac/Linux: cd ~/Documents/crypto-telegram-bot
```

Verify you're in the right folder:

```bash
# List files
ls        # Mac/Linux
dir       # Windows

# You should see: docker-compose.yml, backend/, frontend/, etc.
```

---

## Step 4: Create Your Telegram Bot

Now you need to create a bot on Telegram and get your bot token.

### 4.1: Open Telegram

- Open Telegram app on your phone or https://web.telegram.org

### 4.2: Find BotFather

1. In the search bar, type: `@BotFather`
2. Click on the verified BotFather bot (it has a blue checkmark)
3. Click "START" or send `/start`

### 4.3: Create New Bot

1. Send command: `/newbot`

2. BotFather will ask: **"Alright, a new bot. How are we going to call it?"**
   - Type your bot name (can be anything)
   - Example: `My Crypto Analysis Bot`

3. BotFather will ask: **"Good. Now let's choose a username for your bot."**
   - Must end with `bot`
   - Must be unique
   - Example: `my_crypto_analysis_bot` or `johncryptobot`

4. **SUCCESS!** BotFather will reply with:
   ```
   Done! Congratulations on your new bot...
   
   Use this token to access the HTTP API:
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz1234567
   
   Keep your token secure...
   ```

5. **COPY THIS TOKEN!** You'll need it in the next step.
   - Example token format: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz1234567`

### 4.4: Configure Bot Settings (Optional but Recommended)

Send these commands to BotFather to enable payments:

```
/mybots
[Select your bot]
Payments
Select a Provider → Connect Telegram Payments
```

This enables Telegram Stars for premium subscriptions.

---

## Step 5: Configure Environment Variables

### 5.1: Create .env file

In your terminal, in the project folder:

```bash
# Copy the example file
cp .env.example .env

# For Windows:
copy .env.example .env
```

### 5.2: Edit .env file

Open `.env` file with any text editor:

```bash
# Mac/Linux:
nano .env
# or
vim .env
# or open with your favorite editor

# Windows:
notepad .env
```

### 5.3: Add Your Bot Token

Find this line:
```bash
TELEGRAM_BOT_TOKEN=
```

Add your token after the `=`:
```bash
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz1234567
```

**IMPORTANT:** 
- No spaces around `=`
- No quotes needed
- Keep it on one line

### 5.4: Check Other Settings

Your `.env` file should look like this:

```bash
# Emergent LLM Key (Already configured - DO NOT CHANGE)
EMERGENT_LLM_KEY=sk-emergent-fC6934eD2A55986A6A

# Your Telegram Bot Token (REQUIRED - ADD THIS)
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz1234567

# Optional: News API Keys (Leave empty for now)
CRYPTOPANIC_API_KEY=
NEWSAPI_KEY=
```

### 5.5: Save the file

- **Nano**: Press `Ctrl+X`, then `Y`, then `Enter`
- **Vim**: Press `Esc`, type `:wq`, press `Enter`
- **Notepad**: Click File → Save

---

## Step 6: Start Docker Services

### 6.1: Make sure Docker Desktop is running

- Windows/Mac: Check if Docker Desktop icon shows a green status
- Linux: Run `sudo systemctl status docker`

### 6.2: Start all services

In your terminal, in the project folder:

```bash
docker-compose up -d
```

**What this does:**
- `docker-compose`: Uses Docker Compose to manage multiple services
- `up`: Start the services
- `-d`: Run in background (detached mode)

### 6.3: Wait for services to start

This will take 2-5 minutes the first time (downloading images and building).

You'll see output like:
```
Creating network "crypto-telegram-bot_crypto-bot-network" ... done
Creating volume "crypto-telegram-bot_mongodb_data" ... done
Creating crypto-bot-mongodb ... done
Creating crypto-bot-backend ... done
Creating crypto-bot-telegram ... done
Creating crypto-bot-frontend ... done
```

---

## Step 7: Verify Services Are Running

### 7.1: Check status

```bash
docker-compose ps
```

You should see 4 services running (State = "Up"):
```
NAME                    STATUS    PORTS
crypto-bot-mongodb      Up        0.0.0.0:27017->27017/tcp
crypto-bot-backend      Up        0.0.0.0:8001->8001/tcp
crypto-bot-telegram     Up
crypto-bot-frontend     Up        0.0.0.0:3000->3000/tcp
```

### 7.2: Check logs

```bash
# View all logs
docker-compose logs

# View last 50 lines
docker-compose logs --tail=50

# Follow logs in real-time
docker-compose logs -f

# View only bot logs
docker-compose logs -f telegram-bot
```

**Look for:**
- ✅ "Bot started successfully" in telegram-bot logs
- ✅ No error messages
- ✅ "Application startup complete" in backend logs

### 7.3: Test Backend API

Open your web browser or use curl:

```bash
# Browser: http://localhost:8001/api/

# Or in terminal:
curl http://localhost:8001/api/
```

You should see:
```json
{"message":"Crypto Analysis Bot API"}
```

### 7.4: Test Admin Dashboard

Open your web browser:
```
http://localhost:3000
```

You should see the Crypto Bot Dashboard with:
- Total Users: 0
- Premium Users: 0
- Free Users: 0
- Total Revenue: $0

---

## Step 8: Test Your Telegram Bot

### 8.1: Find Your Bot on Telegram

1. Open Telegram
2. Search for your bot username (e.g., `@my_crypto_analysis_bot`)
3. Click on your bot
4. Click "START" button or send `/start`

### 8.2: Test Commands

Try these commands one by one:

#### 1. Start the bot
```
/start
```
You should see a welcome message with buttons.

#### 2. Get help
```
/help
```
Shows all available commands.

#### 3. Check market overview (FREE)
```
/market
```
You should see:
- Total market cap
- BTC dominance
- Top 10 cryptocurrencies with prices

**Expected output:**
```
📊 Market Overview

💰 Total Market Cap: $2,500,000,000,000
📈 24h Volume: $95,000,000,000
₿ BTC Dominance: 54.2%

🔝 Top 10 Cryptocurrencies:

1. Bitcoin (BTC)
   💵 $67,850.45 | 🟢 +2.34% (24h) | +8.12% (7d)
...
```

#### 4. Get news (FREE)
```
/news
```
Shows latest crypto news (may be limited without API keys).

#### 5. Check a specific price (FREE)
```
/price BTC
```
Shows Bitcoin price, market cap, volume, and 24h change.

Try other cryptos:
```
/price ETH
/price SOL
/price DOGE
```

#### 6. Check subscription status
```
/status
```
Shows your current subscription tier (Free by default).

#### 7. Test Premium Features

Try to analyze an asset:
```
/analyze BTC
```

You should get a message:
```
⭐ This is a premium feature. Please subscribe using /subscribe to access detailed analysis.
```

#### 8. Test Payment (Optional)

```
/subscribe
```

This will show you the payment options via Telegram Stars.

**Note:** To actually test payments:
- You need Telegram Stars (can buy in Telegram)
- Bot payments must be enabled via BotFather
- Use test mode for development

---

## Step 9: Monitor Your Bot

### 9.1: View Real-Time Logs

In terminal:
```bash
docker-compose logs -f telegram-bot
```

You'll see every interaction:
- User commands
- Bot responses
- Errors (if any)

Press `Ctrl+C` to stop viewing logs.

### 9.2: Check Admin Dashboard

Open: http://localhost:3000

After testing the bot:
- Total Users should be 1 (you!)
- Your user info should appear in the Users tab

### 9.3: Check Database

```bash
# Connect to MongoDB
docker-compose exec mongodb mongosh

# In MongoDB shell:
use crypto_bot_db
db.users.find().pretty()
db.subscriptions.find().pretty()

# Exit MongoDB
exit
```

---

## Step 10: Stopping and Starting

### Stop all services:
```bash
docker-compose down
```

### Start again:
```bash
docker-compose up -d
```

### Restart a specific service:
```bash
docker-compose restart telegram-bot
```

### Stop but keep data:
```bash
docker-compose stop
```

### Remove everything (including database):
```bash
docker-compose down -v
```

---

## Troubleshooting

### Problem: Bot doesn't respond on Telegram

**Solution 1:** Check if bot service is running
```bash
docker-compose ps telegram-bot
```

**Solution 2:** Check bot logs
```bash
docker-compose logs telegram-bot
```

**Solution 3:** Verify token in .env
```bash
cat .env | grep TELEGRAM_BOT_TOKEN
```

**Solution 4:** Restart bot
```bash
docker-compose restart telegram-bot
```

### Problem: "Connection refused" errors

**Solution:** Make sure MongoDB is healthy
```bash
docker-compose ps mongodb
docker-compose logs mongodb
```

### Problem: Port already in use (3000, 8001, or 27017)

**Solution:** Stop conflicting service or change port

Find what's using the port:
```bash
# Mac/Linux:
lsof -i :3000
lsof -i :8001

# Windows:
netstat -ano | findstr :3000
```

Kill the process or edit `docker-compose.yml` to use different ports.

### Problem: Docker says "Cannot connect to Docker daemon"

**Solution:** 
- Make sure Docker Desktop is running
- On Linux: `sudo systemctl start docker`

### Problem: Services keep restarting

**Solution:** Check logs for errors
```bash
docker-compose logs --tail=100
```

### Problem: "Module not found" errors in logs

**Solution:** Rebuild containers
```bash
docker-compose down
docker-compose up -d --build
```

### Problem: Bot works but no market data

**Solution:** CoinGecko API might be rate-limited. Wait a few minutes and try again.

### Problem: No news showing

**Solution:** News APIs are optional. To get full news:
1. Sign up at https://cryptopanic.com/developers/api/
2. Sign up at https://newsapi.org/
3. Add keys to `.env`
4. Restart: `docker-compose restart telegram-bot`

---

## Advanced: Adding News API Keys

### 1. Get CryptoPanic API Key

1. Go to https://cryptopanic.com/developers/api/
2. Sign up for free account
3. Copy your API key

### 2. Get NewsAPI Key

1. Go to https://newsapi.org/
2. Register for free account
3. Copy your API key

### 3. Add to .env

Edit `.env`:
```bash
CRYPTOPANIC_API_KEY=your_cryptopanic_key_here
NEWSAPI_KEY=your_newsapi_key_here
```

### 4. Restart services

```bash
docker-compose restart telegram-bot backend
```

### 5. Test news

In Telegram: `/news`

You should now see more news articles!

---

## Testing Checklist

✅ Docker Desktop is running  
✅ All 4 services are up (`docker-compose ps`)  
✅ Backend API responds (http://localhost:8001/api/)  
✅ Admin dashboard loads (http://localhost:3000)  
✅ Bot responds on Telegram (`/start`)  
✅ Market data works (`/market`)  
✅ Price check works (`/price BTC`)  
✅ News works (`/news`)  
✅ User appears in dashboard  
✅ Subscription check works (`/status`)  
✅ Premium features require subscription (`/analyze BTC`)  

---

## Next Steps

### 1. Customize Your Bot

Edit the bot messages in:
- `/app/backend/bot_service.py`

After changes:
```bash
docker-compose up -d --build
```

### 2. Enable Payments

Configure Telegram Stars via BotFather for premium subscriptions.

### 3. Deploy to Production

When ready, deploy to:
- Emergent Platform (easiest)
- Your own VPS (DigitalOcean, AWS, etc.)
- Cloud provider (AWS ECS, Google Cloud Run)

### 4. Monitor Usage

Check the dashboard regularly:
- http://localhost:3000

### 5. Set Up Daily Digest

The bot automatically sends daily digest at 9 AM UTC.

To change time, edit `bot_service.py`:
```python
job_queue.run_daily(
    self.schedule_daily_tasks,
    time=datetime.strptime("09:00", "%H:%M").time()  # Change this
)
```

---

## Summary

You now have:
- ✅ Telegram bot running locally
- ✅ Admin dashboard to monitor users
- ✅ Database storing all data
- ✅ AI-powered analysis (via Emergent LLM)
- ✅ Real-time crypto market data
- ✅ News aggregation
- ✅ Payment system ready (Telegram Stars)

**Key URLs:**
- Admin Dashboard: http://localhost:3000
- Backend API: http://localhost:8001/api/
- MongoDB: mongodb://localhost:27017

**Key Commands:**
```bash
docker-compose up -d        # Start
docker-compose down         # Stop
docker-compose logs -f      # View logs
docker-compose ps          # Check status
docker-compose restart     # Restart
```

---

## Getting Help

If you encounter issues:

1. **Check logs**: `docker-compose logs -f telegram-bot`
2. **Verify configuration**: `cat .env`
3. **Check service status**: `docker-compose ps`
4. **Restart services**: `docker-compose restart`
5. **Rebuild if needed**: `docker-compose up -d --build`

For more help, see:
- `DOCKER_DEPLOYMENT.md` - Full Docker guide
- `README.md` - Complete project documentation
- `DEPLOYMENT_OPTIONS.md` - Deployment alternatives

---

**Congratulations! Your Telegram Crypto Bot is running locally! 🎉**
