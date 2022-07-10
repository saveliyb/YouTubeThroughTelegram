from pytube import YouTube


class YoutubeMethods:
    def __init__(self):
        pass

    @staticmethod
    async def download_video(url: str):
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

    @staticmethod
    async def info_video(url: str):
        try:
            yt_obj = YouTube(url)
            auth = yt_obj.author
            name = yt_obj.title
            return {"auth": auth, "name": name}
        except Exception as e:
            print(e)
            return ""
