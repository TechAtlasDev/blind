from .objects import bot
from .objects.bot import ADMIN_ID

def system_start():
  CuVo=bot.TGBot()
  CuVo.send_message("Sistema iniciado", ADMIN_ID)