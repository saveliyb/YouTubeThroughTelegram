from CONFIG import Config

from urllib.parse import urlparse


def is_admin(user_id: int):
    if str(user_id) in Config.admins_id:
        return True
    else:
        return False


def is_sender_video(user_id: int):
    if str(user_id) == Config.sender_video_id:
        return True
    else:
        return False


def parse_url_query(query: str):
    dct = {}
    for args in query.split("&"):
        arg = args.split("=")
        dct[arg[0]] = arg[1]
    return dct


def is_url_right(url: str):
    ParseResult = urlparse(url)
    if ParseResult.netloc == "youtu.be" and ParseResult.path != "":
        return True
    elif ParseResult.netloc == "www.youtube.com" and \
            ParseResult.path == "/watch" and \
            "v" in parse_url_query(ParseResult.query).keys():
        return True
    return False
