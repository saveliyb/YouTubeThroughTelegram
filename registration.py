from telethon import TelegramClient
from telethon.sessions import StringSession

# Use your own values from my.telegram.org
api_id = 13043497
api_hash = '1e32626638d848727a2a082c9cae3a06'

# The first parameter is the .session file name (absolute paths allowed)
with TelegramClient('anon', api_id, api_hash) as client:
    print(client.session.save())
    print(StringSession.save(client.session))