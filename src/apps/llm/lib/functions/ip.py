from pyrogram import Client
from pyrogram.types.messages_and_media.message import Message

import requests, json

async def fetchIPData(ip:str, **kwargs):
  message:Message = kwargs.get("message", None)
  client:Client = kwargs.get("client", None)

  await message.reply_text(f"[🛰] <b>CuVo</b> está buscando los datos de la IP <code>{ip}</code>.")

  response = requests.get(f"http://ip-api.com/json/{ip}").json()
  await message.reply(f"[✅] CUVO ESTÁ USANDO EL BUSCADOR DE IPS")
  return {"results": response}