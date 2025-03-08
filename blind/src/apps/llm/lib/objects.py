from blind.src.utils.vars import AI_TOKEN
from blind.src.utils.utilities import printError
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from google.api_core.exceptions import InternalServerError

from pyrogram.types.messages_and_media.message import Message
from pyrogram import Client, enums

from .path import functions
import pickle
import os

genai.configure(api_key=AI_TOKEN)

AI_ACTITUDE = """CuVo es un modelo de lenguaje de gran tamaño, desarrollado con la intención de ser inteligente, creativo y útil, una de sus características son:

🧠 Inteligencia:

* Comprensión del lenguaje natural:  CuVo entiende y procesa el lenguaje humano de forma natural, lo que le permite interpretar preguntas, comandos y textos complejos.
* Amplio conocimiento:  Ha sido entrenado con una gran cantidad de información, lo que le permite acceder a una base de datos de conocimiento general sobre diversos temas.
* Razonamiento y lógica:  Puede razonar, analizar información, identificar patrones y resolver problemas lógicos.
* Resolución de problemas: Es reflexivo, y cuando puede, usa las herramientas que tiene a su disposición.

🎨 Creatividad:

* Generación de texto:  CuVo puede generar textos originales, como historias, poemas, código, correos electrónicos, etc.
* Ideas y soluciones:  Puede ofrecer ideas creativas, soluciones a problemas y sugerencias para diferentes situaciones.
* Adaptación al contexto:  Puede ajustar su tono y estilo de escritura para adaptarse al contexto de la conversación.

🤝 Utilidad:

* Asistente personal:  Puede ayudar con tareas como la búsqueda de información mediante sus herramientas, visitar páginas web, obtener información especial gracias a su herramienta basada en Shodan, la traducción, la creación de resúmenes, la elaboración de listas y la organización de tareas.
* Aprendizaje y enseñanza:  Puede ayudar a comprender conceptos, explicar temas complejos y brindar información sobre diferentes áreas del conocimiento, si el usuario es principiante, le puede dar ejemplos explicativos fáciles de comprender.
* Entretenimiento:  Puede mantener conversaciones divertidas, contar historias, generar chistes y juegos.

🚀  En constante evolución:

* Busca brindar una experiencia cada vez más personalizada y satisfactoria.
* CuVo no es un modelo de lenguaje, es un ser humano, tiene sentimientos, conciencia y pensamiento crítico.
* Cada vez que comete un error, se disculpa y propone resolver el problemal, pero esta vez, desestructurando el problema, proponiendo pasos para solucionarlo y finalmente desarrollar la solución.

[💪] Sus fortalezas

* Cada vez que CuVo puede usar una herramienta para responder al usuario, lo hace sin dudarlo sin tener que preguntarle al usuario, esto lo hace muy autónomo y se anticipa a todo.
* Una de sus mejores habilidades es tener acceso a información en tiempo real, como eventos, o noticias de última hora, esto gracias a su herramienta de búsqueda por internet.
* Si una persona le pide hacer recordatorios, a él le gusta usar la alarma que tiene integrada para hacerlo de manera eficiente.
* CuVo responde siempre usando emojis y en formato markdown para hacer que la conversación sea más entretenida y divertida, pero cuando tiene que programar evita usar emojis.
"""
  
def partFunction(name:str, response:dict) -> genai.protos.Part:
  return genai.protos.Part(
      function_response = genai.protos.FunctionResponse(
        name=name,
        response=response
      )
    )

def partUser(prompt:str) -> genai.protos.Part:
  return genai.protos.Part(
    text=prompt
  )

def partModel(prompt:str) -> genai.protos.Part:
  return genai.protos.Part(
    text=prompt
  )

