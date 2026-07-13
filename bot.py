# bot.py
import json
import secrets
import requests
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import TELEGRAM_BOT_TOKEN, DB_FILE, OWNER_ID, UPDATE_CHANNEL, SUPPORT_GROUP

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

def load_db():
    try:
        with open(DB_FILE, "r") as f:
            data = json.load(f)
            if "users" not in data:
                return {"users": {}}
            return data
    except:
        return {"users": {}}

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# 🛠️ बैकएंड API का लाइव स्टेटस चेक करने वाला फंक्शन
def check_api_status():
    try:
        response = requests.get("https://api.cobalt.tools/", timeout=5)
        if response.status_code == 200:
            return "🟢 ONLINE (Fast & Stable)"
        else:
            return "🟡 LEAPING (Slowing Down)"
    except:
        return "🔴 OFFLINE (Maintenance)"

# 🎛️ सभी बटन्स (Owner, Update, Support) एक साथ यहाँ सेट हैं
def get_main_keyboard():
    markup = InlineKeyboardMarkup()
    
    ch_name = UPDATE_CHANNEL.replace("@", "").strip()
    sp_name = SUPPORT_GROUP.replace("@", "").strip()
    
    btn_owner = InlineKeyboardButton("👑 Owner / Developer", url=f"https://t.me/{ch_name}")
    btn_update = InlineKeyboardButton("📢 Update Channel", url=f"https://t.me/{ch_name}")
    btn_support = InlineKeyboardButton("💬 Support Group", url=f"https://t.me/{sp_name}")
    
    markup.row(btn_owner)
    markup.row(btn_update, btn_support)
    return markup

# 🚀 /start और /keygen कमांड्स हैंडलर
@bot.message_handler(commands=['start', 'keygen'])
def send_welcome(message):
    user_id = str(message.from_user.id)
    username = message.from_user.username or "User"
    
    db = load_db()
    
    if user_id in db["users"]:
        api_key = db["users"][user_id]["key"]
    else:
        api_key = f"MARCO_{secrets.token_hex(12).upper()}"
        db["users"][user_id] = {
            "username": username,
            "key": api_key
        }
        save_db(db)

    api_status = check_api_status()

    # ✨ आपका कस्टम प्रीमियम वेलकम मैसेज आपके अपने नाम की URL के साथ ✨
    welcome_text = (
        f"👋 *Hello @{username}*\n\n"
        f"Welcome to *MARCO_BOTS API System*! I am here to provide you with your personal, high-speed API Key for seamless music and video downloading. 🚀\n\n"
        f"🤖 *API Status:* `{api_status}`\n"
        f"🔑 *Your API Key:* `{api_key}`\n\n"
        f"🌐 *API URL:* `https://api.cobalt.tools/api/json`\n\n"
        f"📌 *Available Commands:*\n"
        f"🔹 `/keygen` - Generate or view your 28-days API key\n"
        f"🔹 `/stats` - View your API key usage stats 📊\n\n"
        f"💬 *Note:* Copy this key and paste it into your Music Bot's configuration Headers as `X-API-Key`. Enjoy uninterrupted service!"
    )
    
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=get_main_keyboard())

# 📊 ओनर कमांड: कुल यूज़र्स और चाबियाँ देखने के लिए
@bot.message_handler(commands=['stats'])
def show_stats(message):
    if message.from_user.id != OWNER_ID:
        return

    db = load_db()
    total_users = len(db["users"])
    
    stats_text = (
        f"📊 *MARCO_BOTS Live Statistics*\n\n"
        f"👥 Total Registered Users: `{total_users}`\n"
        f"🔑 Total Generated Keys: `{total_users}`"
    )
    bot.reply_to(message, stats_text, parse_mode="Markdown")

# 📢 ओनर कमांड: सभी यूज़र्स को एक साथ मैसेज भेजने के लिए
@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    if message.from_user.id != OWNER_ID:
        return
        
    text_to_send = message.text.replace("/broadcast", "").strip()
    
    if not text_to_send:
        bot.reply_to(message, "❌ कृपया ब्रॉडकास्ट करने के लिए कोई मैसेज लिखें!\nउदाहरण: `/broadcast Hello Users!`", parse_mode="Markdown")
        return
        
    db = load_db()
    all_users = db["users"].keys()
    
    bot.reply_to(message, f"📢 `{len(all_users)}` यूज़र्स को मैसेज भेजना शुरू कर दिया है...", parse_mode="Markdown")
    
    success_count = 0
    fail_count = 0
    
    for u_id in all_users:
        try:
            bot.send_message(chat_id=int(u_id), text=text_to_send)
            success_count += 1
        except Exception:
            fail_count += 1
            
    bot.send_message(
        message.chat.id, 
        f"✅ *Broadcast Finished!*\n\n"
        f"🚀 सफल संदेश: `{success_count}`\n"
        f"❌ असफल (बॉट ब्लॉक): `{fail_count}`", 
        parse_mode="Markdown"
    )

if __name__ == "__main__":
    bot.infinity_polling()
    
