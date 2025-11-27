from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")  # Ignore MongoDB's _id field
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

class BotStats(BaseModel):
    total_users: int
    premium_users: int
    free_users: int
    total_revenue: float
    recent_users: List[dict]


# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Crypto Analysis Bot API"}

@app.get("/healthz")
async def healthz():
    return {"ok": True}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)
    
    # Convert to dict and serialize datetime to ISO string for MongoDB
    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    
    _ = await db.status_checks.insert_one(doc)
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    # Exclude MongoDB's _id field from the query results
    status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)
    
    # Convert ISO string timestamps back to datetime objects
    for check in status_checks:
        if isinstance(check['timestamp'], str):
            check['timestamp'] = datetime.fromisoformat(check['timestamp'])
    
    return status_checks

@api_router.get("/bot/stats")
async def get_bot_stats():
    """Get bot statistics"""
    try:
        # Total users
        total_users = await db.users.count_documents({})
        
        # Premium users
        premium_subs = await db.subscriptions.find({}).to_list(1000)
        active_premium = 0
        total_revenue = 0
        
        for sub in premium_subs:
            expires_at = sub.get('expires_at')
            if expires_at:
                if isinstance(expires_at, str):
                    expires_at = datetime.fromisoformat(expires_at)
                if expires_at > datetime.now(timezone.utc):
                    active_premium += 1
                    # Each subscription is $5
                    total_revenue += 5
        
        free_users = total_users - active_premium
        
        # Recent users
        recent_users = await db.users.find({}, {"_id": 0}).sort("created_at", -1).limit(10).to_list(10)
        
        return {
            "total_users": total_users,
            "premium_users": active_premium,
            "free_users": free_users,
            "total_revenue": total_revenue,
            "recent_users": recent_users
        }
    except Exception as e:
        logging.error(f"Error fetching bot stats: {e}")
        raise HTTPException(status_code=500, detail="Error fetching statistics")

@api_router.get("/bot/users")
async def get_bot_users():
    """Get all bot users"""
    try:
        users = await db.users.find({}, {"_id": 0}).to_list(1000)
        return users
    except Exception as e:
        logging.error(f"Error fetching users: {e}")
        raise HTTPException(status_code=500, detail="Error fetching users")

@api_router.get("/bot/subscriptions")
async def get_subscriptions():
    """Get all subscriptions"""
    try:
        subscriptions = await db.subscriptions.find({}, {"_id": 0}).to_list(1000)
        return subscriptions
    except Exception as e:
        logging.error(f"Error fetching subscriptions: {e}")
        raise HTTPException(status_code=500, detail="Error fetching subscriptions")

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
