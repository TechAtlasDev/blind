from pyrogram import Client, filters
from pyrogram.types import Message
from .lib.handler import HandlerResponseJSON
from .lib.objects import CHAT
from google.generativeai.types.generation_types import GenerateContentResponse
from pyrogram import enums

from src.utils.utilities import upload_to_gemini, clearComand, downloadMedia, printTest
from src.utils.buttons import keymakers

print ("Alerta de prueba")

@Client.on_message((filters.command("cuvo") & filters.text) | (filters.private & filters.text))
async def CUVO(client: Client, message: Message):
        
    text_user = clearComand(message.text)

    # Si el texto adicional está vacío
    if not text_user or text_user == "":
        botones = keymakers(["🧹 Limpiar memoria"], ["cuvoAction-clear"])
        return await message.reply("CuVo es un asistente experimental diseñado para ayudarte a hacer cosas muy interesantes con el poder de la IA!.\n\n**[⛏️] Sus herramientas son:**\n\n1. Calculadora de sumas\n2. Buscador de direcciones IP\n3. Gráfica de funciones\n4. Enviador de mensajes por privado\n5. Buscador de datos de un usuario en específico\n6. Buscador de Google\n7. Buscador de bins [Aún por terminar]\n8. Creador de alarmas\n9. Visitador de webs\n\nEspero que te guste!", reply_markup=botones)

    mensaje_respuesta = "Generando respuesta..."

    sent_message = await message.reply(mensaje_respuesta)

    # Enviado el mensaje a la IA
    AICUVO = CHAT(message)
    RESPONSE:GenerateContentResponse = AICUVO.talk(text_user)

    # Procesando la respuesta
    HANDLER = HandlerResponseJSON(RESPONSE, message, client)
    await HANDLER.execute()

    client.set_parse_mode(enums.ParseMode.MARKDOWN)
    await sent_message.delete()

@Client.on_message((filters.photo | filters.media_group & filters.private) | (filters.photo & filters.command("cuvo")))
async def CUVO_CAPTION(client: Client, message: Message):
    DESCRIPCION = clearComand(message.caption) if message.caption else ""
    PATHFILES = []

    if message.media_group_id:
        # Obtener el grupo de medios usando el `media_group_id`
        media_group = await client.get_media_group(message.chat.id, message.id)

        # Descargar cada archivo de foto en el grupo de medios
        for c, media in enumerate(media_group):
            if media.photo:  # Asegurarse de que el archivo sea una foto
                PATH = await downloadMedia(client, media.photo.file_id)
                PATHFILES.append(PATH)
                if media.caption:  # Concatenar descripción si existe
                    DESCRIPCION += f"\nDESCRIPCIÓN DE FOTO {c + 1}: {media.caption}"

    # Si el mensaje es una sola foto
    elif message.photo:
        PATH = await downloadMedia(client, message.photo.file_id)
        PATHFILES.append(PATH)

    # Subir imágenes a Gemini y guardar URLs
    IMAGEPARTS = []
    for image in PATHFILES:
        uploaded_file = upload_to_gemini(image)
        IMAGEPARTS.append(uploaded_file.uri)  # Extraer solo el URI

    mensaje_respuesta = "Generando respuesta..."
    sent_message = await message.reply(mensaje_respuesta)

    # Enviado el mensaje a la IA
    AICUVO = CHAT(message)
    PARTCONTEXT = IMAGEPARTS + [DESCRIPCION]
    printTest(PARTCONTEXT)  # -- Debug

    # Enviar solo los URIs en el mensaje a Gemini
    RESPONSE: GenerateContentResponse = AICUVO.chat.send_message(PARTCONTEXT)

    # Ejecutar el handler con la respuesta
    HANDLER = HandlerResponseJSON(RESPONSE, message, client)
    await HANDLER.execute()

    await sent_message.delete()
