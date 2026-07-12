# auth.py
import json
from fastapi import HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from config import DB_FILE

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def load_keys():
    try:
        with open(DB_FILE, "r") as f:
            data = json.load(f)
            if "users" in data:
                # डेटाबेस से सभी यूज़र्स की जनरेट की हुई कीज़ (Keys) की लिस्ट निकालना
                return [user_info["key"] for user_info in data["users"].values()]
            return []
    except:
        return []

async def validate_api_key(api_key_from_header: str = Depends(api_key_header)):
    valid_keys = load_keys()
    
    # चेक करें कि क्या भेजी गई की (Key) हमारे डेटाबेस में मौजूद है
    if api_key_from_header in valid_keys:
        return api_key_from_header
        
    raise HTTPException(
        status_code=403, 
        detail="Unauthorized: Invalid or Expired MARCO_BOTS API Key"
  )
  
