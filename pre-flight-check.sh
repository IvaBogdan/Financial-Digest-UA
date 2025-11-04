#!/bin/bash

# Pre-flight check script
# Run this before docker-compose to catch common issues

echo "╔════════════════════════════════════════╗"
echo "║   Pre-Flight Check for Docker Setup   ║"
echo "╚════════════════════════════════════════╝"
echo ""

ERRORS=0
WARNINGS=0

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_ok() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
    ((ERRORS++))
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARNINGS++))
}

# Check 1: Docker installed
echo "Checking Docker installation..."
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    print_ok "Docker installed: $DOCKER_VERSION"
else
    print_error "Docker is not installed"
    echo "   Install from: https://www.docker.com/products/docker-desktop"
fi

# Check 2: Docker Compose installed
if command -v docker-compose &> /dev/null; then
    COMPOSE_VERSION=$(docker-compose --version)
    print_ok "Docker Compose installed: $COMPOSE_VERSION"
else
    print_error "Docker Compose is not installed"
fi

# Check 3: Docker running
if docker info &> /dev/null; then
    print_ok "Docker daemon is running"
else
    print_error "Docker daemon is not running"
    echo "   Start Docker Desktop and try again"
fi

echo ""
echo "Checking project files..."

# Check 4: Essential files exist
REQUIRED_FILES=(
    "docker-compose.yml"
    "Dockerfile.backend"
    "Dockerfile.bot"
    "Dockerfile.frontend"
    ".env.example"
    "backend/bot_service.py"
    "backend/crypto_service.py"
    "backend/news_service.py"
    "backend/ai_service.py"
    "backend/payment_service.py"
    "backend/server.py"
    "backend/requirements.txt"
    "frontend/package.json"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        print_ok "$file"
    else
        print_error "$file is missing"
    fi
done

echo ""
echo "Checking configuration..."

# Check 5: .env file exists
if [ -f ".env" ]; then
    print_ok ".env file exists"
    
    # Check 6: TELEGRAM_BOT_TOKEN is set
    if grep -q "TELEGRAM_BOT_TOKEN=.\+" .env 2>/dev/null; then
        TOKEN=$(grep "TELEGRAM_BOT_TOKEN=" .env | cut -d'=' -f2)
        if [ ! -z "$TOKEN" ] && [ "$TOKEN" != "" ]; then
            print_ok "TELEGRAM_BOT_TOKEN is configured"
        else
            print_error "TELEGRAM_BOT_TOKEN is empty in .env"
            echo "   Get token from @BotFather on Telegram"
        fi
    else
        print_error "TELEGRAM_BOT_TOKEN not found in .env"
        echo "   Add: TELEGRAM_BOT_TOKEN=your_token_here"
    fi
    
    # Check 7: EMERGENT_LLM_KEY is set
    if grep -q "EMERGENT_LLM_KEY=.\+" .env 2>/dev/null; then
        print_ok "EMERGENT_LLM_KEY is configured"
    else
        print_warning "EMERGENT_LLM_KEY not found (AI features won't work)"
    fi
else
    print_error ".env file not found"
    echo "   Run: cp .env.example .env"
fi

echo ""
echo "Checking ports availability..."

# Check 8: Required ports are free
check_port() {
    if command -v lsof &> /dev/null; then
        if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
            print_warning "Port $1 is already in use"
            lsof -i :$1 | grep LISTEN
            return 1
        else
            print_ok "Port $1 is available"
            return 0
        fi
    else
        # lsof not available (might be Windows)
        print_warning "Cannot check port $1 (lsof not available)"
        return 0
    fi
}

check_port 3000   # Frontend
check_port 8001   # Backend
check_port 27017  # MongoDB

echo ""
echo "Checking Docker resources..."

# Check 9: Docker disk space
if docker info &> /dev/null; then
    DISK_USAGE=$(docker system df -v 2>/dev/null | grep -i "Total" | awk '{print $4}')
    if [ ! -z "$DISK_USAGE" ]; then
        print_ok "Docker disk usage: $DISK_USAGE"
    fi
fi

echo ""
echo "Checking requirements.txt..."

# Check 10: requirements.txt is valid
if [ -f "backend/requirements.txt" ]; then
    LINE_COUNT=$(wc -l < backend/requirements.txt)
    if [ $LINE_COUNT -gt 5 ] && [ $LINE_COUNT -lt 50 ]; then
        print_ok "requirements.txt looks good ($LINE_COUNT lines)"
    elif [ $LINE_COUNT -gt 50 ]; then
        print_warning "requirements.txt has many packages ($LINE_COUNT lines)"
        echo "   This might slow down builds"
    else
        print_error "requirements.txt seems too small ($LINE_COUNT lines)"
    fi
    
    # Check for emergentintegrations
    if grep -q "emergentintegrations" backend/requirements.txt; then
        print_ok "emergentintegrations found in requirements.txt"
    else
        print_warning "emergentintegrations not found in requirements.txt"
    fi
else
    print_error "backend/requirements.txt not found"
fi

echo ""
echo "════════════════════════════════════════"
echo "Summary:"
echo "════════════════════════════════════════"

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed! Ready to run docker-compose up -d${NC}"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠ $WARNINGS warning(s) found${NC}"
    echo "You can proceed, but review the warnings above"
    exit 0
else
    echo -e "${RED}✗ $ERRORS error(s) found${NC}"
    if [ $WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}⚠ $WARNINGS warning(s) found${NC}"
    fi
    echo ""
    echo "Please fix the errors above before running docker-compose"
    echo ""
    echo "Common fixes:"
    echo "  • Install Docker Desktop: https://www.docker.com/products/docker-desktop"
    echo "  • Create .env file: cp .env.example .env"
    echo "  • Add bot token to .env file"
    echo "  • Make sure all project files are present"
    exit 1
fi
