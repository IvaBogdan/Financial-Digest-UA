#!/bin/bash

echo "=================================="
echo "Crypto Bot Docker Setup"
echo "=================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed!"
    echo "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed!"
    echo "Please install Docker Compose"
    exit 1
fi

echo "✓ Docker is installed"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "✓ Created .env file"
    echo ""
    echo "📝 IMPORTANT: Edit .env file and add your TELEGRAM_BOT_TOKEN"
    echo "   Get token from @BotFather on Telegram"
    echo ""
    read -p "Press Enter to continue after adding your token..."
fi

# Check if TELEGRAM_BOT_TOKEN is set
if ! grep -q "TELEGRAM_BOT_TOKEN=.\+" .env; then
    echo "❌ TELEGRAM_BOT_TOKEN is not set in .env file!"
    echo ""
    echo "Please:"
    echo "1. Open Telegram and talk to @BotFather"
    echo "2. Send /newbot and follow instructions"
    echo "3. Copy the token"
    echo "4. Edit .env file and set: TELEGRAM_BOT_TOKEN=your_token_here"
    echo ""
    exit 1
fi

echo "✓ Configuration looks good"
echo ""
echo "🚀 Starting services..."
echo ""

# Start services
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service status
echo ""
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "=================================="
echo "✅ Setup Complete!"
echo "=================================="
echo ""
echo "Access Points:"
echo "  🌐 Admin Dashboard: http://localhost:3000"
echo "  🔌 Backend API: http://localhost:8001/api/"
echo "  📱 Telegram Bot: Search for your bot on Telegram"
echo ""
echo "Useful Commands:"
echo "  View logs: docker-compose logs -f"
echo "  Stop: docker-compose down"
echo "  Restart: docker-compose restart"
echo ""
echo "📖 Full documentation: See DOCKER_DEPLOYMENT.md"
echo ""
