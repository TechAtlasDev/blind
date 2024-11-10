from pyrogram import Client, filters
from pyrogram.types import Message
from .lib.handler import HandlerResponseJSON
from .lib.objects import CHAT
from google.generativeai.types.generation_types import GenerateContentResponse
from pyrogram import enums

from src.utils.utilities import printTest
from src.utils.buttons import keymakers

@Client.on_message(filters.command("cuvo") | filters.private)
async def CUVO(client: Client, message: Message):
        
    text_user = message.text[len(message.text.split(" ")[0]):].strip() if message.text.startswith("/") else message.text

    # Si el texto adicional está vacío
    if not text_user or text_user == "":
        botones = keymakers(["🧹 Limpiar memoria"], ["cuvoAction-clear"])
        return await message.reply("CuVo es un asistente experimental diseñado para ayudarte a hacer cosas muy interesantes con el poder de la IA!.\n\n**[⛏️] Sus herramientas son:**\n\n1. Calculadora de sumas\n2. Buscador de direcciones IP\n3. Gráfica de funciones\n4. Enviador de mensajes por privado\n5. Buscador de datos de un usuario en específico\n6. Buscador de Google\n7. Buscador de bins [Aún por terminar]\n8. Creador de alarmas\n9. Visitador de webs\n\nEspero que te guste!", reply_markup=botones)

    mensaje_respuesta = "Generando respuesta..."

    sent_message = await message.reply(mensaje_respuesta)

    # Enviado el mensaje a la IA
    AICUVO = CHAT(message)
    RESPONSE:GenerateContentResponse = AICUVO.talk(text_user)

    printTest(RESPONSE.parts) # -- Debug

    # Procesando la respuesta
    HANDLER = HandlerResponseJSON(RESPONSE, message, client)
    await HANDLER.execute()

    client.set_parse_mode(enums.ParseMode.MARKDOWN)
    await sent_message.delete()
#    await sent_message.edit(f"[✅] Respuesta procesada con éxito\n\n -> ```\n{str(RESPONSE.parts)[:4000]}\n```")