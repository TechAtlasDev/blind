import requests, json
from pyrogram import Client
from pyrogram.types.messages_and_media.message import Message

def findBin(bin):
  url = "https://bin-ip-checker.p.rapidapi.com/"

  querystring = {"bin":str(bin)}

  payload = {"bin":str(bin)}
  headers = {
    "x-rapidapi-key": "2226a2948dmsh609d06de6f27e41p1b31b8jsn43ca8fc497c0",
    "x-rapidapi-host": "bin-ip-checker.p.rapidapi.com",
    "Content-Type": "application/json"
  }

  response = requests.post(url, json=payload, headers=headers, params=querystring)
  return json.dumps(response.json(), indent=4)


async def getBin(bin:str, **kwargs):
    """
    Una función que sirve para para obtener información de una tarjeta de crédito
    """

    message:Message = kwargs.get("message", None)
    client:Client = kwargs.get("client", None)

    message.reply_text(f"[🧬] <b>CuVo</b> está buscando el bin {bin}.")

    results = findBin(bin)

    return {"results": results}