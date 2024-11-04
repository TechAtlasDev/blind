from pyrogram import Client
from pyrogram.types.messages_and_media.message import Message

async def main(texto:str, **kwargs):
  message:Message = kwargs.get("message", None)
  client:Client = kwargs.get("client", None)
  
  await message.reply(texto)