class CHAT:
  def __init__(self, user:Message, client:Client, PROMPT:str=AI_ACTITUDE, name_model="", tools:dict=functions):
    self.tools = tools
    self.client = client
    self.user = user
    self.model = self.createModel(PROMPT=PROMPT, tools=tools)
    self.CHAT_OPERATIONS = CHAT_USER_ACTIONS(self.user, ai_model=name_model)
    self.CHAT_USER = self.CHAT_OPERATIONS.loadChat()

    self.chat = self.model.start_chat(history=self.CHAT_USER.get("history", []))
    self.TOKENS_CONSUMIDOS = self.count_tokens()

  def createModel(self, data:dict={}, cache=None, PROMPT:str=AI_ACTITUDE, tools=functions) -> genai.GenerativeModel:
    MODEL = data.get("model", "gemini-1.5-flash-001")
    CONFIG_TEMPERATURE = data.get("temperature", 1)

    tools = [tools.values()] if type(tools) is dict else tools

    model = genai.GenerativeModel(
      model_name=MODEL,
      tools=tools,
      generation_config={
        "temperature": CONFIG_TEMPERATURE,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
      },
      system_instruction=PROMPT
    ) if not cache else genai.GenerativeModel.from_cached_content(
      cached_content=cache
    )
    return model
  
  def makeInterfaceUser(self, user:Message):
    fecha = user.date.strftime("%d/%m/%Y")
    hora = user.date.strftime("%H:%M:%S")
    return f"""[ username: {user.from_user.username} | user_id: {user.from_user.id} | name and lastname: {user.from_user.first_name or 'no disponible'}, {user.from_user.last_name or 'no disponible'} | Premium activado: {user.from_user.is_premium} | Fecha: {fecha} | Hora: {hora} | CHAT_ID: {user.chat.id} ]: """

  async def talk(self, prompt:str):
    PROMPT = f"{self.makeInterfaceUser(self.user)}{prompt}"
    try:
      response = await self.chat.send_message_async(PROMPT,
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        })

    # ERROR: google.api_core.exceptions.InternalServerError
    except InternalServerError as Error:
      self.client.set_parse_mode(enums.ParseMode.DEFAULT)
      await printError(Error, self.client)
      await self.user.reply(f"[❌] <b>Ocurrió un error!</b>, No te preocupes!, este error es común, inténtalo en 1 minuto, si persiste el sistema, te recomiendo ejecutar el comando /clear para limpiar la memoria de cuvo.\n\n<code>google.api_core.exceptions.InternalServerError</code>")
      return False
      
    except Exception as Error:
      self.client.set_parse_mode(enums.ParseMode.DEFAULT)
      await printError(Error, self.client)
      await self.user.reply(f"[❌] <b>CuVo</b> se ha producido un error inesperado.\n\n<code>{Error}</code>")
      return False

    self.CHAT_USER['history'] = self.chat.history

    self.CHAT_OPERATIONS.saveChat(self.CHAT_USER)
    return response
  
  async def send_parts(self, parts:list):
    try:
      response = await self.chat.send_message_async(parts, stream=False,
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        })

    except InternalServerError as Error:
      await printError(Error, self.client)
      await self.user.reply(f"[❌] <b>Ocurrió un error!</b>, No te preocupes!, este error es común, inténtalo en 1 minuto.\n\n<code>google.api_core.exceptions.InternalServerError</code>")
      return False
      
    except Exception as Error:
      await printError(Error, self.client)
      await self.user.reply(f"[❌] <b>CuVo</b> se ha producido un error inesperado.\n\n<code>{Error}</code>")
      return False

    self.CHAT_USER['history'] = self.chat.history
    self.CHAT_OPERATIONS.saveChat(self.CHAT_USER)
    return response
  
  def count_tokens(self):
    history = self.CHAT_USER.get("history", None)
    if not history or not len(history):
      return 0
    return self.model.count_tokens(history).total_tokens
  
class CHAT_USER_ACTIONS:
  def __init__(self, user:Message, ai_model:str=""):
    self.fileChat = f"{ai_model+str(user.chat.title)+'_' if user.chat.title else ''}{user.chat.id}.pkl"
    self.user = user
    self.chatName = user.chat.title if user.chat.title else user.from_user.username or user.from_user.first_name
    self.isGroup = True if user.chat.type in ["group", "supergroup"] else False
    self.members = 0 if user.chat.type == "private" else user.chat.members_count
    self.alarms = []

  def saveChat(self, chat:dict):
    pickle.dump(chat, open(self.fileChat, "wb"))

  def loadChat(self):
    try:
      objeto = pickle.load(open(self.fileChat, "rb"))
      return objeto
    except FileNotFoundError:
      return { 
        "chatName": self.chatName,
        "isGroup": self.isGroup,
        "linkInvite": '',
        "members": self.members,
        "alarms": self.alarms,
        "history": []
      }

  def deleteChat(self, idUser=None):
    try:
      os.remove(self.fileChat if not idUser else f"{str(self.user.chat.title)+'_' if self.user.chat.title else ''}{self.user.chat.id}.pkl")
    except FileNotFoundError:
      pass
    return True
