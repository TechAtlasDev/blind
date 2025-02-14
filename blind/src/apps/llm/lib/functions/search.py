from pyrogram import Client
from pyrogram.types.messages_and_media.message import Message
from blind.src.utils.vars import GOOGLE_KEY_CX, GOOGLE_KEY_SEARCH_ENGINE_CUSTOM
from googleapiclient.discovery import build

class objectSearch:
    def __init__(self, data:dict):
        self.data = data

        self.title = data.get("Titulo", None)
        self.description = data.get("Descripcion", None)
        self.url = data.get("URL", None)
    def __dict__(self):
        return self.data

def searcher(query:str) -> list[objectSearch]:
    service = build("customsearch", "v1", developerKey=GOOGLE_KEY_SEARCH_ENGINE_CUSTOM)
    res = service.cse().list(q=query, cx=GOOGLE_KEY_CX).execute()
    
    # Procesa los resultados
    resultados = []
    for item in res.get("items", []):
        resultado = objectSearch({
            "Titulo": item.get("title"),
            "Descripcion": item.get("snippet"),
            "URL": item.get("link")
        })
        resultados.append(resultado)
    
    return resultados

async def google_search(search:str, **kwargs):
  message:Message = kwargs.get("message", None)
  client:Client = kwargs.get("client", None)
  
  await message.reply_text(f"[🔎] <b>CuVo</b> buscando por internet <code>{search}</code>.")

  responseSearch = searcher(search)
  MESSAGE = "Resultados de búsqueda\n\n"
  
  for result in responseSearch:
    MESSAGE += f"Título: {result.title}\nDescripccion: {result.description}\nURL: {result.url}\n\n"
  
#  await message.reply(f"[✅] CUVO ESTÁ USANDO EL BUSCADOR DE GOOGLE -> {search}")
  return {"results": MESSAGE}