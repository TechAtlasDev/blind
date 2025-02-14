from telegram import Bot
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
PARAMS = sys.argv

from blind.src.utils.vars import *

class TGBot:
  def __init__(self):
    self.bot = Bot(token=BOT_TOKEN)

  def send_message(self, content, CHAT_ID):
    self.bot.send_message(CHAT_ID, content)