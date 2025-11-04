import logging
from datetime import datetime, timezone, timedelta

logger = logging.getLogger(__name__)


class PaymentService:
    """Service for handling Telegram Stars payments and subscriptions"""
    
    def __init__(self, db):
        self.db = db
    
    async def check_subscription(self, telegram_id):
        """Check if user has active premium subscription"""
        try:
            subscription = await self.db.subscriptions.find_one({"telegram_id": telegram_id})
            
            if not subscription:
                return False
            
            expires_at = subscription.get('expires_at')
            if not expires_at:
                return False
            
            # Parse datetime if string
            if isinstance(expires_at, str):
                expires_at = datetime.fromisoformat(expires_at)
            
            # Check if subscription is still valid
            return expires_at > datetime.now(timezone.utc)
            
        except Exception as e:
            logger.error(f"Error checking subscription: {e}")
            return False
    
    async def activate_subscription(self, telegram_id, payment_info):
        """Activate premium subscription after successful payment"""
        try:
            # Calculate expiration (30 days from now)
            expires_at = datetime.now(timezone.utc) + timedelta(days=30)
            
            # Check if subscription exists
            existing_sub = await self.db.subscriptions.find_one({"telegram_id": telegram_id})
            
            if existing_sub:
                # Update existing subscription
                await self.db.subscriptions.update_one(
                    {"telegram_id": telegram_id},
                    {
                        "$set": {
                            "expires_at": expires_at.isoformat(),
                            "updated_at": datetime.now(timezone.utc).isoformat(),
                            "payment_info": {
                                "currency": payment_info.currency,
                                "total_amount": payment_info.total_amount,
                                "telegram_payment_charge_id": payment_info.telegram_payment_charge_id,
                            }
                        }
                    }
                )
            else:
                # Create new subscription
                await self.db.subscriptions.insert_one({
                    "telegram_id": telegram_id,
                    "tier": "premium",
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "expires_at": expires_at.isoformat(),
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                    "payment_info": {
                        "currency": payment_info.currency,
                        "total_amount": payment_info.total_amount,
                        "telegram_payment_charge_id": payment_info.telegram_payment_charge_id,
                    }
                })
            
            # Update user tier
            await self.db.users.update_one(
                {"telegram_id": telegram_id},
                {"$set": {"subscription_tier": "premium"}}
            )
            
            logger.info(f"Activated premium subscription for user {telegram_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error activating subscription: {e}")
            return False
