# 1. Python का लाइटवेट और स्टेबल वर्जन
FROM python:3.9-slim

# 2. कंटेनर के अंदर काम करने की जगह (Working Directory) सेट करें
WORKDIR /app

# 3. सिस्टम डिपेंडेंसीज इंस्टॉल करें
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. सबसे पहले requirements.txt को कॉपी करके लाइब्रेरीज़ इंस्टॉल करें
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. बाकी का सारा कोड कॉपी करें
COPY . .

# 6. पोर्ट को ओपन करें (Railway इसे ऑटोमैटिक डिटेक्ट कर लेगा)
EXPOSE 8000

# 7. FastAPI सर्वर और टेलीग्राम बोट दोनों को एक साथ चालू करने की फाइनल कमांड
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
