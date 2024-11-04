from src.utils.vars import AI_TOKEN
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from pyrogram.types.messages_and_media.message import Message

from .path import functions

genai.configure(api_key=AI_TOKEN)

class partFunction:
  def __init__(self, name:str, response:dict) -> genai.protos.Part:
    return genai.protos.Part(
      )


class AI:
  # Funcion que se ejecuta al crearse el objeto
  def __init__(self, name:str="CuVo", info_user:Message=None, data:dict={}) -> None:
    self.name = name

    MODEL = data.get("model", "gemini-1.5-flash")
    self.model = genai.GenerativeModel(
      model_name=MODEL,
      tools=[functions.values()],#.append("google_search_retrieval"),
      generation_config={
        "temperature": data.get("temperature", 1),
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
      },
    )

  def createChat(self):
    self.chat = self.model.start_chat(history=[])
    return self.chat

  def responseTest(self, prompt:str):
    response = self.chat.send_message(prompt)
    return response

  def responseJSON(self, prompt:str):
    PROMPT = f"{self.CONTEXT_JSON.format(prompt)}"
    response = self.model.generate_content(
      PROMPT,
      stream=False,
      safety_settings={
          HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
          HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
          HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
          HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
      }
    )

    return response