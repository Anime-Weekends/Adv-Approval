from flask import Flask, request
from pyrofork import Client
from config import API_ID, API_HASH, BOT_TOKEN, WEBHOOK_URL, PORT
import asyncio

app = Flask(__name__)
loop = asyncio.get_event_loop()

bot = Client(
    "auto_approver_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True
)

@app.route("/", methods=["GET"])
def index():
    return "Bot is Running!", 200

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json()
    if update:
        loop.create_task(bot.process_update(update))
    return "OK", 200

async def start_webhook():
    await bot.start()
    await bot.set_webhook(url=f"{WEBHOOK_URL}/{BOT_TOKEN}")
    print("Bot started with webhook!")

if __name__ == "__main__":
    loop.run_until_complete(start_webhook())
    app.run(host="0.0.0.0", port=PORT)
