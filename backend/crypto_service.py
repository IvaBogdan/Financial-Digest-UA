import aiohttp
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class CryptoService:
    """Service for crypto market data using CoinGecko API"""
    
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.session = None
    
    async def get_session(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def get_market_overview(self):
        """Get overview of top cryptocurrencies"""
        try:
            session = await self.get_session()
            
            # Get global market data
            async with session.get(f"{self.base_url}/global") as response:
                global_data = await response.json()
            
            # Get top 10 cryptocurrencies
            params = {
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': 10,
                'page': 1,
                'sparkline': False,
                'price_change_percentage': '24h,7d'
            }
            
            async with session.get(f"{self.base_url}/coins/markets", params=params) as response:
                coins = await response.json()
            
            # Format market overview
            market_cap = global_data['data']['total_market_cap']['usd']
            volume = global_data['data']['total_volume']['usd']
            btc_dominance = global_data['data']['market_cap_percentage'].get('btc', 0)
            
            result = f"""📊 **Market Overview**

💰 Total Market Cap: ${market_cap:,.0f}
📈 24h Volume: ${volume:,.0f}
₿ BTC Dominance: {btc_dominance:.1f}%

🔝 **Top 10 Cryptocurrencies:**

"""
            
            for i, coin in enumerate(coins, 1):
                name = coin['name']
                symbol = coin['symbol'].upper()
                price = coin['current_price']
                change_24h = coin.get('price_change_percentage_24h', 0)
                change_7d = coin.get('price_change_percentage_7d_in_currency', 0)
                
                change_icon = "🟢" if change_24h > 0 else "🔴"
                
                result += f"{i}. **{name}** ({symbol})\n"
                result += f"   💵 ${price:,.2f} | {change_icon} {change_24h:+.2f}% (24h) | {change_7d:+.2f}% (7d)\n\n"
            
            return result
            
        except Exception as e:
            logger.error(f"Error fetching market overview: {e}")
            raise
    
    async def get_price(self, symbol):
        """Get price for a specific cryptocurrency"""
        try:
            session = await self.get_session()
            
            # Search for coin
            async with session.get(f"{self.base_url}/search", params={'query': symbol}) as response:
                search_data = await response.json()
            
            if not search_data.get('coins'):
                return f"❌ Could not find cryptocurrency: {symbol}"
            
            coin_id = search_data['coins'][0]['id']
            
            # Get coin data
            params = {
                'ids': coin_id,
                'vs_currencies': 'usd',
                'include_24hr_change': 'true',
                'include_7d_change': 'true',
                'include_market_cap': 'true',
                'include_24hr_vol': 'true'
            }
            
            async with session.get(f"{self.base_url}/simple/price", params=params) as response:
                price_data = await response.json()
            
            coin_data = price_data[coin_id]
            price = coin_data['usd']
            change_24h = coin_data.get('usd_24h_change', 0)
            market_cap = coin_data.get('usd_market_cap', 0)
            volume = coin_data.get('usd_24h_vol', 0)
            
            change_icon = "🟢" if change_24h > 0 else "🔴"
            
            result = f"""💎 **{symbol.upper()} Price**

💵 Price: ${price:,.8f}
{change_icon} 24h Change: {change_24h:+.2f}%
📊 Market Cap: ${market_cap:,.0f}
📈 24h Volume: ${volume:,.0f}
"""
            
            return result
            
        except Exception as e:
            logger.error(f"Error fetching price for {symbol}: {e}")
            raise
    
    async def get_detailed_data(self, symbol):
        """Get detailed data for AI analysis"""
        try:
            session = await self.get_session()
            
            # Search for coin
            async with session.get(f"{self.base_url}/search", params={'query': symbol}) as response:
                search_data = await response.json()
            
            if not search_data.get('coins'):
                raise ValueError(f"Could not find cryptocurrency: {symbol}")
            
            coin_id = search_data['coins'][0]['id']
            
            # Get detailed coin data
            params = {
                'localization': 'false',
                'tickers': 'false',
                'community_data': 'true',
                'developer_data': 'true',
                'sparkline': 'false'
            }
            
            async with session.get(f"{self.base_url}/coins/{coin_id}", params=params) as response:
                coin_data = await response.json()
            
            # Get market chart (7 days)
            async with session.get(
                f"{self.base_url}/coins/{coin_id}/market_chart",
                params={'vs_currency': 'usd', 'days': '7'}
            ) as response:
                chart_data = await response.json()
            
            return {
                'name': coin_data['name'],
                'symbol': coin_data['symbol'].upper(),
                'price': coin_data['market_data']['current_price']['usd'],
                'market_cap': coin_data['market_data']['market_cap']['usd'],
                'volume_24h': coin_data['market_data']['total_volume']['usd'],
                'price_change_24h': coin_data['market_data'].get('price_change_percentage_24h', 0),
                'price_change_7d': coin_data['market_data'].get('price_change_percentage_7d', 0),
                'price_change_30d': coin_data['market_data'].get('price_change_percentage_30d', 0),
                'ath': coin_data['market_data']['ath']['usd'],
                'ath_change': coin_data['market_data']['ath_change_percentage']['usd'],
                'atl': coin_data['market_data']['atl']['usd'],
                'circulating_supply': coin_data['market_data'].get('circulating_supply', 0),
                'max_supply': coin_data['market_data'].get('max_supply'),
                'description': coin_data.get('description', {}).get('en', '')[:500],
                'chart_data': chart_data['prices'][-7:],  # Last 7 data points
            }
            
        except Exception as e:
            logger.error(f"Error fetching detailed data for {symbol}: {e}")
            raise
