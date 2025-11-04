# Crypto Analysis Telegram Bot

A comprehensive Telegram bot for cryptocurrency analysis powered by AI (OpenAI GPT-5), featuring real-time market data, news aggregation, and premium subscription system.

## Features

### Free Tier
- 📈 General market overview
- 📰 Daily news digest (automated)
- 💵 Basic price checks for any cryptocurrency
- 🔔 Access to latest crypto news from multiple sources

### Premium Tier ($5/month via Telegram Stars)
- 🔍 Detailed AI-powered asset analysis
- 🧠 Price predictions with reasoning and market insights
- 🤖 Unlimited AI conversational assistant
- 🎯 Personalized market reports
- ✨ Priority support

## Tech Stack

### Backend
- **FastAPI**: REST API for admin dashboard
- **Python Telegram Bot**: Telegram bot framework
- **MongoDB**: Database for users, subscriptions, and chat history
- **OpenAI GPT-5**: AI analysis and conversational assistant (via Emergent LLM)

### Data Sources
- **CoinGecko API**: Real-time crypto market data
- **CryptoPanic API**: Crypto-specific news
- **NewsAPI**: Financial news aggregation

### Frontend
- **React**: Admin dashboard
- **Tailwind CSS + Shadcn UI**: Modern UI components
- **Axios**: API client

## Setup Instructions

### 1. Get Your Telegram Bot Token

1. Open Telegram and talk to [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Choose a name (e.g., "Crypto Analysis Assistant")
4. Choose a username (must end with "bot", e.g., "my_crypto_analysis_bot")
5. Copy the token provided by BotFather

### 2. Configure API Keys

Edit `/app/backend/.env` file:

```bash
# Required
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# AI Integration (already configured with Emergent LLM key)
EMERGENT_LLM_KEY=sk-emergent-fC6934eD2A55986A6A

# Optional: News APIs (bot works without these, but with limited news)
CRYPTOPANIC_API_KEY=your_cryptopanic_api_key
NEWSAPI_KEY=your_newsapi_key
```

#### Getting Optional API Keys:

**CryptoPanic API** (for crypto news):
- Sign up at: https://cryptopanic.com/developers/api/
- Free tier: 500 requests/month

**NewsAPI** (for financial news):
- Sign up at: https://newsapi.org/
- Free tier: 100 requests/day

### 3. Run the Telegram Bot

```bash
python /app/backend/bot_service.py
```

The bot will start polling for messages. Keep this terminal running.

### 4. Access Admin Dashboard

The admin dashboard runs on the frontend (React app):

1. Make sure backend API is running: `sudo supervisorctl status backend`
2. Make sure frontend is running: `sudo supervisorctl status frontend`
3. Access dashboard at: `http://localhost:3000` (or your deployment URL)

The dashboard shows:
- Total users, premium/free breakdown
- Revenue statistics
- User list with subscription status
- Active subscriptions with expiration dates

### 5. Using the Bot

Find your bot on Telegram using the username you chose and:

1. Send `/start` to begin
2. Use the interactive menu or commands:
   - `/market` - Get market overview
   - `/news` - Latest crypto news
   - `/price BTC` - Get price of any crypto
   - `/analyze BTC` - Detailed AI analysis (Premium)
   - `/subscribe` - Subscribe to premium ($5/month)
   - `/status` - Check subscription status

3. **Premium Feature**: Chat directly with the AI assistant by just sending messages (no command needed)

## Bot Commands

| Command | Description | Tier |
|---------|-------------|------|
| `/start` | Start the bot and show main menu | Free |
| `/help` | Show help message with all commands | Free |
| `/market` | Get overview of top cryptocurrencies | Free |
| `/news` | Get latest crypto news | Free |
| `/price [symbol]` | Get price of a cryptocurrency | Free |
| `/analyze [symbol]` | Get detailed AI-powered analysis | Premium |
| `/subscribe` | Subscribe to premium tier | - |
| `/status` | Check your subscription status | Free |

## Architecture

### Services

1. **bot_service.py**: Main Telegram bot handler
   - Command handlers
   - Button callbacks
   - Payment processing
   - Daily digest scheduler

2. **crypto_service.py**: CoinGecko API integration
   - Market overview
   - Price data
   - Detailed crypto information

3. **news_service.py**: News aggregation
   - CryptoPanic integration
   - NewsAPI integration
   - Daily digest generation

4. **ai_service.py**: OpenAI GPT-5 integration
   - Asset analysis
   - Conversational chat
   - Chat history management

5. **payment_service.py**: Telegram Stars payments
   - Subscription management
   - Payment verification
   - Access control

### Database Collections

- **users**: User profiles and subscription tiers
- **subscriptions**: Premium subscription details
- **chat_history**: AI chat conversation history

## Payments

The bot uses **Telegram Stars** for premium subscriptions:

- Price: 50 Telegram Stars (~$5 USD)
- Duration: 30 days
- Auto-renewal: Not implemented (users need to manually renew)
- Telegram handles the payment processing

## Daily Digest

The bot automatically sends a daily digest at 9:00 AM UTC to all users containing:
- Market overview (top 10 cryptos)
- Latest news from multiple sources
- Call-to-action for premium features

## Monitoring & Admin

Use the admin dashboard to:
- Monitor user growth
- Track premium subscriptions
- View revenue statistics
- Check active subscriptions

## Development

### Backend Development

```bash
cd /app/backend
python bot_service.py
```

### Frontend Development

Frontend auto-reloads on changes:
```bash
cd /app/frontend
yarn start
```

### Database Access

MongoDB is accessible at `mongodb://localhost:27017`
Database name: `crypto_bot_db`

## Troubleshooting

### Bot not responding
1. Check if bot is running: `ps aux | grep bot_service`
2. Check logs for errors
3. Verify TELEGRAM_BOT_TOKEN is correct
4. Make sure bot is not blocked by Telegram

### News not showing
- CoinGecko API works without API key (basic features)
- News APIs are optional - add keys for full functionality
- Check API rate limits

### Payment issues
- Telegram Stars must be enabled by @BotFather
- Make sure bot has payment permissions
- Test with Telegram's test environment first

### AI not working
- EMERGENT_LLM_KEY should be pre-configured
- Check OpenAI service status
- Verify API key balance

## Future Enhancements

- 📧 Email notifications for price alerts
- 📈 Custom price alerts and watchlists
- 🔔 Real-time price notifications
- 📊 Advanced technical analysis
- 👥 Portfolio tracking
- 🌐 Multi-language support
- 📱 Mobile app companion

## License

MIT License

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review logs for error messages
3. Contact support via the admin dashboard
