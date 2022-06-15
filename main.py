from pytube import YouTube
import logging

import os

import aiogram
from CONFIG import Config
from aiogram import types

logging.basicConfig(level=logging.INFO)

bot = aiogram.Bot(token=Config.TOKEN)
dp = aiogram.Dispatcher(bot)


async def is_admin(message: types.Message):
    if str(message.from_user.id) in Config.admins_id:
        return True
    else:
        return False


async def download_yotube_video(url: str):
    try:
        yt_obj = YouTube(url)

        filters = yt_obj.streams.filter(progressive=True, file_extension='mp4')
        video_name = f"{yt_obj.title}.mp4"
        # download the highest quality video
        filters.get_highest_resolution().download(filename=video_name)
        print('Video Downloaded Successfully')
        return video_name
    except Exception as e:
        print(e)
        return e


async def info_video(message: types.Message):
    if await is_admin(message):
        try:
            url = message.text.replace("/url", "")
            yt_obj = YouTube(url)
            auth = yt_obj.author
            name = yt_obj.title
            return {"auth": auth, "name": name}
        except Exception as e:
            print(e)
            return e
    else:
        return {"auth": "К сожадению", "name": " Вы не админ!"}  # Костыль


@dp.message_handler(commands=["info"])
async def info(message: types.Message):
    return await message.answer(': '.join((await info_video(message)).values()))


@dp.message_handler(commands=["d", "donload"])
async def download_video(message: types.Message):
    # https://youtu.be/vT0M6q0dkp4
    url = ' '.join(message.text.split()[1:])
    if "youtu.be" in url:
        url = f"https://www.youtube.com/watch?v={url.split('/')[-1]}"
    print(url)
    await message.answer("Ожидайте")
    file_name = await download_yotube_video(url)
    await message.answer("Видео скачано на сервер.\nНачалась загрузка в телеграм.")
    print(file_name)
    with open(f"./{file_name}", "rb") as vid:
        await message.answer_video(vid)
        os.remove(file_name)



@dp.message_handler()
async def main(message: types.Message):
    """обработчик всех сообщений не связанных с командой"""
    print(message.text)
    print(message)
    await message.answer(message.text)
    return


if __name__ == '__main__':
  aiogram.executor.start_polling(dp, skip_updates=True)