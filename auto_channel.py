
import json
import time
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError

API_ID = 26720505
API_HASH = "4f6b5edda1519598f711c0f1dbd294f2"
PHONE_NUMBER = "+918982059329"

def create_new_channel():
    with TelegramClient("session_auto", API_ID, API_HASH) as client:
        client.connect()
        if not client.is_user_authorized():
            client.send_code_request(PHONE_NUMBER)
            try:
                client.sign_in(PHONE_NUMBER, input('Enter OTP: '))
            except SessionPasswordNeededError:
                client.sign_in(password=input('Two-Step Verification Password: '))

        result = client(functions.channels.CreateChannelRequest(
            title='Cruel Women Backup',
            about='Auto-created channel for recovery',
            megagroup=False
        ))
        new_channel = result.chats[0]
        new_link = f"https://t.me/{new_channel.username or 'joinchat/' + new_channel.invite.link}"

        with open("user_data.json", "r+") as f:
            data = json.load(f)
            data["latest_channel_link"] = new_link
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()

if __name__ == "__main__":
    create_new_channel()
