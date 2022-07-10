import os

import aiogram
from aiogram import types
import logging

from APIYouTube import YoutubeMethods as YT_methods
from filters import *
from unifier import Unifier
import telethon_sender

logging.basicConfig(level=logging.INFO)

bot = aiogram.Bot(token=Config.TOKEN)
dp = aiogram.Dispatcher(bot)


@dp.message_handler(content_types=aiogram.types.ContentTypes.VIDEO)
async def video_handler(message: types.Message):
    chat_id, text = message.caption.split("-757247959279949225")
    await bot.send_video(chat_id=int(chat_id), video=message.video.file_id, caption=text)
    await bot.send_message(int(chat_id), "видео получено")


@dp.message_handler()
async def main(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("Вы не имеете доступа к боту!")
        return
    if not is_url_right(message.text):
        await message.answer("К сожалению это не ссылка")
        return
    await message.answer("Ожидайте")
    file_name = (await YT_methods.download_video(Unifier.url(message.text)))
    await message.answer("Видео скачано на сервер.\nНачалась загрузка в телеграм.")
    await telethon_sender.send_video(file_name, message.from_user.id, message.text)
    os.remove(file_name)
        


if __name__ == '__main__':
    aiogram.executor.start_polling(dp, skip_updates=True)
