# After Pulling Changes - Quick Guide

If you've pulled new changes from the repository and Docker build fails, follow these steps:

---

## Quick Fix

```bash
# 1. Make sure you're in the project directory
cd /path/to/your/project

# 2. Clean old Docker stuff
docker-compose down
docker system prune -a

# 3. Make sure .env exists
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  Created .env - Please add your TELEGRAM_BOT_TOKEN!"
fi

# 4. Build and start
docker-compose up -d --build
```

---

## Common Issues After Pulling

### Issue 1: "yarn.lock not found"

**Error:**
```
failed to compute cache key: "/frontend/yarn.lock": not found
```

**Solution:**
This is normal if you don't have yarn.lock locally. The Dockerfile is now configured to work without it.

**Just rebuild:**
```bash
docker-compose build --no-cache frontend
docker-compose up -d
```

---

### Issue 2: ".env file missing"

**Error:**
```
WARNING: The TELEGRAM_BOT_TOKEN variable is not set
```

**Solution:**
```bash
# Create .env from template
cp .env.example .env

# Edit and add your token
nano .env
# or
code .env

# Add:
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

---

### Issue 3: "Port already in use"

**Error:**
```
bind: address already in use
```

**Solution:**
```bash
# Stop any running containers
docker-compose down

# Find what's using the ports
lsof -i :3000    # Frontend
lsof -i :8001    # Backend
lsof -i :27017   # MongoDB

# Kill the process or stop Docker containers
```

---

### Issue 4: Requirements changed

**Error:**
```
ModuleNotFoundError: No module named 'XXX'
```

**Solution:**
```bash
# Rebuild without cache
docker-compose build --no-cache backend telegram-bot
docker-compose up -d
```

---

## Complete Reset (If Nothing Works)

```bash
# 1. Stop everything
docker-compose down -v

# 2. Remove all related containers and images
docker rm -f $(docker ps -a -q --filter "name=crypto-bot") 2>/dev/null
docker rmi $(docker images 'financial-digest-ua*' -q) 2>/dev/null

# 3. Clean Docker system
docker system prune -a --volumes

# 4. Verify .env file exists
ls -la .env

# 5. Rebuild from scratch
docker-compose build --no-cache

# 6. Start services
docker-compose up -d

# 7. Check logs
docker-compose logs -f
```

---

## Verify After Pulling

### Step 1: Check what files changed
```bash
git status
git diff HEAD~1
```

### Step 2: Check if new dependencies added
```bash
# Check backend
git diff HEAD~1 backend/requirements.txt

# Check frontend  
git diff HEAD~1 frontend/package.json
```

### Step 3: Run pre-flight check
```bash
./pre-flight-check.sh
```

---

## Files You Should Have Locally

Essential files needed in your local project:

```
your-project/
├── docker-compose.yml          ✓ Required
├── Dockerfile.backend          ✓ Required
├── Dockerfile.bot              ✓ Required
├── Dockerfile.frontend         ✓ Required
├── .env                        ✓ Required (create from .env.example)
├── .env.example                ✓ Required
├── backend/
│   ├── requirements.txt        ✓ Required
│   ├── server.py              ✓ Required
│   ├── bot_service.py         ✓ Required
│   ├── crypto_service.py      ✓ Required
│   ├── news_service.py        ✓ Required
│   ├── ai_service.py          ✓ Required
│   └── payment_service.py     ✓ Required
├── frontend/
│   ├── package.json           ✓ Required
│   ├── yarn.lock              ⚠️ Optional (auto-generated)
│   └── src/                   ✓ Required
└── setup-wizard.sh            ✓ Helpful
```

---

## After Successful Build

### Verify everything works:

```bash
# 1. Check all services running
docker-compose ps

# 2. Test backend
curl http://localhost:8001/api/

# 3. Test frontend
curl http://localhost:3000

# 4. Check bot logs
docker-compose logs telegram-bot | tail -20

# 5. Open dashboard
open http://localhost:3000   # Mac
xdg-open http://localhost:3000   # Linux
start http://localhost:3000  # Windows
```

---

## Common Commands After Pulling

```bash
# View what changed
git log -p -1

# Pull latest changes
git pull

# Rebuild affected services
docker-compose up -d --build

# View logs
docker-compose logs -f

# Restart specific service
docker-compose restart telegram-bot

# Complete rebuild
docker-compose down
docker-compose up -d --build
```

---

## Understanding Your Project Structure

When you pull changes, these might be updated:

| File/Folder | What It Does | Impact |
|-------------|--------------|---------|
| `backend/requirements.txt` | Python packages | Rebuild backend & bot |
| `frontend/package.json` | Node packages | Rebuild frontend |
| `backend/*.py` | Python code | Restart services (hot reload) |
| `frontend/src/**` | React code | Restart frontend (hot reload) |
| `Dockerfile.*` | Build instructions | Rebuild all |
| `docker-compose.yml` | Service config | Restart all |
| `.env.example` | Config template | Update your .env |

---

## Troubleshooting Workflow

```
Pull Changes
    ↓
Does .env exist? → No → Copy from .env.example
    ↓ Yes
Run: docker-compose down
    ↓
Run: docker-compose build --no-cache
    ↓
Build Success? → No → Check error logs
    ↓ Yes            → See BUILD_ERRORS_FIXED.md
Run: docker-compose up -d
    ↓
All services Up? → No → Check docker-compose logs
    ↓ Yes             → Fix and restart
Test endpoints
    ↓
Working? → No → Check service logs
    ↓ Yes        → Restart specific service
Done! ✓
```

---

## Need Help?

1. **Check documentation:**
   - `BUILD_ERRORS_FIXED.md` - Common build errors
   - `DOCKER_TROUBLESHOOTING.md` - Runtime issues
   - `LOCAL_SETUP_GUIDE.md` - Complete setup

2. **Get debug info:**
   ```bash
   # System info
   docker version
   docker-compose version
   
   # Service status
   docker-compose ps
   
   # Recent logs
   docker-compose logs --tail=50
   ```

3. **Run pre-flight check:**
   ```bash
   ./pre-flight-check.sh
   ```

---

## Summary Checklist

After pulling changes:

- [ ] Pulled latest code: `git pull`
- [ ] Checked what changed: `git log -p -1`
- [ ] .env file exists with bot token
- [ ] Ran: `docker-compose down`
- [ ] Cleaned cache: `docker system prune -a`
- [ ] Rebuilt: `docker-compose build --no-cache`
- [ ] Started: `docker-compose up -d`
- [ ] Verified: `docker-compose ps` shows all "Up"
- [ ] Tested: Backend, Frontend, and Bot working

---

**Quick Start After Pull:**
```bash
docker-compose down && docker system prune -a -f && docker-compose up -d --build
```

That's it! Your local environment should now match the latest changes. 🚀
