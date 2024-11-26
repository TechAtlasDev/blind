import sys
import os
from pyrogram import Client
from src.utils.vars import *

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
PARAMS = sys.argv

IS_PROD = PARAMS[-1] == "--prod"

bot = Client(
    NAME,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="src/apps")
)

bot.run()
