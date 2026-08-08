from os import getenv
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.API_ID = int(getenv("API_ID", 0))
        self.API_HASH = getenv("API_HASH")

        self.BOT_TOKEN = getenv("BOT_TOKEN")
        self.MONGO_URL = getenv("MONGO_URL")

        self.LOGGER_ID = int(getenv("LOGGER_ID", 0))
        self.OWNER_ID = int(getenv("OWNER_ID", 0))

        self.SONG_LOG_ID = int(getenv("SONG_LOG_ID", 0)) or self.LOGGER_ID

        self.DURATION_LIMIT = int(getenv("DURATION_LIMIT", 1500)) * 1500
        self.QUEUE_LIMIT = int(getenv("QUEUE_LIMIT", 200))
        self.PLAYLIST_LIMIT = int(getenv("PLAYLIST_LIMIT", 200))

        self.SESSION1 = getenv("SESSION", None)
        self.SESSION2 = getenv("SESSION2", None)
        self.SESSION3 = getenv("SESSION3", None)

        self.SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/kullaniciadidi")
        self.SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/ht_bots/40")

        self.AUTO_LEAVE: bool = getenv("AUTO_LEAVE", "False").lower() == "true"
        self.AUTO_END: bool = getenv("AUTO_END", "False").lower() == "true"
    
        self.THUMB_GEN: bool = getenv("THUMB_GEN", "True").lower() == "true"
        self.VIDEO_PLAY: bool = getenv("VIDEO_PLAY", "True").lower() == "true"

        self.LANG_CODE = getenv("LANG_CODE", "az")

        self.COOKIES_URL = [
            url for url in getenv("COOKIES_URL", "").split(" ")
            if url and "batbin.me" in url
        ]
        self.DEFAULT_THUMB = getenv("DEFAULT_THUMB", "https://ibb.co/B29L5v4X")
        self.PING_IMG = getenv("PING_IMG", "https://ibb.co/B29L5v4X")
        self.START_IMG = getenv("START_IMG", "https://ibb.co/B29L5v4X")

        self.BOT_USERNAME = getenv("BOT_USERNAME", "Nunum_robot")
        self.BOT_NAME = getenv("BOT_NAME", "Nuranə")
        self.SEHID_FILE = getenv("SEHID_FILE", "xeyal/helpers/data/sehid.txt")

        self.GROQ_API_KEY = getenv("GROQ_API_KEY")
        self.GROQ_MODEL = getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.PEXELS_API_KEY = getenv("PEXELS_API_KEY")
        self.ADMIN_IDS = [
            int(x) for x in getenv("ADMIN_IDS", "").split(",") if x.strip().isdigit()
        ]
        self.LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", 0)) or self.LOGGER_ID
        self.BOT_CHANNEL_URL = getenv("BOT_CHANNEL_URL", "https://t.me/kullaniciadidi")
        self.CATALOG_PATH = getenv("CATALOG_PATH", "./data/catalog.json")
        self.USERS_PATH = getenv("USERS_PATH", "./data/users.json")

        self.DEFAULT_INLINE_QUERY = getenv("DEFAULT_INLINE_QUERY", "top hits 2026")
        self.KEEPMEDIA_BOT = getenv("KEEPMEDIA_BOT", "KeepMediaBot")
        self.KEEPMEDIA_DUMP_CHAT = int(getenv("KEEPMEDIA_DUMP_CHAT", 0)) or self.LOGGER_ID

    def check(self):
        missing = [
            var
            for var in ["API_ID", "API_HASH", "BOT_TOKEN", "MONGO_URL", "LOGGER_ID", "OWNER_ID", "SESSION1"]
            if not getattr(self, var)
        ]
        if missing:
            raise SystemExit(f"Missing required environment variables: {', '.join(missing)}")
