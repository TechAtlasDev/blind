from pyrogram import Client, filters
from pyrogram.types import Message
from .lib.handler import HandlerResponseJSON
from .lib.objects import CHAT
from google.generativeai.types.generation_types import GenerateContentResponse
from pyrogram import enums

from blind.src.utils.utilities import clearComand
from blind.src.utils.buttons import keymakers

@Client.on_message((filters.command("cuvo") & filters.text) | (filters.private & filters.text))
async def CUVO(client: Client, message: Message):
        
    text_user = clearComand(message.text)

    # Si el texto adicional está vacío
    if not text_user or text_user == "":
        botones = keymakers(["🧹 Limpiar memoria"], ["cuvoAction-clear"])
        return await message.reply("CuVo es un asistente experimental diseñado para ayudarte a hacer cosas muy interesantes con el poder de la IA!.\n\n**[⛏️] Sus herramientas son:**\n\n1. Calculadora de sumas\n2. Buscador de direcciones IP\n3. Gráfica de funciones\n4. Enviador de mensajes por privado\n5. Buscador de datos de un usuario en específico\n6. Buscador de Google\n7. Buscador de bins [Aún por terminar]\n8. Creador de alarmas\n9. Visitador de webs\n\n[⚠️] Si CuVo te dice que no sabe usar estas herramientas o que no puede ayudarte, es normal, y reinicia su memoria.", reply_markup=botones)

    await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)

    # Enviado el mensaje a la IA
    AICUVO = CHAT(message, client)
    RESPONSE:GenerateContentResponse = await AICUVO.talk(text_user)

    if not RESPONSE:
        await client.send_chat_action(message.chat.id, enums.ChatAction.CANCEL)
        return "_"

    # Procesando la respuesta
    HANDLER = HandlerResponseJSON(RESPONSE, message, client)
    await HANDLER.execute()

    client.set_parse_mode(enums.ParseMode.MARKDOWN)
    await client.send_chat_action(message.chat.id, enums.ChatAction.CANCEL)