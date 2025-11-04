import logging
import os
from datetime import datetime, timezone, timedelta

logger = logging.getLogger(__name__)


class PaymentService:
    """Service for handling Telegram Stars payments and subscriptions"""
    
    def __init__(self, db):
        self.db = db
    
    def _is_premium_test_user(self, telegram_id):
        """Check if user should get free premium for testing"""
        # Check if testing mode is enabled for all users
        testing_mode = os.getenv('PREMIUM_TESTING_MODE', 'false').lower() == 'true'
        if testing_mode:
            return True
        
        # Check if user is in test users list
        test_users_str = os.getenv('PREMIUM_TEST_USERS', '')
        if test_users_str:
            test_users = [int(uid.strip()) for uid in test_users_str.split(',') if uid.strip().isdigit()]
            return telegram_id in test_users
        
        return False
    
    async def check_subscription(self, telegram_id):
        """Check if user has active premium subscription"""
        try:
            # Check testing mode first
            if self._is_premium_test_user(telegram_id):
                logger.info(f"User {telegram_id} has free premium (testing mode)")
                return True
            
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
