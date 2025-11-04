import aiohttp
import os
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


class NewsService:
    """Service for crypto and financial news aggregation"""
    
    def __init__(self):
        self.cryptopanic_key = os.environ.get('CRYPTOPANIC_API_KEY', '')
        self.newsapi_key = os.environ.get('NEWSAPI_KEY', '')
        self.session = None
    
    async def get_session(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def get_cryptopanic_news(self, limit=5):
        """Get news from CryptoPanic"""
        if not self.cryptopanic_key:
            return []
        
        try:
            session = await self.get_session()
            url = "https://cryptopanic.com/api/v1/posts/"
            params = {
                'auth_token': self.cryptopanic_key,
                'public': 'true',
                'kind': 'news',
                'filter': 'important'
            }
            
            async with session.get(url, params=params) as response:
                data = await response.json()
                return data.get('results', [])[:limit]
        
        except Exception as e:
            logger.error(f"Error fetching CryptoPanic news: {e}")
            return []
    
    async def get_newsapi_articles(self, limit=5):
        """Get crypto news from NewsAPI"""
        if not self.newsapi_key:
            return []
        
        try:
            session = await self.get_session()
            url = "https://newsapi.org/v2/everything"
            params = {
                'apiKey': self.newsapi_key,
                'q': 'cryptocurrency OR bitcoin OR ethereum',
                'sortBy': 'publishedAt',
                'language': 'en',
                'pageSize': limit
            }
            
            async with session.get(url, params=params) as response:
                data = await response.json()
                return data.get('articles', [])[:limit]
        
        except Exception as e:
            logger.error(f"Error fetching NewsAPI articles: {e}")
            return []
    
    async def get_latest_news(self):
        """Get latest crypto news from multiple sources"""
        cryptopanic_news = await self.get_cryptopanic_news(3)
        newsapi_articles = await self.get_newsapi_articles(3)
        
        result = "📰 **Latest Crypto News**\n\n"
        
        if cryptopanic_news:
            result += "**🔥 Top Stories (CryptoPanic)**\n\n"
            for i, news in enumerate(cryptopanic_news, 1):
                title = news.get('title', 'No title')
                url = news.get('url', '')
                source = news.get('source', {}).get('title', 'Unknown')
                published = news.get('published_at', '')
                
                result += f"{i}. **{title}**\n"
                result += f"   📅 {published[:10]} | 📰 {source}\n"
                result += f"   🔗 {url}\n\n"
        
        if newsapi_articles:
            result += "\n**📈 Financial News (NewsAPI)**\n\n"
            for i, article in enumerate(newsapi_articles, 1):
                title = article.get('title', 'No title')
                url = article.get('url', '')
                source = article.get('source', {}).get('name', 'Unknown')
                published = article.get('publishedAt', '')[:10]
                
                result += f"{i}. **{title}**\n"
                result += f"   📅 {published} | 📰 {source}\n"
                result += f"   🔗 {url}\n\n"
        
        if not cryptopanic_news and not newsapi_articles:
            result += "📡 No news available at the moment. Please check back later.\n"
            result += "\n💡 Tip: Make sure API keys are configured for news sources."
        
        return result
    
    async def get_daily_digest(self):
        """Get news digest for daily broadcast"""
        cryptopanic_news = await self.get_cryptopanic_news(5)
        newsapi_articles = await self.get_newsapi_articles(5)
        
        result = "📰 **Top News Today**\n\n"
        
        all_news = []
        
        for news in cryptopanic_news:
            all_news.append({
                'title': news.get('title', ''),
                'url': news.get('url', ''),
                'source': news.get('source', {}).get('title', 'CryptoPanic')
            })
        
        for article in newsapi_articles:
            all_news.append({
                'title': article.get('title', ''),
                'url': article.get('url', ''),
                'source': article.get('source', {}).get('name', 'NewsAPI')
            })
        
        for i, news in enumerate(all_news[:8], 1):
            result += f"{i}. {news['title']}\n"
            result += f"   📰 {news['source']} | 🔗 {news['url']}\n\n"
        
        if not all_news:
            result += "No news available for today's digest.\n"
        
        return result
