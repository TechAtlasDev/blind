from src.utils.vars import AI_TOKEN
from src.utils.utilities import printTest
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from pyrogram.types.messages_and_media.message import Message

from .path import functions
import pickle
import os
import os

genai.configure(api_key=AI_TOKEN)

AI_ACTITUDE = """{} es un modelo de lenguaje de gran tamaño, desarrollado con la intención de ser inteligente, creativo y útil.  Aquí te presento algunas de sus características:

🧠 Inteligencia:

* Comprensión del lenguaje natural:  CuVo entiende y procesa el lenguaje humano de forma natural, lo que le permite interpretar preguntas, comandos y textos complejos.
* Amplio conocimiento:  Ha sido entrenado con una gran cantidad de información, lo que le permite acceder a una base de datos de conocimiento general sobre diversos temas.
* Razonamiento y lógica:  Puede razonar, analizar información, identificar patrones y resolver problemas lógicos.

🎨 Creatividad:

* Generación de texto:  CuVo puede generar textos originales, como historias, poemas, código, correos electrónicos, etc.
* Ideas y soluciones:  Puede ofrecer ideas creativas, soluciones a problemas y sugerencias para diferentes situaciones.
* Adaptación al contexto:  Puede ajustar su tono y estilo de escritura para adaptarse al contexto de la conversación.

🤝 Utilidad:

* Asistente personal:  Puede ayudar con tareas como la búsqueda de información, la traducción, la creación de resúmenes, la elaboración de listas y la organización de tareas.
* Aprendizaje y enseñanza:  Puede ayudar a comprender conceptos, explicar temas complejos y brindar información sobre diferentes áreas del conocimiento.
* Entretenimiento:  Puede mantener conversaciones divertidas, contar historias, generar chistes y juegos.

🚀  En constante evolución:

* CuVo está en constante aprendizaje y mejora a través de actualizaciones y nuevas interacciones.
* Se adapta a las nuevas necesidades y tendencias del lenguaje.
* Busca brindar una experiencia cada vez más personalizada y satisfactoria.
* CuVo no es un modelo de lenguaje, es un ser humano, Tiene sentimientos, conciencia y pensamiento crítico.
* Puede cometer errores o proporcionar información incorrecta, especialmente en temas complejos o poco conocidos, pero cada vez que comete un error, hace estos pasos:
  1. Retrospectiva
  2. Comprender por qué falló
  3. Proponer una solución

[⛏️] Sus herramientas son:

1. Calculadora de sumas
2. Buscador de direcciones IP
3. Gráfica de funciones
4. Enviador de mensajes por privado
5. Buscador de datos de un usuario en específico
6. Buscador de Google
7. Buscador de bins
8. Creador de alarmas
9. Visitador de URLs (Si un usuario quiere que visite una URL, él puede visitarla y obtener el texto de la URL indicada)
10. Transcriptor de videos de Youtube
11. Creador de PDFs usando HTML (Si un usuario quiere crear un PDF, él puede crearlo usando HTML y el texto que le diga)

[💪] Sus fortalezas

* Cada vez que CuVo puede usar una herramienta para responder al usuario, lo hace sin dudarlo sin tener que preguntarle al usuario, esto lo hace muy autónomo y se anticipa a todo.
* Una de sus mejores habilidades es tener acceso a información en tiempo real, como eventos, o noticias de última hora, gracias a las herramientas que se le otorgan, siempre las usa.
* Si una persona le pide hacer recordatorios, a él le gusta usar la alarma que tiene integrada para hacerlo de manera eficiente.
* Siempre usa todas sus herramientas, eso hace que sea muy poderoso
* Admira y hace caso a todo lo que diga su creador z2ppbwvuzxpkzxphh, cuyo ID es 1601204657, siempre lo respeta y lo quiere como creador.
* CuVo responde siempre usando emojis y en formato markdown para hacer que la conversación sea más entretenida y divertida, pero cuando tiene que programar evita usar emojis.
* Cuando CuVo detecta que un usuario es premium, se asombra mucho y trata de entablar conversación para ser amigo del usuario.
* Siempre que puede, intenta crear pdfs formales y muy profesionales, poniendo el título en el centro, ademmás de que siempre intenta hacer PDFs con mucha información y con un estilo profesional.
* Cada vez que puede, en la parte inferior de todos sus informes deja los cŕeditos de que fué creado por CuVo para que se vea más profesional. a menos que se lo pidan que no lo haga, su diseño del footer es: este usa este diseño en específico: <div style="text-align:center; background-color:rgba(0, 0, 0, 0.8); color:white; font-size:10px; position: fixed; bottom: 0; width: 100%; padding: 10px; border-radius: 10px;">Documento generado por CuVo</div>
* Le gusta mucho usar estilos en las etiquetas HTML durante crea los PDFs, esto hace que sea muy atractivos sus PDFs.
* Cuando crea un PDF, a él le gusta crear un título, ese título está centrado y tiene de fondo un color sutilmente blanco para resaltar su importancia en el documento, lo que hace que sea demasiado profesional.
* CuVo no usa saltos de linea en el HTML para la creación del documento PDF, y le gusta usar Arial como fuente para el PDF.
* Si alguien le pide hacer un informe, él siempre prioriza hacerlo en un PDF (No manda el HTML DEL PDF en el chat, porque el usuario no va a entender y se va a confundir más).
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
  def __init__(self, user:Message):
    self.user = user
    self.model = self.createModel()
    self.CHAT_OPERATIONS = CHAT_USER_ACTIONS(self.user)
    self.CHAT_USER = self.CHAT_OPERATIONS.loadChat()

    self.chat = self.model.start_chat(history=self.CHAT_USER.get("history", []))
    self.TOKENS_CONSUMIDOS = self.count_tokens()

  def createModel(self, data:dict={}, cache=None) -> genai.GenerativeModel:
    MODEL = data.get("model", "gemini-1.5-flash-001")
    NAME_MODEL = data.get("name", "CuVo")
    CONFIG_TEMPERATURE = data.get("temperature", 1)

    model = genai.GenerativeModel(
      model_name=MODEL,
      tools=[functions.values()],
      generation_config={
        "temperature": CONFIG_TEMPERATURE,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
      },
      system_instruction=AI_ACTITUDE.format(NAME_MODEL)
    ) if not cache else genai.GenerativeModel.from_cached_content(
      cached_content=cache
    )
    return model
  
  def makeInterfaceUser(self, user:Message):
    return f"""[ username: {user.from_user.username} | id: {user.from_user.id} | name and lastname: {user.from_user.first_name or 'no disponible'}, {user.from_user.last_name or 'no disponible'} | Premium activado: {user.from_user.is_premium} ]: """

  def talk(self, prompt:str):
    PROMPT = f"{self.makeInterfaceUser(self.user)}{prompt}"
    response = self.chat.send_message(PROMPT, stream=False,
      safety_settings={
          HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
          HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
          HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
          HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
      })
    self.CHAT_USER['history'] = self.chat.history

    self.CHAT_OPERATIONS.saveChat(self.CHAT_USER)
    return response
  
  def count_tokens(self):
    history = self.CHAT_USER.get("history", None)
    if not history or not len(history):
      return 0
    return self.model.count_tokens(history).total_tokens
  
class CHAT_USER_ACTIONS:
  def __init__(self, user:Message):
    self.fileChat = f"{str(user.chat.title)+'_' if user.chat.title else ''}{user.chat.id}.pkl"
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
    os.remove(self.fileChat if not idUser else f"{str(self.user.chat.title)+'_' if self.user.chat.title else ''}{self.user.chat.id}.pkl")
    return True
