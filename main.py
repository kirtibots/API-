# main.py
import threading
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from auth import validate_api_key
import requests
from config import COBALT_API_URL
import bot

app = FastAPI(title="KIRTI_BOTS Custom API Server")

def run_bot():
    print("Starting KIRTI_BOTS Telegram Bot Thread...")
    bot.bot.infinity_polling()

@app.on_event("startup")
def startup_event():
    # टेलीग्राम बोट को अलग बैकग्राउंड थ्रेड में चलाना ताकि API सर्वर डिस्टर्ब न हो
    threading.Thread(target=run_bot, daemon=True).start()

class DownloadPayload(BaseModel):
    url: str
    mode: str = "audio"  # डिफ़ॉल्ट 'audio' रहेगा, वीडियो के लिए 'video' भेजें

@app.get("/")
def home():
    return {"status": "KIRTI_BOTS API & Bot are live and running successfully!"}

@app.post("/api/v1/fetch")
async def get_link(payload: DownloadPayload, api_key: str = Depends(validate_api_key)):
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    data = {"url": payload.url, "downloadMode": payload.mode}
    
    # अगर मोड 'audio' है तो mp3 फॉर्मेट पास करना
    if payload.mode == "audio":
        data["audioFormat"] = "mp3"
        
    try:
        response = requests.post(COBALT_API_URL, json=data, headers=headers)
        if response.status_code == 200:
            return {"success": True, "link": response.json().get("url")}
        return {"success": False, "error": f"Error code from Core Engine: {response.status_code}"}
    except Exception as e:
        return {"success": False, "error": str(e)}
