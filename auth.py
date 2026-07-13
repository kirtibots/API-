# auth.py
from fastapi import HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from pymongo import MongoClient  # 👈 मोंगोडीबी इम्पोर्ट किया
from config import MONGO_URL      # 👈 मोंगो यूआरएल इम्पोर्ट किया

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

# 🌐 MongoDB कनेक्शन सेटअप
try:
    client = MongoClient(MONGO_URL)
    db_mongo = client["marco_bot_db"]       # बोट वाला सेम डेटाबेस
    users_collection = db_mongo["users"]    # बोट वाला सेम कलेक्शन
    print("✅ Auth MongoDB Connected Successfully!")
except Exception as e:
    print(f"❌ Auth MongoDB Connection Error: {e}")

def load_keys():
    """मोंगोडीबी से सभी यूज़र्स की एक्टिव API Keys की लिस्ट निकालना"""
    try:
        # डेटाबेस से सिर्फ 'key' फील्ड निकालना ताकि प्रोसेस फास्ट हो
        all_users = users_collection.find({}, {"key": 1, "_id": 0})
        return [u["key"] for u in all_users if "key" in u]
    except Exception as e:
        print(f"Error loading keys from MongoDB: {e}")
        return []

async def validate_api_key(api_key_from_header: str = Depends(api_key_header)):
    valid_keys = load_keys()
    
    # चेक करें कि क्या भेजी गई की (Key) हमारे मोंगोडीबी डेटाबेस में मौजूद है
    if api_key_from_header in valid_keys:
        return api_key_from_header
        
    raise HTTPException(
        status_code=403, 
        detail="Unauthorized: Invalid or Expired MARCO_BOTS API Key"
        )
    
