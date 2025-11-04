# Docker Build & Runtime Troubleshooting Guide

This guide helps you solve common Docker issues when setting up the Telegram Crypto Bot.

---

## 🔧 Build Errors

### Error: "pip install failed" or "requirements.txt error"

**Symptoms:**
```
=> ERROR [5/6] RUN pip install --no-cache-dir -r requirements.txt
```

**Solution 1: Clean rebuild**
```bash
# Remove old images and containers
docker-compose down
docker system prune -a

# Rebuild from scratch
docker-compose build --no-cache
docker-compose up -d
```

**Solution 2: Check requirements.txt**
```bash
# View the file
cat backend/requirements.txt

# Make sure it's not corrupted
# Should have format: package==version
```

**Solution 3: Build with verbose output**
```bash
docker-compose build --progress=plain
# This shows detailed error messages
```

---

### Error: "Cannot find module" or "ImportError"

**Symptoms:**
```
ModuleNotFoundError: No module named 'telegram'
ImportError: cannot import name 'LlmChat'
```

**Solution:**
```bash
# Rebuild containers
docker-compose build --no-cache telegram-bot backend

# Restart
docker-compose up -d
```

---

### Error: "Context canceled" or "Build timeout"

**Symptoms:**
```
=> ERROR [internal] load metadata for docker.io/library/python:3.11-slim
```

**Solution:**
```bash
# Check Docker daemon
docker info

# Restart Docker Desktop
# Then try again
docker-compose up -d --build
```

---

### Error: "COPY failed" or "no such file or directory"

**Symptoms:**
```
=> ERROR [5/6] COPY backend/requirements.txt .
```

**Solution:**
```bash
# Make sure you're in the project root directory
pwd
ls -la

# You should see:
# - docker-compose.yml
# - backend/
# - frontend/

# If not, navigate to the correct directory
cd /path/to/crypto-telegram-bot
```

---

## 🐛 Runtime Errors

### Error: "Connection refused" to MongoDB

**Symptoms:**
```
pymongo.errors.ServerSelectionTimeoutError: localhost:27017
Connection refused
```

**Solution:**
```bash
# Check if MongoDB is running
docker-compose ps mongodb

# View MongoDB logs
docker-compose logs mongodb

# Restart MongoDB
docker-compose restart mongodb

# Wait 10 seconds then restart dependent services
sleep 10
docker-compose restart backend telegram-bot
```

---

### Error: "Port already in use"

**Symptoms:**
```
Error starting userland proxy: listen tcp4 0.0.0.0:3000: bind: address already in use
```

**Solution 1: Find and kill process**
```bash
# Find what's using the port
lsof -i :3000        # Mac/Linux
netstat -ano | findstr :3000   # Windows

# Kill the process
kill -9 <PID>        # Mac/Linux
taskkill /PID <PID> /F   # Windows
```

**Solution 2: Change port in docker-compose.yml**
```yaml
# Edit docker-compose.yml
frontend:
  ports:
    - "3001:3000"  # Changed from 3000:3000
```

---

### Error: Bot not responding on Telegram

**Symptoms:**
- Bot doesn't reply to commands
- No response to /start

**Solution:**
```bash
# 1. Check bot logs
docker-compose logs -f telegram-bot

# 2. Check if token is set
docker-compose exec telegram-bot env | grep TELEGRAM_BOT_TOKEN

# 3. Verify token format (should be: 1234567890:ABCdef...)
cat .env | grep TELEGRAM_BOT_TOKEN

# 4. Restart bot
docker-compose restart telegram-bot

# 5. Check if bot is running
docker-compose ps telegram-bot
```

---

### Error: "Cannot connect to Docker daemon"

**Symptoms:**
```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock
```

**Solution:**

**Mac/Windows:**
- Open Docker Desktop
- Wait for it to start (green icon)
- Try again

**Linux:**
```bash
# Start Docker service
sudo systemctl start docker

# Enable on boot
sudo systemctl enable docker

# Add user to docker group
sudo usermod -aG docker $USER

# Log out and log back in
```

---

### Error: Services keep restarting

**Symptoms:**
```bash
docker-compose ps
# Shows "Restarting" status
```

**Solution:**
```bash
# Check logs for errors
docker-compose logs --tail=100

# Common causes:
# 1. MongoDB not ready - wait longer
# 2. Missing environment variables
# 3. Port conflicts
# 4. Code errors

# Fix and restart
docker-compose down
docker-compose up -d
```

---

## 🗄️ Database Issues

### Error: MongoDB not starting

**Solution:**
```bash
# Remove volume and restart
docker-compose down -v
docker-compose up -d

# Check logs
docker-compose logs mongodb

# Test connection
docker-compose exec mongodb mongosh --eval "db.version()"
```

---

### Error: Database connection timeout

