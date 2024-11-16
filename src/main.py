import sys
import os
from pyrogram import Client
from src.utils.vars import *

print ("Sistema iniciando... -> ", AI_TOKEN)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

bot = Client(
    NAME,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="src/apps")
)

bot.run()
