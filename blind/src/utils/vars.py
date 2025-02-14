from dotenv import load_dotenv
import os

load_dotenv()

class DotEnv:
  def __init__(self, file:str):
    self.file = file
  
  def get(self, var:str):
    return os.environ.get(var)

ENV_BOT = DotEnv(".env")
NAME = ENV_BOT.get("NAME")
API_ID = ENV_BOT.get("API_ID")
API_HASH = ENV_BOT.get("API_HASH")
BOT_TOKEN = ENV_BOT.get("BOT_TOKEN")
ADMIN_ID = ENV_BOT.get("ADMIN_ID")
AI_TOKEN = ENV_BOT.get("AI_TOKEN")
GOOGLE_KEY_SEARCH_ENGINE_CUSTOM = ENV_BOT.get("GOOGLE_KEY_SEARCH_ENGINE_CUSTOM")
GOOGLE_KEY_CX = ENV_BOT.get("GOOGLE_KEY_CX")
IS_PROD = True