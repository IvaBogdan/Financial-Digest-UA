# Environment Variables Guide

Complete reference for all environment variables used in the Telegram Crypto Bot.

---

## 📋 Quick Setup Checklist

**Minimum required to start:**
- ✅ `TELEGRAM_BOT_TOKEN` - Get from @BotFather
- ✅ `EMERGENT_LLM_KEY` - Already configured
- ⚠️ Everything else is optional

---

## 🔧 Required Variables

### TELEGRAM_BOT_TOKEN
**Required:** ✅ Yes  
**Default:** None  
**Where to get:** [@BotFather](https://t.me/BotFather) on Telegram

```bash
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

**How to get:**
1. Open Telegram, search for `@BotFather`
2. Send `/newbot`
3. Follow instructions
4. Copy the token provided

---

### EMERGENT_LLM_KEY
**Required:** ✅ For AI features  
**Default:** `sk-emergent-fC6934eD2A55986A6A` (pre-configured)

```bash
EMERGENT_LLM_KEY=sk-emergent-fC6934eD2A55986A6A
```

**What it does:** Powers AI analysis and chat features using OpenAI GPT-5

---

## 📰 News API Keys (Optional)

### CRYPTOPANIC_API_KEY
**Required:** ⚠️ Optional (recommended)  
**Free tier:** 500 requests/month  
**Where to get:** https://cryptopanic.com/developers/api/

```bash
CRYPTOPANIC_API_KEY=your_cryptopanic_key_here
```

**What it does:** Provides crypto-specific news and sentiment data

---

### NEWSAPI_KEY
**Required:** ⚠️ Optional (recommended)  
**Free tier:** 100 requests/day (with 24h delay)  
**Where to get:** https://newsapi.org/

```bash
NEWSAPI_KEY=your_newsapi_key_here
```

**What it does:** Provides financial and general crypto news

**Note:** Free tier has 24h delay for articles. Consider upgrading or using RSS fallback.

---

## 🏦 External Data Sources (Free, No Keys Needed)

### NBU_API_ENABLED
**Required:** No  
**Default:** `true`  
**API:** https://bank.gov.ua/NBUStatService/v1/

```bash
NBU_API_ENABLED=true
```

**What it does:** Fetches UAH exchange rates from National Bank of Ukraine  
**Features enabled:**
- `/uah` command - Current UAH/USD, EUR, PLN, GBP rates
- `/fxchart` - UAH exchange rate charts
- Daily digest UAH context

**No API key required** - Public API

---

### ECB_RSS_ENABLED
**Required:** No  
**Default:** `true`  
**RSS Feed:** https://www.ecb.europa.eu/rss/press.html

```bash
ECB_RSS_ENABLED=true
```

**What it does:** European Central Bank press releases and speeches  
**Features enabled:**
- Macro economic news in digests
- ECB policy announcements

**No API key required** - Public RSS feed

---

### IMF_RSS_ENABLED
**Required:** No  
**Default:** `true`  
**RSS Feed:** https://www.imf.org/en/News/RSS

```bash
IMF_RSS_ENABLED=true
```

**What it does:** International Monetary Fund news and reports  
**Features enabled:**
- Global macro context
- IMF statements on Ukraine and global economy

**No API key required** - Public RSS feed

---

### COINGECKO_API_KEY
**Required:** No  
**Free tier:** 10-30 calls/minute (no key needed)  
**Pro tier:** Increases rate limits  
**Where to get:** https://www.coingecko.com/en/api/pricing

```bash
COINGECKO_API_KEY=
```

**What it does:** Crypto prices, market data, charts  
**Leave empty to use free tier** (sufficient for most use cases)

---

## 🌍 Bot Features Configuration

### DEFAULT_LANGUAGE
**Default:** `en`  
**Options:** `en` (English), `ua` (Ukrainian)

```bash
DEFAULT_LANGUAGE=en
```

**What it does:** Default language for new users

---

### DEFAULT_TIMEZONE
**Default:** `Europe/Kiev`  
**Options:** Any valid timezone (e.g., `Europe/London`, `America/New_York`)

```bash
DEFAULT_TIMEZONE=Europe/Kiev
```

**What it does:** Default timezone for digest scheduling

---

### MORNING_DIGEST_TIME
**Default:** `08:00`  
**Format:** `HH:MM` (24-hour format)

```bash
MORNING_DIGEST_TIME=08:00
```

**What it does:** When to send morning digest (in DEFAULT_TIMEZONE)

---

### EVENING_DIGEST_TIME
**Default:** `18:00`  
**Format:** `HH:MM` (24-hour format)

```bash
EVENING_DIGEST_TIME=18:00
```

**What it does:** When to send evening digest (in DEFAULT_TIMEZONE)

---

### Feature Toggles

Enable/disable specific features:

```bash
ENABLE_WATCHLISTS=true      # Watchlists and price alerts
ENABLE_PORTFOLIO=true       # Portfolio tracking
ENABLE_INLINE_MODE=true     # Inline queries (@yourbot btc)
ENABLE_CHARTS=true          # Server-generated charts
```

---

## 🧪 Testing & Development

### PREMIUM_TESTING_MODE
**Default:** `false`  
**⚠️ IMPORTANT:** Set to `false` in production!

```bash
# Enable free premium for ALL users (testing only)
PREMIUM_TESTING_MODE=true
```

**What it does:**
- When `true`: **ALL users get premium features for free**
- When `false`: Normal subscription system applies

**Use case:**
```bash
# During development
PREMIUM_TESTING_MODE=true

# In production
PREMIUM_TESTING_MODE=false
```

---

### PREMIUM_TEST_USERS
**Default:** Empty  
**Format:** Comma-separated user IDs

```bash
# Give specific users free premium
PREMIUM_TEST_USERS=123456789,987654321
```

**What it does:** These specific Telegram user IDs get premium for free

**How to find your user ID:**
1. Start your bot
2. Send `/start`
3. Check logs: `docker-compose logs telegram-bot`
4. Look for your Telegram ID

**Example:**
```bash
# Give yourself and one tester free premium
PREMIUM_TEST_USERS=123456789,555666777
```

---

### DEBUG_MODE
**Default:** `false`

```bash
DEBUG_MODE=true
```

**What it does:** Enables verbose logging for debugging

---

## ⚡ Performance & Rate Limiting

### Cache TTL (Time To Live)

Control how long to cache external API responses:

```bash
COINGECKO_CACHE_TTL=60      # CoinGecko data (seconds)
NEWS_CACHE_TTL=300          # News articles (5 minutes)
NBU_CACHE_TTL=3600          # NBU rates (1 hour)
```

**Why cache?**
- Respects rate limits
- Faster response times
- Reduces external API calls

---

### USER_RATE_LIMIT
**Default:** `30`

```bash
USER_RATE_LIMIT=30
```

**What it does:** Max commands per user per minute  
**Prevents:** Spam and abuse

---

## 📝 Complete Example .env File

Here's a complete example with all variables:

```bash
# ========================================
# DATABASE (Do not modify)
# ========================================
MONGO_URL="mongodb://localhost:27017"
DB_NAME="crypto_bot_db"
CORS_ORIGINS="*"

# ========================================
# TELEGRAM BOT (REQUIRED)
# ========================================
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# ========================================
# AI INTEGRATION (Pre-configured)
# ========================================
EMERGENT_LLM_KEY=sk-emergent-fC6934eD2A55986A6A

# ========================================
# NEWS APIS (Optional but recommended)
# ========================================
CRYPTOPANIC_API_KEY=your_key_here
NEWSAPI_KEY=your_key_here

# ========================================
# FREE DATA SOURCES (No keys needed)
# ========================================
NBU_API_ENABLED=true
ECB_RSS_ENABLED=true
IMF_RSS_ENABLED=true
COINGECKO_API_KEY=

# ========================================
# BOT CONFIGURATION
# ========================================
DEFAULT_LANGUAGE=en
DEFAULT_TIMEZONE=Europe/Kiev
MORNING_DIGEST_TIME=08:00
EVENING_DIGEST_TIME=18:00

# ========================================
# FEATURE TOGGLES
# ========================================
ENABLE_WATCHLISTS=true
ENABLE_PORTFOLIO=true
ENABLE_INLINE_MODE=true
ENABLE_CHARTS=true

# ========================================
# TESTING (Set to false in production!)
# ========================================
PREMIUM_TESTING_MODE=false
PREMIUM_TEST_USERS=
DEBUG_MODE=false

# ========================================
# PERFORMANCE
# ========================================
COINGECKO_CACHE_TTL=60
NEWS_CACHE_TTL=300
NBU_CACHE_TTL=3600
USER_RATE_LIMIT=30
```

---

## 🎯 Quick Setup Scenarios

### Scenario 1: Minimal Setup (Just to test)

```bash
TELEGRAM_BOT_TOKEN=your_token
EMERGENT_LLM_KEY=sk-emergent-fC6934eD2A55986A6A
PREMIUM_TESTING_MODE=true  # Free premium for testing
```

---

### Scenario 2: Full Features (Development)

```bash
TELEGRAM_BOT_TOKEN=your_token
EMERGENT_LLM_KEY=sk-emergent-fC6934eD2A55986A6A
CRYPTOPANIC_API_KEY=your_key
NEWSAPI_KEY=your_key
PREMIUM_TESTING_MODE=true
DEBUG_MODE=true
```

---

### Scenario 3: Production Ready

```bash
TELEGRAM_BOT_TOKEN=your_token
EMERGENT_LLM_KEY=sk-emergent-fC6934eD2A55986A6A
CRYPTOPANIC_API_KEY=your_key
NEWSAPI_KEY=your_key

# All free features enabled
NBU_API_ENABLED=true
ECB_RSS_ENABLED=true
IMF_RSS_ENABLED=true

# Normal subscription (not free)
PREMIUM_TESTING_MODE=false
PREMIUM_TEST_USERS=
DEBUG_MODE=false
```

---

## 🔒 Security Best Practices

1. **Never commit `.env` to git**
   ```bash
   # Already in .gitignore
   echo ".env" >> .gitignore
   ```

2. **Use different tokens for dev/prod**
   - Create separate bots for testing and production
   - Use `PREMIUM_TESTING_MODE=true` only in development

3. **Rotate API keys periodically**
   - Especially if they're exposed in logs

4. **Keep EMERGENT_LLM_KEY secure**
   - It's billed based on usage
   - Monitor usage in your Emergent dashboard

---

## 🐛 Troubleshooting

### Bot not starting?
```bash
# Check if token is set
grep TELEGRAM_BOT_TOKEN .env

# Should show your token, not empty
```

### News not working?
```bash
# Check API keys
grep -E "(CRYPTOPANIC|NEWSAPI)" .env

# If empty, bot will work but with limited news
```

### Want free premium for testing?
```bash
# Option 1: Everyone gets premium
PREMIUM_TESTING_MODE=true

# Option 2: Specific users only
PREMIUM_TEST_USERS=your_telegram_id
```

**To find your Telegram ID:**
```bash
# Start bot, send /start, then check logs
docker-compose logs telegram-bot | grep "telegram_id"
```

---

## 📞 Getting API Keys

### CryptoPanic (Recommended)
1. Go to https://cryptopanic.com/developers/api/
2. Sign up with email
3. Copy API key
4. Paste in `.env`: `CRYPTOPANIC_API_KEY=your_key`

### NewsAPI (Recommended)
1. Go to https://newsapi.org/
2. Register for free account
3. Copy API key
4. Paste in `.env`: `NEWSAPI_KEY=your_key`

**Note:** Free tier has limitations. Bot will gracefully degrade if limits are hit.

---

## 🚀 After Changing .env

Always restart the bot to apply changes:

```bash
# Restart only bot
docker-compose restart telegram-bot

# Or restart everything
docker-compose down
docker-compose up -d
```

---

## 📊 Monitoring API Usage

Check your API usage:

- **CryptoPanic:** https://cryptopanic.com/developers/api/
- **NewsAPI:** https://newsapi.org/account
- **Emergent LLM:** Check your Emergent dashboard
- **CoinGecko:** No account needed for free tier

---

## ✅ Validation

Run this to validate your configuration:

```bash
# Check for required variables
docker-compose exec telegram-bot python -c "from config import config; print(config.validate())"
```

Should return empty list `[]` if all is good.

---

**Need help?** Check `DOCKER_TROUBLESHOOTING.md` or `QUICK_REFERENCE.md`
