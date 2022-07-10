from telethon import TelegramClient
from telethon.sessions import StringSession
import os
from CONFIG import Config

import asyncio
from APIYouTube import YoutubeMethods as YT

# loop = asyncio.get_event_loop()


async def send_video(video_name: str, chat_id: int, url: str):
    video_info = ": ".join((await YT.info_video(url)).values())

    # отправка видео через telethon
    if os.path.isfile(f"{Config.session_name}.session"):
        client = TelegramClient(StringSession(Config.secret_string), Config.api_id, Config.api_hash)
    else:
        client = TelegramClient(Config.session_name, Config.api_id, Config.api_hash)

    await client.connect()

    text_ = "-757247959279949225".join([str(chat_id), video_info])

    await client.send_file(Config.bot_name, f'./{video_name}', caption=text_)

    await client.disconnect()
