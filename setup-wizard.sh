#!/bin/bash

# Telegram Crypto Bot - Setup Wizard
# This script will guide you through the complete setup process

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored messages
print_step() {
    echo -e "${BLUE}==>${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_header() {
    echo ""
    echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC}  Telegram Crypto Bot - Setup Wizard             ${BLUE}║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to wait for user
wait_for_user() {
    echo ""
    read -p "Press Enter to continue..."
    echo ""
}

# Function to ask yes/no question
ask_yes_no() {
    while true; do
        read -p "$1 (y/n): " yn
        case $yn in
            [Yy]* ) return 0;;
            [Nn]* ) return 1;;
            * ) echo "Please answer yes (y) or no (n).";;
        esac
    done
}

# Clear screen and show header
clear
print_header

echo "This wizard will help you set up the Telegram Crypto Bot locally."
echo "The entire process takes about 5-10 minutes."
echo ""
wait_for_user

# ===== STEP 1: Check Docker =====
clear
print_header
print_step "Step 1/7: Checking Docker installation..."
echo ""

if command_exists docker; then
    DOCKER_VERSION=$(docker --version)
    print_success "Docker is installed: $DOCKER_VERSION"
else
    print_error "Docker is not installed!"
    echo ""
    echo "Please install Docker Desktop from:"
    echo "https://www.docker.com/products/docker-desktop"
    echo ""
    echo "After installing, run this script again."
    exit 1
fi

if command_exists docker-compose; then
    COMPOSE_VERSION=$(docker-compose --version)
    print_success "Docker Compose is installed: $COMPOSE_VERSION"
else
    print_error "Docker Compose is not installed!"
    echo ""
    echo "Docker Compose is usually included with Docker Desktop."
    echo "If you're on Linux, install it with:"
    echo "  sudo apt-get install docker-compose"
    exit 1
fi

# Check if Docker is running
if docker info >/dev/null 2>&1; then
    print_success "Docker is running"
else
    print_error "Docker is not running!"
    echo ""
    echo "Please start Docker Desktop and run this script again."
    exit 1
fi

wait_for_user

# ===== STEP 2: Check Project Files =====
clear
print_header
print_step "Step 2/7: Checking project files..."
echo ""

REQUIRED_FILES=(
    "docker-compose.yml"
    "Dockerfile.backend"
    "Dockerfile.bot"
    "Dockerfile.frontend"
    ".env.example"
    "backend/bot_service.py"
    "backend/requirements.txt"
    "frontend/package.json"
)

ALL_FILES_PRESENT=true
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        print_success "$file"
    else
        print_error "$file is missing!"
        ALL_FILES_PRESENT=false
    fi
done

if [ "$ALL_FILES_PRESENT" = false ]; then
    echo ""
    print_error "Some required files are missing!"
    echo "Please make sure you have all project files in the current directory."
    exit 1
fi

wait_for_user

# ===== STEP 3: Create .env file =====
clear
print_header
print_step "Step 3/7: Setting up environment configuration..."
echo ""

if [ -f ".env" ]; then
    print_warning ".env file already exists"
    if ask_yes_no "Do you want to overwrite it?"; then
        cp .env.example .env
        print_success "Created new .env file from template"
    else
        print_success "Using existing .env file"
    fi
else
    cp .env.example .env
    print_success "Created .env file from template"
fi

wait_for_user

# ===== STEP 4: Get Telegram Bot Token =====
clear
print_header
print_step "Step 4/7: Configure Telegram Bot Token..."
echo ""

# Check if token is already set
if grep -q "TELEGRAM_BOT_TOKEN=.\+" .env 2>/dev/null; then
    CURRENT_TOKEN=$(grep "TELEGRAM_BOT_TOKEN=" .env | cut -d'=' -f2)
    if [ ! -z "$CURRENT_TOKEN" ]; then
        print_success "Bot token is already configured"
        TOKEN_SET=true
    else
        TOKEN_SET=false
    fi
else
    TOKEN_SET=false
fi

if [ "$TOKEN_SET" = false ]; then
    echo "You need a Telegram Bot Token from @BotFather"
    echo ""
    echo "Steps to get your token:"
    echo "1. Open Telegram"
    echo "2. Search for @BotFather"
    echo "3. Send: /newbot"
    echo "4. Follow instructions"
    echo "5. Copy the token (format: 1234567890:ABCdefGHI...)"
    echo ""
    
    if ask_yes_no "Do you have your bot token ready?"; then
        echo ""
        read -p "Enter your Telegram Bot Token: " BOT_TOKEN
        
        if [ -z "$BOT_TOKEN" ]; then
            print_error "Token cannot be empty!"
            exit 1
        fi
        
        # Update .env file
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            sed -i '' "s/TELEGRAM_BOT_TOKEN=.*/TELEGRAM_BOT_TOKEN=$BOT_TOKEN/" .env
        else
            # Linux
            sed -i "s/TELEGRAM_BOT_TOKEN=.*/TELEGRAM_BOT_TOKEN=$BOT_TOKEN/" .env
        fi
        
        print_success "Bot token configured successfully!"
    else
        echo ""
        print_error "Cannot continue without bot token"
        echo "Please get your token from @BotFather and run this script again."
        exit 1
    fi
fi

wait_for_user

# ===== STEP 5: Optional API Keys =====
clear
print_header
print_step "Step 5/7: Optional API Keys (for enhanced news)..."
echo ""

