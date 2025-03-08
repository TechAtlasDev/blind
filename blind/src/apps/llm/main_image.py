from pyrogram import Client, filters
from pyrogram.types import Message
from .lib.handler import HandlerResponseJSON
from .lib.objects import CHAT
from google.generativeai.types.generation_types import GenerateContentResponse
from pyrogram import enums

from blind.src.utils.utilities import upload_to_gemini, clearComand, downloadMedia, printTest
from blind.src.utils.buttons import keymakers
import os

@Client.on_message(filters.photo & (filters.command("cuvo") | filters.private))
async def main_images(client: Client, message: Message):
  await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)

  CONTENT = []
  CONTENT_MIME = "image/jpeg"
  CONTENT_ID = message.photo.file_id
  
  CAPTION = f"Analiza esta imagen, formato: {CONTENT_MIME}" if clearComand(message.caption) == "" or clearComand(message.caption) == None else clearComand(message.caption)+f"\n\nTipo de contenido: {CONTENT_MIME}"
  print (message.caption)
  CONTENT.append(CAPTION)

  # Descargando el archivo
  PATH = await downloadMedia(client, CONTENT_ID)
  # Subiendo el archivo a gemini
  URL = upload_to_gemini(PATH, CONTENT_MIME)
  os.remove(PATH)

  CONTENT.append(URL)

  printTest(CONTENT)

  # Enviando el mensaje a la IA
  AICUVO = CHAT(message, client)
  RESPONSE = await AICUVO.send_parts(CONTENT)

  HANDLER = HandlerResponseJSON(RESPONSE, message, client)
  await HANDLER.execute()

  client.set_parse_mode(enums.ParseMode.MARKDOWN)
  await client.send_chat_action(message.chat.id, enums.ChatAction.CANCEL)