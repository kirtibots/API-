# config.py
import os

# @BotFather से मिला हुआ आपके बोट का टोकन यहाँ डालें
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN_HERE")

# अपनी असली टेलीग्राम संख्यात्मक आईडी (Numeric ID) यहाँ डालें (उदा: 543216789)
# सिर्फ इसी आईडी से /broadcast और /stats कमांड्स काम करेंगे
OWNER_ID = int(os.getenv("OWNER_ID", "123456789")) 

# अपने अपडेट चैनल और सपोर्ट ग्रुप का यूजरनेम यहाँ डालें (आगे @ ज़रूर लगाएँ)
UPDATE_CHANNEL = "@YourUpdateChannel"   # उदा: @marco_updates
SUPPORT_GROUP = "@YourSupportGroup"    # उदा: @marco_support

# कोर डाउनलोडर API और डेटाबेस फाइल का नाम
COBALT_API_URL = "https://api.cobalt.tools/api/json"
DB_FILE = "database.json"
