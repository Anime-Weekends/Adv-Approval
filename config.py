import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

# Webhook settings
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", 8080))

# MongoDB
MONGO_URI = os.getenv("MONGO_URI")

# Start message images (unlimited support)
START_IMAGES = [
    "https://i.ibb.co/ynjcqYdZ/photo-2025-04-06-20-48-47-7490304985767346192.jpg",
    "https://i.ibb.co/hBnMzYm/photo-2025-04-07-20-50-00.jpg"
]
