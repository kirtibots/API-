# bot.py
import secrets
import requests
import telebot
import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient  # 👈 मोंगोडीबी इम्पोर्ट किया
from config import TELEGRAM_BOT_TOKEN, OWNER_ID, LOG_GROUP_ID, UPDATE_CHANNEL, SUPPORT_GROUP, MONGO_URL

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# 🌐 MongoDB कनेक्शन सेटअप
try:
    client = MongoClient(MONGO_URL)
    db_mongo = client["marco_bot_db"]       # डेटाबेस का नाम
    users_collection = db_mongo["users"]    # कलेक्शन (टेबल) का नाम
    print("✅ MongoDB Connected Successfully!")
except Exception as e:
    print(f"❌ MongoDB Connection Error: {e}")

def load_db():
    try:
        all_users = users_collection.find()
        user_dict = {}
        for u in all_users:
            if "user_id" in u:
                user_dict[str(u["user_id"])] = {
                    "username": u.get("username", "User"),
                    "key": u.get("key", ""),
                    "created_at": u.get("created_at", datetime.date.today().isoformat())
                }
        return {"users": user_dict}
    except Exception as e:
        print(f"Load DB Error: {e}")
        return {"users": {}}

def save_db_user(user_id, user_data):
    try:
        users_collection.update_one(
            {"user_id": str(user_id)},
            {"$set": {
                "username": user_data["username"],
                "key": user_data["key"],
                "created_at": user_data["created_at"]
            }},
            upsert=True
        )
    except Exception as e:
        print(f"Save DB Error: {e}")

# 📣 लॉगर ग्रुप में मैसेज भेजने का फंक्शन
def send_log(message_text):
    if LOG_GROUP_ID and str(LOG_GROUP_ID) != "0":
        try:
            bot.send_message(int(LOG_GROUP_ID), message_text, parse_mode="Markdown")
        except Exception as e:
            print(f"❌ CRITICAL LOG ERROR: {e}")

# 🛠️ बैकएंड API का लाइव 触发
def check_api_status():
    try:
        response = requests.get("https://api.cobalt.tools/", timeout=5)
        if response.status_code == 200:
            return "🟢 ONLINE (Fast & Stable)"
        else:
            return "🟡 LEAPING (Slowing Down)"
    except:
        return "🔴 OFFLINE (Maintenance)"

# 28 दिन वाली लॉजिक के साथ नई की जनरेट करने का हेल्पर फंक्शन
def generate_new_key(user_id, user_name, db, log_reason="New User"):
    api_key = f"MARCO_{secrets.token_hex(12).upper()}"
    today = datetime.date.today().isoformat()
    
    user_data = {
        "username": user_name,  # यहाँ अब यूजर का असली नाम सेव होगा
        "key": api_key,
        "created_at": today
    }
    
    db["users"][user_id] = user_data
    save_db_user(user_id, user_data)
    
    # 📝 लॉगर ग्रुप में अलर्ट (Name के साथ)
    log_msg = (
        f"🔑 *New API Key Generated!*\n\n"
        f"👤 *Name:* {user_name}\n"
        f"🆔 *ID:* `{user_id}`\n"
        f"🔑 *Key:* `{api_key}`\n"
        f"📌 *Reason:* {log_reason}"
    )
    send_log(log_msg)
    
    return api_key

# 🎛️ सभी बटन्स (Owner, Update, Support)
def get_main_keyboard():
    markup = InlineKeyboardMarkup()
    
    def clean_tg_link(variable_value, default_fallback, is_id=False):
        if not variable_value:
            return f"https://t.me/{default_fallback}"
        if is_id:
            clean_val = str(variable_value).strip()
            clean_val = ''.join(filter(str.isdigit, clean_val))
            if clean_val:
                return f"tg://user?id={clean_val}"
            return f"https://t.me/{default_fallback}"
        clean_value = str(variable_value).replace("@", "").replace("https://t.me/", "").replace("http://t.me/", "").strip()
        return f"https://t.me/{clean_value}"

    owner_link = clean_tg_link(OWNER_ID, "Telegram", is_id=True)
    update_link = clean_tg_link(UPDATE_CHANNEL, "Telegram")
    support_link = clean_tg_link(SUPPORT_GROUP, "Telegram")
    
    btn_owner = InlineKeyboardButton("⛥ 𝗞ʀ𝛊֟፝͝ꜱʜnᴀ ⛥", url=owner_link)
    btn_update = InlineKeyboardButton("📢 Update", url=update_link)
    btn_support = InlineKeyboardButton("💬 Support", url=support_link)
    
    markup.row(btn_owner)
    markup.row(btn_update, btn_support)
    return markup

