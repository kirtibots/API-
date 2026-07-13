# bot.py
import json
import secrets
import requests
import telebot
import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import TELEGRAM_BOT_TOKEN, DB_FILE, OWNER_ID, LOG_GROUP_ID, UPDATE_CHANNEL, SUPPORT_GROUP

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

# 📣 लॉगर ग्रुप में मैसेज भेजने का फंक्शन
def send_log(message_text):
    if LOG_GROUP_ID != 0:
        try:
            bot.send_message(LOG_GROUP_ID, message_text, parse_mode="Markdown")
        except Exception as e:
            print(f"Log Error: {e}")

# 🛠️ बैकएंड API का लाइव触发
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
def generate_new_key(user_id, username, db, log_reason="New User"):
    api_key = f"MARCO_{secrets.token_hex(12).upper()}"
    today = datetime.date.today().isoformat()
    db["users"][user_id] = {
        "username": username,
        "key": api_key,
        "created_at": today
    }
    save_db(db)
    
    # 📝 लॉगर ग्रुप में की जनरेशन का अलर्ट भेजना
    log_msg = (
        f"🔑 *New API Key Generated!*\n\n"
        f"👤 *User:* @{username}\n"
        f"🆔 *ID:* `{user_id}`\n"
        f"🔑 *Key:* `{api_key}`\n"
        f"📌 *Reason:* {log_reason}"
    )
    send_log(log_msg)
    
    return api_key

# 🎛️ सभी बटन्स (Owner, Update, Support)
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
    today = datetime.date.today()
    
    # 📝 लॉगर ग्रुप में सिर्फ स्टार्ट करने का अलर्ट भेजना
    start_log = (
        f"👋 *User Started Bot*\n\n"
        f"👤 *User:* @{username}\n"
        f"🆔 *ID:* `{user_id}`\n"
        f"📅 *Time:* `{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`"
    )
    send_log(start_log)
    
    if user_id in db["users"]:
        created_at_str = db["users"][user_id].get("created_at", today.isoformat())
        created_at = datetime.date.fromisoformat(created_at_str)
        days_passed = (today - created_at).days
        
        if days_passed >= 28:
            api_key = generate_new_key(user_id, username, db, log_reason="Key Expired (28 Days Completed)")
            status_text = "🔄 आपकी पुरानी की 28 दिन पूरे होने के कारण एक्सपायर हो गई थी। नई API Key जनरेट कर दी गई है!"
        else:
            api_key = db["users"][user_id]["key"]
            remaining_days = 28 - days_passed
            status_text = f"⏳ आपकी यह API Key अभी `{remaining_days} दिन` और वैलिड है।इसके बाद आप नई की निकाल सकेंगे।"
    else:
        api_key = generate_new_key(user_id, username, db, log_reason="First Time Registration")
        status_text = "🎉 आपकी पहली 28-days API Key सफलतापूर्वक जनरेट हो गई है!"

    api_status = check_api_status()

    welcome_text = (
        f"👋 *Hello @{username}*\n\n"
        f"Welcome to *MARCO_BOTS API System*! I am here to provide you with your personal, high-speed API Key for seamless music and video downloading. 🚀\n\n"
        f"📢 *Status:* {status_text}\n\n"
        f"🤖 *API Status:* `{api_status}`\n"
        f"🔑 *Your API Key:* `{api_key}`\n\n"
        f"🌐 *API URL:* `https://api.marco-bots.tools/api/v1/fetch`\n\n"
        f"📌 *Available Commands:*\n"
        f"🔹 `/keygen` - View or refresh your 28-days API key\n"
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
