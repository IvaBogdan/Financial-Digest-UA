# Docker Deployment Guide for Crypto Analysis Bot

Complete guide to deploy the Telegram bot locally or on your own infrastructure using Docker.

## Quick Start (Development)

### Prerequisites
- Docker Desktop installed (https://www.docker.com/products/docker-desktop)
- Docker Compose installed (included with Docker Desktop)
- Telegram Bot Token from @BotFather

### Setup Steps

1. **Clone/Copy the project** to your local machine

2. **Create environment file**:
   ```bash
   cp .env.example .env
   ```

3. **Edit .env file** and add your tokens:
   ```bash
   nano .env  # or use any text editor
   ```
   
   Required:
   - `TELEGRAM_BOT_TOKEN` - Get from @BotFather on Telegram
   
   Optional (already configured):
   - `EMERGENT_LLM_KEY` - Already set for AI features
   - `CRYPTOPANIC_API_KEY` - For crypto news
   - `NEWSAPI_KEY` - For financial news

4. **Start all services**:
   ```bash
   docker-compose up -d
   ```

5. **Check logs**:
   ```bash
   # All services
   docker-compose logs -f
   
   # Specific service
   docker-compose logs -f telegram-bot
   docker-compose logs -f backend
   docker-compose logs -f frontend
   ```

6. **Access the application**:
   - Frontend Dashboard: http://localhost:3000
   - Backend API: http://localhost:8001/api/
   - MongoDB: mongodb://localhost:27017
   - Telegram Bot: Search for your bot on Telegram

## Production Deployment

For production deployment with optimizations:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

Production features:
- Optimized builds
- Multiple workers
- Nginx for frontend
- Better logging
- Automatic restarts

## Common Commands

### Start services
```bash
docker-compose up -d
```

### Stop services
```bash
docker-compose down
```

### Restart a service
```bash
docker-compose restart telegram-bot
```

### View logs
```bash
# All logs
docker-compose logs -f

# Specific service
docker-compose logs -f telegram-bot

# Last 100 lines
docker-compose logs --tail=100 telegram-bot
```

### Rebuild after code changes
```bash
docker-compose up -d --build
```

### Stop and remove everything (including volumes)
```bash
docker-compose down -v
```

## Service Architecture

### Services Included:

1. **mongodb** (Port 27017)
   - Database for users, subscriptions, chat history
   - Persistent volume for data
   - Health checks enabled

2. **backend** (Port 8001)
   - FastAPI REST API
   - Admin dashboard backend
   - Health checks enabled

3. **telegram-bot** (No exposed port)
   - Runs the Telegram bot
   - Polls Telegram for messages
   - Handles user interactions

4. **frontend** (Port 3000 or 80)
   - React admin dashboard
   - Development: Port 3000
   - Production: Port 80 with Nginx

## Environment Variables

### Required:
```bash
TELEGRAM_BOT_TOKEN=     # From @BotFather
```

### Pre-configured:
```bash
EMERGENT_LLM_KEY=sk-emergent-fC6934eD2A55986A6A
```

### Optional (Enhanced Features):
```bash
CRYPTOPANIC_API_KEY=    # Crypto news (cryptopanic.com/developers/api/)
NEWSAPI_KEY=            # Financial news (newsapi.org)
```

## Troubleshooting

### Bot not starting
```bash
# Check logs
docker-compose logs telegram-bot

# Verify token is set
docker-compose exec telegram-bot env | grep TELEGRAM
```

### MongoDB connection issues
```bash
# Check MongoDB health
docker-compose ps

# Test MongoDB connection
docker-compose exec mongodb mongosh --eval "db.runCommand('ping')"
```

### Port already in use
```bash
# Find what's using the port
sudo lsof -i :3000  # or :8001, :27017

# Kill the process or change port in docker-compose.yml
```

### Rebuild from scratch
```bash
# Stop everything
docker-compose down -v

# Remove images
docker-compose down --rmi all

# Rebuild and start
docker-compose up -d --build
```

## Data Persistence

MongoDB data is stored in a Docker volume:
```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect app_mongodb_data

# Backup database
docker-compose exec mongodb mongodump --out=/backup
```

## Scaling

### Run multiple bot instances:
```bash
docker-compose up -d --scale telegram-bot=3
```

### Increase backend workers:
Edit `docker-compose.prod.yml`:
```yaml
command: uvicorn server:app --host 0.0.0.0 --port 8001 --workers 4
```

## Network

All services communicate via a bridge network:
- Service names are DNS resolvable (e.g., `mongodb`, `backend`)
- Internal communication doesn't require exposed ports

## Production Checklist

- [ ] Set strong MongoDB password (uncomment in docker-compose.prod.yml)
- [ ] Configure CORS_ORIGINS with your domain
- [ ] Set up SSL/TLS (use reverse proxy like Traefik or Caddy)
- [ ] Enable MongoDB authentication
- [ ] Set up monitoring (Prometheus + Grafana)
- [ ] Configure log rotation
- [ ] Set up backups for MongoDB
- [ ] Use secrets management (Docker Secrets or Vault)
- [ ] Configure firewall rules
- [ ] Set up domain and DNS

## Deployment Platforms

This Docker setup works on:
- **Local Development**: Docker Desktop
- **VPS**: DigitalOcean, Linode, AWS EC2, etc.
- **Cloud**: AWS ECS, Google Cloud Run, Azure Container Instances
- **PaaS**: Railway, Render, Fly.io

## Getting Help

1. Check logs: `docker-compose logs -f`
2. Verify environment: `docker-compose config`
3. Test connectivity: `docker-compose exec backend curl http://mongodb:27017`
4. Review Docker status: `docker-compose ps`

## Clean Uninstall

```bash
# Stop and remove containers, networks, and volumes
docker-compose down -v

# Remove images
docker rmi $(docker images 'app_*' -q)

# Remove project directory
cd ..
rm -rf app
```
