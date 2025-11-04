"""
Configuration management for the Telegram Crypto Bot
Loads and validates environment variables
"""
import os
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration"""
    
    # Database
    MONGO_URL: str = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
    DB_NAME: str = os.getenv('DB_NAME', 'crypto_bot_db')
    
    # Telegram
    TELEGRAM_BOT_TOKEN: str = os.getenv('TELEGRAM_BOT_TOKEN', '')
    
    # AI Integration
    EMERGENT_LLM_KEY: str = os.getenv('EMERGENT_LLM_KEY', '')
    
    # News APIs
    CRYPTOPANIC_API_KEY: str = os.getenv('CRYPTOPANIC_API_KEY', '')
    NEWSAPI_KEY: str = os.getenv('NEWSAPI_KEY', '')
    
    # External APIs
    NBU_API_ENABLED: bool = os.getenv('NBU_API_ENABLED', 'true').lower() == 'true'
    ECB_RSS_ENABLED: bool = os.getenv('ECB_RSS_ENABLED', 'true').lower() == 'true'
    IMF_RSS_ENABLED: bool = os.getenv('IMF_RSS_ENABLED', 'true').lower() == 'true'
    COINGECKO_API_KEY: str = os.getenv('COINGECKO_API_KEY', '')
    
    # Bot Features
    DEFAULT_LANGUAGE: str = os.getenv('DEFAULT_LANGUAGE', 'en')
    DEFAULT_TIMEZONE: str = os.getenv('DEFAULT_TIMEZONE', 'Europe/Kiev')
    MORNING_DIGEST_TIME: str = os.getenv('MORNING_DIGEST_TIME', '08:00')
    EVENING_DIGEST_TIME: str = os.getenv('EVENING_DIGEST_TIME', '18:00')
    
    ENABLE_WATCHLISTS: bool = os.getenv('ENABLE_WATCHLISTS', 'true').lower() == 'true'
    ENABLE_PORTFOLIO: bool = os.getenv('ENABLE_PORTFOLIO', 'true').lower() == 'true'
    ENABLE_INLINE_MODE: bool = os.getenv('ENABLE_INLINE_MODE', 'true').lower() == 'true'
    ENABLE_CHARTS: bool = os.getenv('ENABLE_CHARTS', 'true').lower() == 'true'
    
    # Testing & Development
    PREMIUM_TESTING_MODE: bool = os.getenv('PREMIUM_TESTING_MODE', 'false').lower() == 'true'
    PREMIUM_TEST_USERS: List[int] = [
        int(uid.strip()) 
        for uid in os.getenv('PREMIUM_TEST_USERS', '').split(',') 
        if uid.strip().isdigit()
    ]
    DEBUG_MODE: bool = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
    
    # Rate Limiting & Caching
    COINGECKO_CACHE_TTL: int = int(os.getenv('COINGECKO_CACHE_TTL', '60'))
    NEWS_CACHE_TTL: int = int(os.getenv('NEWS_CACHE_TTL', '300'))
    NBU_CACHE_TTL: int = int(os.getenv('NBU_CACHE_TTL', '3600'))
    USER_RATE_LIMIT: int = int(os.getenv('USER_RATE_LIMIT', '30'))
    
    # API Endpoints
    NBU_API_BASE: str = 'https://bank.gov.ua/NBUStatService/v1/'
    ECB_RSS_URL: str = 'https://www.ecb.europa.eu/rss/press.html'
    IMF_RSS_URL: str = 'https://www.imf.org/en/News/RSS'
    COINGECKO_API_BASE: str = 'https://api.coingecko.com/api/v3'
    
    @classmethod
    def validate(cls) -> List[str]:
        """Validate required configuration"""
        errors = []
        
        if not cls.TELEGRAM_BOT_TOKEN:
            errors.append("TELEGRAM_BOT_TOKEN is required")
        
        if not cls.EMERGENT_LLM_KEY:
            errors.append("EMERGENT_LLM_KEY is missing (AI features will not work)")
        
        return errors
    
    @classmethod
    def is_premium_test_user(cls, user_id: int) -> bool:
        """Check if user should get free premium for testing"""
        if cls.PREMIUM_TESTING_MODE:
            return True
        return user_id in cls.PREMIUM_TEST_USERS
    
    @classmethod
    def get_digest_times(cls) -> tuple:
        """Get morning and evening digest times"""
        return (cls.MORNING_DIGEST_TIME, cls.EVENING_DIGEST_TIME)


# Create singleton instance
config = Config()

# Validate on import
validation_errors = config.validate()
if validation_errors:
    import logging
    logger = logging.getLogger(__name__)
    for error in validation_errors:
        logger.warning(f"Configuration warning: {error}")
