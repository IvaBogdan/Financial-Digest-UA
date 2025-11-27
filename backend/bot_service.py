import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
    PreCheckoutQueryHandler,
)
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone, timedelta
import asyncio

from crypto_service import CryptoService
from news_service import NewsService
from ai_service import AIService
from payment_service import PaymentService

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# MongoDB setup
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Initialize services
crypto_service = CryptoService()
news_service = NewsService()
ai_service = AIService()
payment_service = PaymentService(db)


class TelegramBot:
    def __init__(self):
        self.token = os.environ.get('TELEGRAM_BOT_TOKEN')
        self.application = None
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        telegram_id = user.id
        
        # Register user in database
        existing_user = await db.users.find_one({"telegram_id": telegram_id})
        if not existing_user:
            await db.users.insert_one({
                "telegram_id": telegram_id,
                "username": user.username,
                "first_name": user.first_name,
                "subscription_tier": "free",
                "created_at": datetime.now(timezone.utc).isoformat()
            })
        
        keyboard = [
            [InlineKeyboardButton("📊 Market Overview", callback_data="market_overview")],
            [InlineKeyboardButton("📰 Latest News", callback_data="latest_news")],
            [InlineKeyboardButton("💎 Analyze Asset", callback_data="analyze_asset")],
            [InlineKeyboardButton("🤖 AI Assistant", callback_data="ai_chat")],
            [InlineKeyboardButton("⭐ Premium Subscription", callback_data="subscribe")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        welcome_text = f"""👋 Welcome to Crypto Analysis Bot, {user.first_name}!

🆓 **Free Features:**
• Daily news digest
• General market overview
• Basic price checks

⭐ **Premium Features ($5/month):**
• Detailed AI-powered asset analysis
• Price predictions with reasoning
• Unlimited AI conversations
• Personalized alerts
• In-depth market reports

What would you like to do?"""
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """🔰 **Available Commands:**

/start - Start the bot
/help - Show this help message
/market - Get market overview
/news - Get latest crypto news
/price [symbol] - Get price of a crypto (e.g., /price BTC)
/analyze [symbol] - Detailed analysis (Premium)
/subscribe - Subscribe to premium
/status - Check your subscription status

You can also chat directly with me for AI assistance (Premium feature)!"""
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def market_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /market command - Free feature"""
        await update.message.reply_text("📊 Fetching market data...")
        
        try:
            market_data = await crypto_service.get_market_overview()
            await update.message.reply_text(market_data, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Error fetching market data: {e}")
            await update.message.reply_text("❌ Error fetching market data. Please try again later.")
    
    async def news_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /news command - Free feature"""
        await update.message.reply_text("📰 Fetching latest news...")
        
        try:
            news = await news_service.get_latest_news()
            await update.message.reply_text(news, parse_mode='Markdown', disable_web_page_preview=True)
        except Exception as e:
            logger.error(f"Error fetching news: {e}")
            await update.message.reply_text("❌ Error fetching news. Please try again later.")
    
    async def price_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /price command - Free feature"""
        if not context.args:
            await update.message.reply_text("Please provide a crypto symbol. Example: /price BTC")
            return
        
        symbol = context.args[0].upper()
        
        try:
            price_data = await crypto_service.get_price(symbol)
            await update.message.reply_text(price_data, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Error fetching price: {e}")
            await update.message.reply_text(f"❌ Error fetching price for {symbol}. Please check the symbol and try again.")
    
    async def analyze_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /analyze command - Premium feature"""
        user_id = update.effective_user.id
        
        # Check subscription
        is_premium = await payment_service.check_subscription(user_id)
        if not is_premium:
            await update.message.reply_text(
                "⭐ This is a premium feature. Please subscribe using /subscribe to access detailed analysis."
            )
            return
        
        if not context.args:
            await update.message.reply_text("Please provide a crypto symbol. Example: /analyze BTC")
            return
        
        symbol = context.args[0].upper()
        await update.message.reply_text(f"🔍 Analyzing {symbol}... This may take a moment.")
        
        try:
            # Get crypto data
            crypto_data = await crypto_service.get_detailed_data(symbol)
            
            # Get AI analysis
            analysis = await ai_service.analyze_asset(symbol, crypto_data)
            
            await update.message.reply_text(analysis, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Error analyzing {symbol}: {e}")
            await update.message.reply_text(f"❌ Error analyzing {symbol}. Please try again later.")
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command"""
        user_id = update.effective_user.id
        
        user_data = await db.users.find_one({"telegram_id": user_id})
        subscription = await db.subscriptions.find_one({"telegram_id": user_id})
        
        if subscription and subscription.get('expires_at'):
            expires_at = subscription['expires_at']
            if isinstance(expires_at, str):
                expires_at = datetime.fromisoformat(expires_at)
            
            if expires_at > datetime.now(timezone.utc):
                status_text = f"""✅ **Subscription Status**

🎯 Tier: Premium ⭐
📅 Expires: {expires_at.strftime('%Y-%m-%d %H:%M UTC')}
💡 Enjoy unlimited access to all features!"""
            else:
                status_text = """❌ **Subscription Status**

🎯 Tier: Free
💡 Your premium subscription has expired. Renew with /subscribe"""
        else:
            status_text = """📊 **Subscription Status**

🎯 Tier: Free
💡 Upgrade to Premium for $5/month to unlock:
• AI-powered asset analysis
• Price predictions
• Unlimited AI chat
• Personalized alerts

Use /subscribe to upgrade!"""
        
        await update.message.reply_text(status_text, parse_mode='Markdown')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages - AI chat (Premium)"""
        user_id = update.effective_user.id
        message_text = update.message.text
        
        # Check subscription
        is_premium = await payment_service.check_subscription(user_id)
        if not is_premium:
            await update.message.reply_text(
                "🤖 AI Assistant is a premium feature. Subscribe with /subscribe to chat with AI!"
            )
            return
        
        # AI Chat
        try:
            response = await ai_service.chat(user_id, message_text)
            await update.message.reply_text(response, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Error in AI chat: {e}")
            await update.message.reply_text("❌ Sorry, I encountered an error. Please try again.")
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        callback_data = query.data
        
        if callback_data == "market_overview":
            await query.message.reply_text("📊 Fetching market data...")
            try:
                market_data = await crypto_service.get_market_overview()
                await query.message.reply_text(market_data, parse_mode='Markdown')
            except Exception as e:
                await query.message.reply_text("❌ Error fetching market data.")
        
        elif callback_data == "latest_news":
            await query.message.reply_text("📰 Fetching latest news...")
            try:
                news = await news_service.get_latest_news()
                await query.message.reply_text(news, parse_mode='Markdown', disable_web_page_preview=True)
            except Exception as e:
                await query.message.reply_text("❌ Error fetching news.")
        
        elif callback_data == "analyze_asset":
            is_premium = await payment_service.check_subscription(user_id)
            if not is_premium:
                await query.message.reply_text(
                    "⭐ Asset analysis is a premium feature. Use /subscribe to upgrade!"
                )
            else:
                await query.message.reply_text(
                    "Please send the crypto symbol you want to analyze (e.g., BTC, ETH, SOL)"
                )
        
        elif callback_data == "ai_chat":
            is_premium = await payment_service.check_subscription(user_id)
            if not is_premium:
                await query.message.reply_text(
                    "⭐ AI Assistant is a premium feature. Use /subscribe to upgrade!"
                )
            else:
                await query.message.reply_text(
                    "🤖 AI Assistant activated! Just send me your questions about crypto markets, analysis, or anything else."
                )
        
        elif callback_data == "subscribe":
            await self.subscribe_command(update, context)
    
    async def subscribe_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle subscription request"""
        # Get user_id from either message or callback query
        if update.message:
            chat_id = update.message.chat_id
            user_id = update.effective_user.id
        else:
            chat_id = update.callback_query.message.chat_id
            user_id = update.effective_user.id
        
        # Check if already subscribed
        is_premium = await payment_service.check_subscription(user_id)
        if is_premium:
            text = "✅ You already have an active premium subscription!"
            if update.message:
                await update.message.reply_text(text)
            else:
                await update.callback_query.message.reply_text(text)
            return
        
        # Create payment invoice
        title = "Premium Subscription"
        description = "Get unlimited access to AI analysis, detailed reports, and AI assistant for 30 days"
        payload = f"premium_sub_{user_id}"
        currency = "XTR"  # Telegram Stars
        price = 50  # 50 stars (~$5)
        
        try:
            await context.bot.send_invoice(
                chat_id=chat_id,
                title=title,
                description=description,
                payload=payload,
                provider_token="",  # Empty for Telegram Stars
                currency=currency,
                prices=[{"label": "Premium", "amount": price}]
            )
        except Exception as e:
            logger.error(f"Error sending invoice: {e}")
            text = "❌ Error creating payment. Please try again later."
            if update.message:
                await update.message.reply_text(text)
            else:
                await update.callback_query.message.reply_text(text)
    
    async def precheckout_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle pre-checkout query"""
        query = update.pre_checkout_query
        await query.answer(ok=True)
    
    async def successful_payment_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle successful payment"""
        user_id = update.effective_user.id
        payment_info = update.message.successful_payment
        
        # Activate premium subscription
        await payment_service.activate_subscription(user_id, payment_info)
        
        await update.message.reply_text(
            """🎉 **Payment Successful!**

✅ Your premium subscription is now active!

🎯 You now have access to:
• Detailed AI-powered asset analysis
• Price predictions with reasoning
• Unlimited AI conversations
• Personalized alerts

Try /analyze BTC or just chat with me!""",
            parse_mode='Markdown'
        )
    
    async def send_daily_digest(self):
        """Send daily news digest to all users"""
        try:
            news_digest = await news_service.get_daily_digest()
            market_summary = await crypto_service.get_market_overview()
            
            digest_text = f"""🌅 **Daily Crypto Digest**

{market_summary}

---

{news_digest}

💡 For detailed analysis and AI insights, upgrade to Premium with /subscribe"""
            
            # Get all users
            users = await db.users.find({}).to_list(1000)
            
            for user in users:
                try:
                    await self.application.bot.send_message(
                        chat_id=user['telegram_id'],
                        text=digest_text,
                        parse_mode='Markdown',
                        disable_web_page_preview=True
                    )
                    await asyncio.sleep(0.1)  # Rate limiting
                except Exception as e:
                    logger.error(f"Error sending digest to {user['telegram_id']}: {e}")
        
        except Exception as e:
            logger.error(f"Error creating daily digest: {e}")
    
    async def schedule_daily_tasks(self, context: ContextTypes.DEFAULT_TYPE):
        """Schedule daily tasks"""
        await self.send_daily_digest()
    
    def run(self):
        """Start the bot"""
        if not self.token:
            logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
            return
        
        self.application = Application.builder().token(self.token).build()
        
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("market", self.market_command))
        self.application.add_handler(CommandHandler("news", self.news_command))
        self.application.add_handler(CommandHandler("price", self.price_command))
        self.application.add_handler(CommandHandler("analyze", self.analyze_command))
        self.application.add_handler(CommandHandler("subscribe", self.subscribe_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        
        # Callback query handler
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Payment handlers
        self.application.add_handler(PreCheckoutQueryHandler(self.precheckout_callback))
        self.application.add_handler(
            MessageHandler(filters.SUCCESSFUL_PAYMENT, self.successful_payment_callback)
        )
        
        # Message handler for AI chat
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )
        
        # Schedule daily digest (runs at 9 AM UTC)
        job_queue = self.application.job_queue
        if job_queue:
            job_queue.run_daily(
                self.schedule_daily_tasks,
                time=datetime.strptime("09:00", "%H:%M").time()
            )
            logger.info("Daily digest scheduled for 9 AM UTC")
        else:
            logger.warning("JobQueue not available - daily digest will not be scheduled")
        
        logger.info("Bot started successfully")
        logger.info("Version 1.0.0")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    bot = TelegramBot()
    bot.run()
