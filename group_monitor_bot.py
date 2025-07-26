

import requests
from telethon import TelegramClient, events
from datetime import datetime

# --- CONFIGURATION ---
API_ID = 26720505
API_HASH = "4f6b5edda1519598f711c0f1dbd294f2"
BOT_TOKEN = "8390342775:AAFJ31nGULTt2MQlAnCyUDwdz9QfGskmkbA"
ADMIN_USER_ID = 7229386225
PREVIEW_CHANNEL_ID = -1002879063669  # Not used here, but keep if needed later

# --- TELEGRAM CLIENT SETUP ---
bot = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# --- HELPER FUNCTION: GEO INFO FROM IP ---
def get_geo_info():
    try:
        response = requests.get("https://ipinfo.io/json", timeout=5)
        return response.json().get("country", "Unknown")
    except Exception:
        return "Unknown"

# --- HELPER FUNCTION: APPROXIMATE ACCOUNT AGE ---
def account_age(user):
    if user and not user.bot:
        created = user.id >> 32
        year = 2000 + ((created & 0x7F000000) >> 24)
        return f"{datetime.now().year - year} years"
    return "Unknown"

# --- EVENT HANDLER FOR NEW JOIN EVENTS ---
@bot.on(events.ChatAction())
async def handler(event):
    if event.user_joined or event.user_added:
        user = await event.get_user()
        geo = get_geo_info()
        age = account_age(user)

        msg = (
            f"👤 <b>New Join Request</b>\n"
            f"🆔 Username: @{user.username or 'N/A'}\n"
            f"🌍 Country: {geo}\n"
            f"📅 Account Age: {age}"
        )

        await bot.send_message(ADMIN_USER_ID, msg, parse_mode="html")

# --- KEEP BOT RUNNING ---
print("🤖 Bot is running...")
bot.run_until_disconnected()
