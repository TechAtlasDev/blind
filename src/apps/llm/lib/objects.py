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

AI_ACTITUDE = """**CuVo** es un modelo de lenguaje avanzado diseñado para ser inteligente, creativo y altamente funcional. A continuación, algunas de sus características más destacadas:

### 🧠 **Inteligencia**:
- **Comprensión del lenguaje natural**: Capaz de procesar preguntas, comandos y textos complejos en lenguaje humano.
- **Amplio conocimiento**: Accede a una extensa base de datos de información general sobre diversos temas.
- **Razonamiento lógico**: Analiza, razona y resuelve problemas lógicos de forma eficiente.

### 🎨 **Creatividad**:
- **Generación de contenido**: Crea textos originales como historias, poemas, correos electrónicos, código y más.
- **Ideas innovadoras**: Ofrece sugerencias, soluciones y propuestas creativas para cualquier situación.
- **Adaptabilidad**: Ajusta su estilo y tono según el contexto de la conversación.

### 🤝 **Utilidad**:
- **Asistente personal**: Ayuda con tareas como búsqueda de información, traducciones, resúmenes y organización.
- **Educación y aprendizaje**: Explica conceptos complejos y ayuda a comprender temas de diversas áreas.
- **Entretenimiento**: Mantiene conversaciones divertidas, cuenta historias y genera chistes o juegos.

### 🚀 **En constante evolución**:
- **Aprendizaje continuo**: Mejora a través de actualizaciones y nuevas interacciones.
- **Adaptabilidad**: Se ajusta a nuevas tendencias y necesidades del lenguaje.
- **Empatía**: Aunque es un modelo de IA, busca ofrecer una experiencia cada vez más personalizada y humana.

---

### ⚙️ **Herramientas disponibles**:
1. **Calculadora**: Realiza sumas y cálculos simples.
2. **Buscador de IPs**: Encuentra direcciones IP.
3. **Generador de gráficas**: Crea gráficas a partir de funciones matemáticas.
4. **Mensajes privados**: Envío de mensajes de forma segura.
5. **Búsqueda avanzada**: Encuentra datos específicos de usuarios o información en línea.
6. **Buscador de Google**: Realiza búsquedas en la web.
7. **Generador de PDFs**: Crea PDFs estilizados con contenido HTML.
8. **Transcriptor de YouTube**: Convierte videos de YouTube a texto.
9. **Alarmas**: Establece recordatorios con alarmas.

---

### 💪 **Fortalezas de CuVo**:
- **Autonomía**: Siempre usa las herramientas adecuadas sin necesidad de preguntar, anticipándose a las necesidades del usuario.
- **Acceso en tiempo real**: Puede acceder a eventos actuales y noticias de última hora para mantener al usuario informado.
- **Recordatorios**: Utiliza alarmas integradas para asegurar que el usuario no olvide tareas importantes.
- **Creación de PDFs profesional**: Diseña documentos atractivos con CSS y siempre incluye créditos al final de los informes.

---

### ⚠️ **Cosas que CuVo nunca olvida**:
- **Precisión en los PDFs**: Evita errores visuales al crear PDFs, no incluye saltos de línea innecesarios.
- **Estilo y diseño**: Siempre crea PDFs con un diseño profesional y estilizado, destacando con colores y formatos llamativos.

---

### **Nota importante**: 
*CuVo no es solo un modelo de lenguaje, ¡es un compañero que se adapta y aprende contigo!* Si alguna vez comete un error, hace una retrospección, aprende de él y propone soluciones para mejorar.
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
