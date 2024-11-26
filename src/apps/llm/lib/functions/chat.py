from pyrogram import Client
from pyrogram.types.messages_and_media.message import Message
from pyrogram import enums

async def main(texto:str, **kwargs):
  message:Message = kwargs.get("message", None)
  client:Client = kwargs.get("client", None)

  client.set_parse_mode(enums.ParseMode.MARKDOWN)
  
  for index in range(0, len(texto), 4000):
    await message.reply(texto[index:index+4000], reply_to_message_id=message.id)