class Unifier:
    @staticmethod
    def name(name: str) -> str:
        new_name = ""
        symbols = "abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя:;\"'1234567890-=_+*@!#$%^&()№[]{}|,<>."
        for symb in name.lower():
            if symb in symbols:
                new_name += symb
            else:
                new_name += " "
        return new_name

    @staticmethod
    def url(url: str):
        if "youtu.be" in url:
            url = f"https://www.youtube.com/watch?v={url.split('/')[-1]}"
        if "https://www.youtube.com/watch?v=" in url:
            return url
        else:
            return -1

