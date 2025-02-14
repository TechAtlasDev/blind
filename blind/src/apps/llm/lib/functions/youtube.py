#from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

from pyrogram import Client
from pyrogram.types.messages_and_media.message import Message

async def youtube_obtener_video_transcripcion(url:str, **kwargs):
    """
    Una herramienta que permite obtener las transcripciones de un video de youtube a través de la URL y como resultado entrega las transcripciones de dicho video

    Retorna: Transcripciones del video
    """

    message:Message = kwargs.get("message", None)
    client:Client = kwargs.get("client", None)

    await message.reply_text(f"[🧾] <b>CuVo</b> está obteniendo los subtítulos de tu video.")

    # Analiza la URL
    query = urlparse(url)
    
    # Verifica si es un enlace de YouTube Shorts o un enlace estándar de YouTube
    if "youtube.com/shorts/" in url:
        video_id = query.path.split("/shorts/")[-1]
    else:
        video_id = parse_qs(query.query).get("v")
        if video_id:
            video_id = video_id[0]  # Extrae el ID del video desde el parámetro 'v'
        else:
            raise ValueError("URL inválida o sin ID de video")

    # Obtiene la transcripción del video
    try:
#        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['es', 'en'])
        # Convierte la transcripción en un texto simple
#        texto = "\n".join([item['text'] for item in transcript])
        return {"results":"Funcionalidad en mantenimiento"}
    except Exception as e:
        print (f"Ocurrió un error en la transcripción -> {e}")
        return {"results": f"Error al obtener la transcripción, error: {e}"}