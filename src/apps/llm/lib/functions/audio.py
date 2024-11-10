from pyrogram import Client as ClientTG
from pyrogram.types.messages_and_media.message import Message

from pyht import Client
from pyht.client import TTSOptions

async def generar_audio(texto:str, **kwargs):
    """Genera un archivo de audio a partir de un texto.

    Args:
        texto (str): El texto a convertir en voz.

    Returns:
        str: El nombre del archivo de audio generado.
    """

    message:Message = kwargs.get("message", None)
    clientTG:ClientTG = kwargs.get("client", None)

    voice="s3://mockingbird-prod/william_vo_training_1b939b71-14fa-41f0-b1db-7d94f194ad0a/voices/speaker/manifest.json"
    output_format="mp3"

    # Reemplaza estas variables con tus credenciales de Play.ht:
    user_id = "JnwsOza0yzTLm5IqfiIP9ESz3XM2"
    api_key = "84e9badc984740db961337e7a6853d07"

    client = Client(user_id=user_id, api_key=api_key)
    options = TTSOptions(voice=voice, format=output_format)

    # Generamos el archivo de audio
    nombre_archivo = "audio.mp3"  # Nombre del archivo de audio
    with open(nombre_archivo, "wb") as f:
        for chunk in client.tts(texto, options):
            f.write(chunk)

    return {"results": nombre_archivo}