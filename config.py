# config.py
import os

# @BotFather से मिला हुआ आपके बोट का टोकन यहाँ डालें
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN_HERE")

# 📢 आपके लॉग ग्रुप की ID (ग्रुप आईडी हमेशा माइनस '-' से शुरू होती है, जैसे: -1003979103138)
LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID", "-1003979103138")) 

# अपनी असली टेलीग्राम संख्यात्मक आईडी (Numeric ID) यहाँ डालें (उदा: 8857291657)
# सिर्फ इसी आईडी से /broadcast और /stats कमांड्स काम करेंगे
OWNER_ID = int(os.getenv("OWNER_ID", "8857291657")) 

# अपने अपडेट चैनल और सपोर्ट ग्रुप का यूजरनेम यहाँ डालें (आगे @ ज़रूर लगाएँ)
UPDATE_CHANNEL = "https://telegram.me/annu_updates"   # उदा: @annu_updates
SUPPORT_GROUP = "https://telegram.me/annu_support"    # उदा: @annu_support

# कोर डाउनलोडर API और डेटाबेस फाइल का नाम
COBALT_API_URL = "https://api-dl.cgm.rs/api/json"
MONGO_URL = "mongodb+srv://pusers:nycreation@nycreation.pd4klp1.mongodb.net/?retryWrites=true&w=majority&appName=NYCREATION"