echo "The bot works without these, but you'll get better news coverage with them."
echo ""
echo "Optional API Keys:"
echo "  • CryptoPanic: https://cryptopanic.com/developers/api/ (Free: 500 req/month)"
echo "  • NewsAPI: https://newsapi.org/ (Free: 100 req/day)"
echo ""

if ask_yes_no "Do you want to add optional API keys now?"; then
    echo ""
    read -p "CryptoPanic API Key (press Enter to skip): " CRYPTO_KEY
    read -p "NewsAPI Key (press Enter to skip): " NEWS_KEY
    
    if [ ! -z "$CRYPTO_KEY" ]; then
        if [[ "$OSTYPE" == "darwin"* ]]; then
            sed -i '' "s/CRYPTOPANIC_API_KEY=.*/CRYPTOPANIC_API_KEY=$CRYPTO_KEY/" .env
        else
            sed -i "s/CRYPTOPANIC_API_KEY=.*/CRYPTOPANIC_API_KEY=$CRYPTO_KEY/" .env
        fi
        print_success "CryptoPanic API key added"
    fi
    
    if [ ! -z "$NEWS_KEY" ]; then
        if [[ "$OSTYPE" == "darwin"* ]]; then
            sed -i '' "s/NEWSAPI_KEY=.*/NEWSAPI_KEY=$NEWS_KEY/" .env
        else
            sed -i "s/NEWSAPI_KEY=.*/NEWSAPI_KEY=$NEWS_KEY/" .env
        fi
        print_success "NewsAPI key added"
    fi
else
    print_warning "Skipping optional API keys (you can add them later)"
fi

wait_for_user

# ===== STEP 6: Start Services =====
clear
print_header
print_step "Step 6/7: Starting Docker services..."
echo ""

echo "This will download and start 4 services:"
echo "  1. MongoDB (Database)"
echo "  2. Backend API (FastAPI)"
echo "  3. Telegram Bot (Your bot)"
echo "  4. Frontend (Admin Dashboard)"
echo ""
echo "First time setup may take 2-5 minutes..."
echo ""

if ask_yes_no "Ready to start services?"; then
    echo ""
    print_step "Starting services (please wait)..."
    
    # Start services
    docker-compose up -d
    
    if [ $? -eq 0 ]; then
        print_success "Services started successfully!"
        echo ""
        print_step "Waiting for services to be ready (30 seconds)..."
        sleep 30
    else
        print_error "Failed to start services!"
        echo ""
        echo "Check logs with: docker-compose logs"
        exit 1
    fi
else
    echo ""
    print_error "Setup cancelled"
    exit 1
fi

wait_for_user

# ===== STEP 7: Verify Installation =====
clear
print_header
print_step "Step 7/7: Verifying installation..."
echo ""

# Check services
print_step "Checking service status..."
docker-compose ps

echo ""

# Test backend
print_step "Testing Backend API..."
if curl -s http://localhost:8001/api/ | grep -q "message"; then
    print_success "Backend API is responding"
else
    print_warning "Backend API might not be ready yet"
fi

# Check frontend
print_step "Testing Frontend..."
if curl -s http://localhost:3000 >/dev/null 2>&1; then
    print_success "Frontend is accessible"
else
    print_warning "Frontend might not be ready yet"
fi

# Check MongoDB
print_step "Testing MongoDB..."
if docker-compose exec -T mongodb mongosh --quiet --eval "db.version()" >/dev/null 2>&1; then
    print_success "MongoDB is running"
else
    print_warning "MongoDB might not be ready yet"
fi

# Check bot
print_step "Testing Telegram Bot..."
BOT_LOGS=$(docker-compose logs telegram-bot 2>&1)
if echo "$BOT_LOGS" | grep -q "started"; then
    print_success "Telegram Bot is running"
else
    print_warning "Telegram Bot might still be starting"
fi

wait_for_user

# ===== FINAL SUMMARY =====
clear
print_header
echo -e "${GREEN}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║${NC}           🎉 SETUP COMPLETE! 🎉                   ${GREEN}║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${BLUE}Access Points:${NC}"
echo "  🌐 Admin Dashboard:    http://localhost:3000"
echo "  🔌 Backend API:        http://localhost:8001/api/"
echo "  📱 Telegram Bot:       Search for your bot on Telegram"
echo ""

echo -e "${BLUE}Next Steps:${NC}"
echo "  1. Open Telegram and search for your bot"
echo "  2. Send /start to your bot"
echo "  3. Try these commands:"
echo "     • /market - Market overview"
echo "     • /news - Latest news"
echo "     • /price BTC - Bitcoin price"
echo ""

echo -e "${BLUE}Useful Commands:${NC}"
echo "  • View logs:           docker-compose logs -f"
echo "  • Stop services:       docker-compose down"
echo "  • Restart services:    docker-compose restart"
echo "  • Check status:        docker-compose ps"
echo ""

echo -e "${BLUE}Documentation:${NC}"
echo "  • Quick reference:     QUICK_REFERENCE.md"
echo "  • Full guide:          LOCAL_SETUP_GUIDE.md"
echo "  • Troubleshooting:     DOCKER_DEPLOYMENT.md"
echo ""

echo -e "${GREEN}Happy bot building! 🤖${NC}"
echo ""

# Ask to view logs
if ask_yes_no "Would you like to view the live logs now?"; then
    echo ""
    echo "Showing logs (press Ctrl+C to exit)..."
    sleep 2
    docker-compose logs -f
fi
