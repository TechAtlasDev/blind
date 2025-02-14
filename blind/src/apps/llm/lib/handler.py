from google.generativeai.types import HarmCategory, HarmBlockThreshold
from pyrogram import Client, enums
from pyrogram.types.messages_and_media.message import Message
from google.generativeai.types.generation_types import GenerateContentResponse

from .objects import CHAT, partFunction

from .path import functions
from .functions.chat import main
from blind.src.utils.utilities import printTest, printError

class HandlerResponseJSON:
  def __init__(self, data:GenerateContentResponse, messsage:Message, client:Client):
    self.message = messsage
    self.client = client
    self.data = data    

  async def execute(self, functions:dict=functions) -> dict:
    for part in self.data.parts:
      printTest(part) # -- Debug
      if part.text:
        AICUVO = CHAT(self.message, self.client)
        await main(f"{part.text}", message=self.message, client=self.client)
      if part.function_call:
        self.client.set_parse_mode(enums.ParseMode.DEFAULT)
        function_name = part.function_call.name
        if functions.get(function_name, None):
          # Ejecutando la funcion y guardando el resultado
          try:
            response = await functions[function_name](**part.function_call.args, message=self.message, client=self.client)
          except Exception as e:
            await printError(e, self.client)
            response = {"results": f"Error al ejecutar la función {function_name}: {e}"}

          PARTRESPONSECALL = response["results"] if response.get("results", None) else response
          partContent = partFunction(name=function_name, response={"results": PARTRESPONSECALL})
          parts = [partContent]

          PARTSADITIONAL = response["parts"] if response.get("parts", None) else None
          if PARTSADITIONAL:
            for part in PARTSADITIONAL:
              parts.append(part) if part else None

          AICUVO = CHAT(self.message, self.client)
          RESPONSE = await AICUVO.send_parts(parts)
          HANDLER = HandlerResponseJSON(RESPONSE, self.message, self.client)
          await HANDLER.execute()