**Solution:**
```bash
# Check network
docker network ls
docker network inspect crypto-telegram-bot_crypto-bot-network

# Restart all services in order
docker-compose down
docker-compose up -d mongodb
sleep 10
docker-compose up -d backend telegram-bot frontend
```

---

## 📦 Image Issues

### Error: "No space left on device"

**Solution:**
```bash
# Check Docker disk usage
docker system df

# Clean up
docker system prune -a
docker volume prune

# Remove unused images
docker image prune -a
```

---

### Error: "failed to solve with frontend dockerfile.v0"

**Solution:**
```bash
# Update Docker Desktop to latest version
# Or try legacy builder
DOCKER_BUILDKIT=0 docker-compose build
```

---

## 🌐 Network Issues

### Error: "Cannot reach backend from frontend"

**Solution:**
```bash
# Check if all containers are on same network
docker network inspect crypto-telegram-bot_crypto-bot-network

# Restart network
docker-compose down
docker-compose up -d
```

---

### Error: DNS resolution failed

**Solution:**
```bash
# Add to docker-compose.yml under each service:
dns:
  - 8.8.8.8
  - 8.8.4.4
```

---

## 🔐 Permission Issues

### Error: "Permission denied" on Linux

**Solution:**
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Log out and log back in

# Or run with sudo (not recommended)
sudo docker-compose up -d
```

---

### Error: "Cannot write to volume"

**Solution:**
```bash
# Check volume permissions
docker volume inspect app_mongodb_data

# Remove and recreate
docker-compose down -v
docker-compose up -d
```

---

## 🧹 Complete Clean Reset

If nothing works, try a complete reset:

```bash
# 1. Stop everything
docker-compose down -v

# 2. Remove all related containers
docker rm -f $(docker ps -a -q --filter "name=crypto-bot")

# 3. Remove all images
docker rmi $(docker images 'app_*' -q)

# 4. Clean system
docker system prune -a --volumes

# 5. Verify .env file
cat .env

# 6. Rebuild from scratch
docker-compose build --no-cache

# 7. Start services
docker-compose up -d

# 8. Watch logs
docker-compose logs -f
```

---

## 🔍 Debugging Commands

### Check service status
```bash
docker-compose ps
```

### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f telegram-bot
docker-compose logs -f backend
docker-compose logs -f mongodb

# Last 50 lines
docker-compose logs --tail=50

# Since specific time
docker-compose logs --since 5m
```

### Inspect container
```bash
# Get container details
docker inspect crypto-bot-telegram

# Check environment variables
docker-compose exec telegram-bot env

# Get into container shell
docker-compose exec telegram-bot /bin/bash
```

### Check resources
```bash
# Resource usage
docker stats

# Disk usage
docker system df

# Network details
docker network ls
docker network inspect crypto-telegram-bot_crypto-bot-network
```

### Test connectivity
```bash
# Test MongoDB from backend
docker-compose exec backend curl mongodb:27017

# Test backend API
curl http://localhost:8001/api/

# Test frontend
curl http://localhost:3000
```

---

## 🆘 Getting More Help

### 1. Collect Information
```bash
# System info
docker version
docker-compose version
uname -a  # Linux/Mac
systeminfo  # Windows

# Service status
docker-compose ps

# Recent logs
docker-compose logs --tail=100 > logs.txt
```

### 2. Check Configuration
```bash
# Verify docker-compose.yml syntax
docker-compose config

# Check .env file
cat .env

# List volumes
docker volume ls

# List networks
docker network ls
```

### 3. Common Diagnostic Steps

**Step 1: Verify files exist**
```bash
ls -la docker-compose.yml
ls -la backend/requirements.txt
ls -la backend/bot_service.py
```

**Step 2: Check Docker is running**
```bash
docker info
```

**Step 3: Test basic Docker functionality**
```bash
docker run hello-world
```

**Step 4: Check ports are free**
```bash
lsof -i :3000
lsof -i :8001
lsof -i :27017
```

---

## 📚 Additional Resources

- Docker Docs: https://docs.docker.com/
- Docker Compose: https://docs.docker.com/compose/
- Python Telegram Bot: https://python-telegram-bot.org/
- MongoDB Docker: https://hub.docker.com/_/mongo

---

## ✅ Success Checklist

After fixing issues, verify:

- [ ] `docker-compose ps` shows all 4 services as "Up"
- [ ] `curl http://localhost:8001/api/` returns JSON
- [ ] `curl http://localhost:3000` returns HTML
- [ ] `docker-compose logs telegram-bot` shows "Bot started"
- [ ] Bot responds to `/start` on Telegram
- [ ] No error messages in logs
- [ ] Dashboard loads at http://localhost:3000

---

**Still having issues?** 
1. Review the complete logs: `docker-compose logs > full_logs.txt`
2. Check QUICK_REFERENCE.md for common commands
3. See LOCAL_SETUP_GUIDE.md for step-by-step setup
