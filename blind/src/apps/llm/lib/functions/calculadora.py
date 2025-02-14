from blind.src.utils.utilities import printTest

from pyrogram import Client
from pyrogram.types.messages_and_media.message import Message

async def sumar(a:int, b:int, **kwargs):
  message:Message = kwargs.get("message", None)
  client:Client = kwargs.get("client", None)

  await message.reply_text(f"[🧠] <b>CuVo</b> está realizando una suma.")

  await message.reply(f"[✅] CUVO ESTÁ USANDO LA CALCULADORA")
  return {"results": a+b}