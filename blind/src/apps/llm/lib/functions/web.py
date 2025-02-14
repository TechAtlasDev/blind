from bs4 import BeautifulSoup
import requests

from pyrogram import Client
from pyrogram.types.messages_and_media.message import Message

from blind.src.utils.utilities import printTest

async def visitarURL(url:str, **kwargs):
    """
    Esta función permite enviar una URL con el objetivo de visitarla y obtener el texto que se encuentra dentro de ella

    Retorna: El texto que se encuentra dentro de la web visitada.
    """

    message:Message = kwargs.get("message", None)
    client:Client = kwargs.get("client", None)

    await message.reply_text(f"[👀] <b>CuVo</b> buscando visitando la URL {url}.")

    # Realizar la solicitud HTTP a la URL
    response = requests.get(url)
    response.raise_for_status()  # Asegura que la solicitud fue exitosa

    # Parsear el HTML de la página
    soup = BeautifulSoup(response.text, 'html.parser')

    # Obtener el texto puro de la página
    texto_puro = soup.get_text(separator=' ', strip=True)

    # Resultado final
    return {
        'results': texto_puro
    }