# 🚀 1. केवल /start कमांड हैंडलर (Welcome Message)
@bot.message_handler(commands=['start'])
def send_start_welcome(message):
    user_id = str(message.from_user.id)
    user_name = message.from_user.first_name if message.from_user.first_name else "User"
    
    # 📝 लॉगर ग्रुप में सिर्फ स्टार्ट करने का अलर्ट भेजना (Name के साथ)
    start_log = (
        f"👋 *User Started Bot*\n\n"
        f"👤 *Name:* {user_name}\n"
        f"🆔 *ID:* `{user_id}`\n"
        f"📅 *Time:* `{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`"
    )
    send_log(start_log)
    
    welcome_text = (
        f"👋 *Hello {user_name}*,\n\n"
        f"Welcome to *krishna_BOTS API System*! 🚀\n\n"
        f"Main aapko high-speed aur personal API Keys provide karunga jisse aap apne Music bots me bina kisi dikkat ke high-quality gaane aur videos play kar payenge.\n\n"
        f"📌 *Apni API Key nikalne ke liye niche diye gaye command ka use kare:*\n"
        f"👉 `/keygen` - Generate or View your 28-Days API Key\n\n"
        f"any help to  Support group join!"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=get_main_keyboard())

# 🔑 2. केवल /keygen कमांड हैंडलर (अलग Key Generation Message)
@bot.message_handler(commands=['keygen'])
def handle_key_generation(message):
    user_id = str(message.from_user.id)
    user_name = message.from_user.first_name if message.from_user.first_name else "User"
    
    db = load_db()
    today = datetime.date.today()
    
    if user_id in db["users"]:
        created_at_str = db["users"][user_id].get("created_at", today.isoformat())
        try:
            created_at = datetime.date.fromisoformat(created_at_str)
        except:
            created_at = today
        days_passed = (today - created_at).days
        
        if days_passed >= 28:
            api_key = generate_new_key(user_id, user_name, db, log_reason="Key Expired (28 Days Completed)")
            status_text = "🔄 Aapki purani key 28 din pure hone par expire ho gayi thi. Nayi API Key generate kar di gayi hai!"
        else:
            api_key = db["users"][user_id]["key"]
            remaining_days = 28 - days_passed
            status_text = f"⏳ Aapki yeh API Key abhi `{remaining_days} din` aur valid hai."
    else:
        api_key = generate_new_key(user_id, user_name, db, log_reason="First Time Registration")
        status_text = "🎉 Aapki pahli 28-days API Key successfully generate ho gayi hai!"

    api_status = check_api_status()

    keygen_text = (
        f"🔑 *MARCO_BOTS API KEY MANAGER* 🔑\n\n"
        f"👤 *User Name:* {first_name}\n"
        f"📢 *Key Status:* {status_text}\n"
        f"🤖 *System Status:* `{api_status}`\n"
        f"🌐 *API URL:* `https://marco-yt-api-production.up.railway.app/api/json`\n\n"
        f"💬 *Note:* Is key ko copy kare aur apne Music Bot ke Environment Variables / Config Headers me `X-API-Key` ke roop me paste kar dein. Enjoy seamless downloading! 🚀"
    )
    bot.send_message(message.chat.id, keygen_text, parse_mode="Markdown", reply_markup=get_main_keyboard())

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
        bot.reply_to(message, "❌ Please write a message to broadcast!\nExample: `/broadcast Hello Users!`", parse_mode="Markdown")
        return
    db = load_db()
    all_users = db["users"].keys()
    bot.reply_to(message, f"📢 `{len(all_users)}` Users ko message bhejna shuru kar diya hai...", parse_mode="Markdown")
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
        f"🚀 Success: `{success_count}`\n"
        f"❌ Failed (Bot Blocked): `{fail_count}`", 
        parse_mode="Markdown"
    )

if __name__ == "__main__":
    bot.infinity_polling()
    
