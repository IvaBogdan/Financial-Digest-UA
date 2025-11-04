#!/bin/bash

echo "Starting Crypto Analysis Telegram Bot..."
echo ""
echo "Make sure you have:"
echo "1. Added TELEGRAM_BOT_TOKEN to /app/backend/.env"
echo "2. MongoDB is running"
echo ""

cd /app/backend

# Check if TELEGRAM_BOT_TOKEN is set
if grep -q "TELEGRAM_BOT_TOKEN=" .env && ! grep -q "TELEGRAM_BOT_TOKEN=$" .env; then
    echo "✓ TELEGRAM_BOT_TOKEN found in .env"
    echo ""
    echo "Starting bot..."
    echo ""
    python bot_service.py
else
    echo "✗ TELEGRAM_BOT_TOKEN not found or empty in .env!"
    echo ""
    echo "Please:"
    echo "1. Go to https://t.me/BotFather"
    echo "2. Create a new bot using /newbot"
    echo "3. Copy the token"
    echo "4. Add it to /app/backend/.env:"
    echo "   TELEGRAM_BOT_TOKEN=your_token_here"
    echo ""
    exit 1
fi
