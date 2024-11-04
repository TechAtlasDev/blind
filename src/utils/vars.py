from dotenv import DotEnv

ENV = DotEnv(".env")

NAME = ENV.get("NAME")
API_ID = ENV.get("API_ID")
API_HASH = ENV.get("API_HASH")
BOT_TOKEN = ENV.get("BOT_TOKEN")
ADMIN_ID = ENV.get("ADMIN_ID")
AI_TOKEN = ENV.get("AI_TOKEN")
GOOGLE_KEY_SEARCH_ENGINE_CUSTOM = ENV.get("GOOGLE_KEY_SEARCH_ENGINE_CUSTOM")
GOOGLE_KEY_CX = ENV.get("GOOGLE_KEY_CX")