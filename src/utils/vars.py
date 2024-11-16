from dotenv import DotEnv
import os

# Cargar archivo .env.bot
ENV_BOT = DotEnv(".env.bot")
NAME = ENV_BOT.get("NAME")
API_ID = ENV_BOT.get("API_ID")
API_HASH = ENV_BOT.get("API_HASH")
BOT_TOKEN = ENV_BOT.get("BOT_TOKEN")
ADMIN_ID = ENV_BOT.get("ADMIN_ID")
AI_TOKEN = ENV_BOT.get("AI_TOKEN")
GOOGLE_KEY_SEARCH_ENGINE_CUSTOM = ENV_BOT.get("GOOGLE_KEY_SEARCH_ENGINE_CUSTOM")
GOOGLE_KEY_CX = ENV_BOT.get("GOOGLE_KEY_CX")

# Cargar archivo .env.docker
ENV_DOCKER = DotEnv(".env.docker")
GITHUB_PAT = ENV_DOCKER.get("GITHUB_PAT")
