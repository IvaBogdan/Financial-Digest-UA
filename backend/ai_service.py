import os
import logging
from emergentintegrations.llm.chat import LlmChat, UserMessage
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]


class AIService:
    """Service for AI-powered analysis and chat using OpenAI GPT-5"""
    
    def __init__(self):
        self.api_key = os.environ.get('EMERGENT_LLM_KEY')
        self.model_provider = "openai"
        self.model_name = "gpt-5"
    
    def get_chat_instance(self, session_id, system_message):
        """Get LlmChat instance"""
        chat = LlmChat(
            api_key=self.api_key,
            session_id=session_id,
            system_message=system_message
        )
        chat.with_model(self.model_provider, self.model_name)
        return chat
    
    async def analyze_asset(self, symbol, crypto_data):
        """Analyze a crypto asset with AI"""
        try:
            # Create analysis prompt
            price = crypto_data['price']
            market_cap = crypto_data['market_cap']
            volume = crypto_data['volume_24h']
            change_24h = crypto_data['price_change_24h']
            change_7d = crypto_data['price_change_7d']
            change_30d = crypto_data['price_change_30d']
            ath = crypto_data['ath']
            ath_change = crypto_data['ath_change']
            
            prompt = f"""Analyze the cryptocurrency {symbol} ({crypto_data['name']}) with the following data:

Current Price: ${price:,.8f}
Market Cap: ${market_cap:,.0f}
24h Volume: ${volume:,.0f}
24h Change: {change_24h:.2f}%
7d Change: {change_7d:.2f}%
30d Change: {change_30d:.2f}%
All-Time High: ${ath:,.2f} (Currently {ath_change:.2f}% from ATH)

Provide a comprehensive analysis including:
1. Current market sentiment and trend
2. Key factors affecting the price
3. Short-term outlook (1-7 days)
4. Medium-term outlook (1-4 weeks)
5. Important support and resistance levels
6. Risk factors to watch

Keep the analysis concise (under 400 words) and actionable."""
            
            system_message = "You are an expert cryptocurrency analyst with deep knowledge of blockchain technology, market dynamics, and technical analysis. Provide clear, data-driven insights."
            
            chat = self.get_chat_instance(f"analysis_{symbol}", system_message)
            user_message = UserMessage(text=prompt)
            response = await chat.send_message(user_message)
            
            # Format response
            result = f"""🔍 **Detailed Analysis: {crypto_data['name']} ({symbol})**

💵 **Current Price:** ${price:,.8f}
📊 **Market Cap:** ${market_cap:,.0f}
📈 **24h Volume:** ${volume:,.0f}

{response}

⚠️ *This analysis is for informational purposes only and should not be considered financial advice.*
"""
            
            return result
            
        except Exception as e:
            logger.error(f"Error in AI analysis: {e}")
            raise
    
    async def chat(self, user_id, message):
        """Handle conversational chat with AI"""
        try:
            # Load chat history from database
            chat_history = await db.chat_history.find_one({"user_id": user_id})
            
            system_message = """You are a helpful AI assistant specializing in cryptocurrency and blockchain technology. 
You can answer questions about crypto markets, provide analysis, explain concepts, and discuss trading strategies. 
Be conversational, helpful, and informative. Keep responses concise (under 300 words)."""
            
            chat = self.get_chat_instance(f"user_{user_id}", system_message)
            user_message = UserMessage(text=message)
            response = await chat.send_message(user_message)
            
            # Save chat history
            timestamp = datetime.now(timezone.utc).isoformat()
            
            if chat_history:
                await db.chat_history.update_one(
                    {"user_id": user_id},
                    {
                        "$push": {
                            "messages": {
                                "$each": [
                                    {"role": "user", "content": message, "timestamp": timestamp},
                                    {"role": "assistant", "content": response, "timestamp": timestamp}
                                ]
                            }
                        },
                        "$set": {"updated_at": timestamp}
                    }
                )
            else:
                await db.chat_history.insert_one({
                    "user_id": user_id,
                    "messages": [
                        {"role": "user", "content": message, "timestamp": timestamp},
                        {"role": "assistant", "content": response, "timestamp": timestamp}
                    ],
                    "created_at": timestamp,
                    "updated_at": timestamp
                })
            
            return response
            
        except Exception as e:
            logger.error(f"Error in AI chat: {e}")
            raise
