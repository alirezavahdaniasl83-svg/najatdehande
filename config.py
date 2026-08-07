import os

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "0"))

    API_NAME = "NajatDehande"
    API_VERSION = "0.2.0"

config = Config()
