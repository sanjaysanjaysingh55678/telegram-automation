
import json
import requests
from telethon import TelegramClient, events
from datetime import datetime

API_ID = 26720505
API_HASH = "4f6b5edda1519598f711c0f1dbd294f2"
BOT_TOKEN = "8390342775:AAFJ31nGULTt2MQlAnCyUDwdz9QfGskmkbA"
ADMIN_USER_ID = 7229386225
PREVIEW_CHANNEL_ID = -1002879063669

bot = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

def get_geo_info():
    try:
        response = requests.get("https://ipinfo.io/json")
        return response.json().get("country", "Unknown")
    except:
        return "Unknown"

def account_age(user):
    if user and user.bot is False:
        created = user.id >> 32
        year = 2000 + ((created & 0x7F000000) >> 24)
        return f"{2025 - year} years"
    return "Unknown"

@bot.on(events.ChatAction())
async def handler(event):
    if event.user_joined or event.user_added:
        user = await event.get_user()
        geo = get_geo_info()
        age = account_age(user)
        msg = f"👤 New Join Request:

🆔 Username: @{user.username}
🌍 Country: {geo}
📅 Account Age: {age}"
        await bot.send_message(ADMIN_USER_ID, msg)

bot.run_until_disconnected()
