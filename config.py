# config.py
from dataclasses import dataclass
from environs import Env

@dataclass
class Bots:
    bot_token: str
    admin_ids: list[int]
    gemini_api_key: str

@dataclass
class Settings:
    bots: Bots

def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMIN_IDS"))),
            gemini_api_key=env.str("GEMINI_API_KEY")
        )
    )

