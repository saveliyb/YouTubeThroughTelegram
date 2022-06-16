from pytube import YouTube
import logging

import os

import aiogram
from aiogram import types

from CONFIG import Config
from example_tele import send_video

logging.basicConfig(level=logging.INFO)

bot = aiogram.Bot(token=Config.TOKEN)
dp = aiogram.Dispatcher(bot)


async def is_admin(message: types.Message):
    if str(message.from_user.id) in Config.admins_id:
        return True
    else:
        return False


async def download_yotube_video(url: str):
    """скачивание видео на сервер"""
    try:
        yt_obj = YouTube(url)

        filters = yt_obj.streams.filter(progressive=True, file_extension='mp4')
        video_name = f"{yt_obj.title}.mp4"
        # download the highest quality video
        filters.get_highest_resolution().download(filename=video_name)
        return video_name
    except Exception as e:
        print(e)
        return e


async def info_video(message: types.Message, flag=True):
    if await is_admin(message):
        try:
            url = message.text.split()[-1]
            yt_obj = YouTube(url)
            auth = yt_obj.author
            name = yt_obj.title
            return {"auth": auth, "name": name}
        except Exception as e:
            print(e)
            return -1
    else:
        return {"auth": "К сожадению", "name": " Вы не админ!"}  # Костыль


@dp.message_handler(commands=["info"])
async def info(message: types.Message):
    return await message.answer(': '.join((await info_video(message)).values()))


@dp.message_handler(commands=["d", "donload"])
async def download_video(message: types.Message):
    """скачивание и отпрвка видео пользователю"""
    chat_id = message.chat.id

    url = ' '.join(message.text.split()[1:])
    if "youtu.be" in url:
        # преобразование ссылки мобильного ютуба
        url = f"https://www.youtube.com/watch?v={url.split('/')[-1]}"

    await message.answer("Ожидайте")
    file_name = (await download_yotube_video(url))
    await message.answer("Видео скачано на сервер.\nНачалась загрузка в телеграм.")
    # отправка видео пользователю
    res = await info_video(message)
    if res != -1:
        text = ': '.join((await info_video(message)).values())
    else:
        text = ""

    await send_video(file_name, chat_id=chat_id, text=text)
    os.remove(file_name)


@dp.message_handler(content_types=aiogram.types.ContentTypes.VIDEO)
async def video_handler(message: types.Message):
    chat_id, text = message.caption.split("-757247959279949225")
    await bot.send_video(chat_id=int(chat_id), video=message.video.file_id, caption=text)
    await bot.send_message(int(chat_id), "видео получено")


@dp.message_handler()
async def main(message: types.Message):
    """обработчик всех сообщений не связанных с командой"""
    await message.answer(message.text)
    return


if __name__ == '__main__':
  aiogram.executor.start_polling(dp, skip_updates=True)
