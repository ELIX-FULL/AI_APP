# config.py
import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class Bots:
    bot_token: str
    admin_ids: list[int]
    gemini_api_key: str
    # Новые поля
    fusion_brain_api: str
    fusion_brain_secret: str


@dataclass
class Settings:
    bots: Bots


def get_settings(path: str):
    load_dotenv(path)
    admin_ids_str = os.getenv("ADMIN_IDS", "")

    return Settings(
        bots=Bots(
            bot_token=os.getenv("BOT_TOKEN"),
            admin_ids=[int(admin_id) for admin_id in admin_ids_str.split(',') if admin_id],
            gemini_api_key=os.getenv("GEMINI_API_KEY"),
            # Новые поля
            fusion_brain_api=os.getenv("FUSION_BRAIN_API_KEY"),
            fusion_brain_secret=os.getenv("FUSION_BRAIN_SECRET_KEY")
        )
    )