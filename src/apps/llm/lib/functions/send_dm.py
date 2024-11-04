from pyrogram import Client
from pyrogram.types.messages_and_media.message import Message

class objectResponse:
  def __init__(self, data:dict={}):
    self.CHAT_ID = data.get("chat_id", None)
    self.TEXT = data.get("text", None)

async def send_dm(id:int, text:str, **kwargs):
  message:Message = kwargs.get("message", None)
  client:Client = kwargs.get("client", None)
  
#  response = objectResponse(data_validated)
  await message.reply("[✅] CUVO ESTÁ USANDO EL MENSAJEADOR PRIVADO")
  await client.send_message(chat_id=id, text=f"CUVO TE DICE: {text}", reply_to_message_id=message.id)

  return {"results": f"Mensaje enviado de manera exitosa a {id}"}