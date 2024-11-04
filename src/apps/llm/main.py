from pyrogram import Client, filters
from pyrogram.types import Message
from .lib.objects import AI
from .lib.handler import HandlerResponseJSON
from google.generativeai.types.generation_types import GenerateContentResponse

from src.utils.utilities import printTest
import google.generativeai as genai

class partFunction:
  def __init__(self, name:str, response:dict) -> genai.protos.Part:
    return genai.protos.Part(
        function_response = genai.protos.FunctionResponse(
          name=name,
          response=response
        )
      )


@Client.on_message(filters.command("cuvo") | filters.private)
async def CUVO(client: Client, message: Message):
    CUVO = AI(info_user=message)
    CHAT = CUVO.createChat()
    
    text_user = message.text[len(message.text.split(" ")[0]):].strip()
    mensaje_respuesta = "Generando respuesta..."

    sent_message = await message.reply(mensaje_respuesta)

    RESPONSE:GenerateContentResponse = CHAT.send_message(text_user)
    printTest(RESPONSE.parts)
    HANDLER = HandlerResponseJSON(RESPONSE, message, client)
    response = await HANDLER.execute()
    responseIA = CHAT.send_message(genai.protos.Part(
        function_response = genai.protos.FunctionResponse(
          name=response["name"],
          response=response["response"]
        )
      ), tools=["google_search_retrieval"]
    )    
    HANDLER = HandlerResponseJSON(responseIA, message, client)
    response = await HANDLER.execute()

    await sent_message.edit("[✅] Respuesta procesada con éxito")