from .serializer import SerializerResponse

from pyrogram import Client
from pyrogram.types.messages_and_media.message import Message
from google.generativeai.types.generation_types import GenerateContentResponse

from .path import functions
from .functions.chat import main

class HandlerResponseJSON:
  def __init__(self, data:GenerateContentResponse, messsage:Message, client:Client):
    self.message = messsage
    self.client = client
    self.data = data    

  async def execute(self) -> dict:
    for part in self.data.parts:
      if part.function_call:
        function_name = part.function_call.name
        args = part.function_call.args
        if functions.get(function_name, None):
#          if type(args) == dict:
#            await self.message.reply(f"Funcion activada por CuVo: {function_name}")
#          else:
#            await self.message.reply(f"Funcion activada por CuVo: {function_name}")
          response = await functions[function_name](**part.function_call.args, message=self.message, client=self.client)
          return {"name":function_name, "response":response}
      elif part.text:
        await main(part.text, message=self.message, client=self.client)