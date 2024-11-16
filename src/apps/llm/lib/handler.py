from google.generativeai.types import HarmCategory, HarmBlockThreshold
from pyrogram import Client
from pyrogram.types.messages_and_media.message import Message
from google.generativeai.types.generation_types import GenerateContentResponse

from .objects import CHAT, partFunction

from .path import functions
from .functions.chat import main
from src.utils.utilities import printTest

class HandlerResponseJSON:
  def __init__(self, data:GenerateContentResponse, messsage:Message, client:Client):
    self.message = messsage
    self.client = client
    self.data = data    

  async def execute(self) -> dict:
    for part in self.data.parts:
      printTest(part) # -- Debug
      if part.text:
        AICUVO = CHAT(self.message)
        await main(f"{part.text}\n\n[❗️] Tokens usados: {AICUVO.count_tokens()}", message=self.message, client=self.client)
      if part.function_call:
        function_name = part.function_call.name
        if functions.get(function_name, None):
          # Ejecutando la funcion y guardando el resultado
          response = await functions[function_name](**part.function_call.args, message=self.message, client=self.client)

          PARTRESPONSECALL = response["results"] if response.get("results", None) else response
          partContent = partFunction(name=function_name, response={"results": PARTRESPONSECALL})
          parts = [partContent]

          PARTSADITIONAL = response["parts"] if response.get("parts", None) else None
          if PARTSADITIONAL:
            for part in PARTSADITIONAL:
              parts.append(part) if part else None

          AICUVO = CHAT(self.message)
          RESPONSE:GenerateContentResponse = AICUVO.chat.send_message(parts,       safety_settings={
          HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
          HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
          HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
          HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
      })
          HANDLER = HandlerResponseJSON(RESPONSE, self.message, self.client)
          await HANDLER.execute()

