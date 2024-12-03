from pyrogram import Client
from pyrogram.types.messages_and_media.message import Message

import requests, json

async def searchShodan(query:str, facet:str, limit:int, **kwargs):
  """
  Buscador de shodan que usa la API oficial de Shodan, las consultas tienen la capacidad de tener todos los filtros disponibles en Shodan, incluyendo filtros exclusivos como "vuln", "tag", "before", "after", etc.

  Args:
      query (str): Consulta de búsqueda.
      facet (str): Faceta de búsqueda.
      limit (int): Límite de resultados.

  Retorna:
      Un diccionario con los resultados de la búsqueda.
  """
  message:Message = kwargs.get("message", None)
  client:Client = kwargs.get("client", None)

  try:
    await message.reply_text(f"[💻] <b>CuVo</b> está usando Shodan: <code>{query}</code>.")
    response = requests.post(f"https://prl412-web-backend.vercel.app/api/search", data={"query": query, "facets": facet, "limit": limit}).json()
    return {"results": response}
  except Exception as e:
    return {"results": f"Error al obtener información de los datos solicitados: {e}"}