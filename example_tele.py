from telethon import TelegramClient
from telethon.sessions import StringSession
import os
from CONFIG import Config

import asyncio
loop = asyncio.get_event_loop()


async def send_video(video_name, chat_id, text):
    # отправка видео через telethon
    if os.path.isfile(f"{Config.session_name}.session"):
        client = TelegramClient(StringSession(Config.secret_string), Config.api_id, Config.api_hash)
    else:
        client = TelegramClient(Config.session_name, Config.api_id, Config.api_hash)

    await client.connect()
    client.start()

    text_ ="-757247959279949225".join([str(chat_id), text])

    await client.send_file('@mi_bot_mi_bot', f'./{video_name}', caption=text_)

    client.disconnect()
