from pyrogram import Client, filters
from pyrogram.types import Message
from google.generativeai.types.generation_types import GenerateContentResponse
from pyrogram import enums

from .lib.path import functions

from blind.src.apps.llm.lib.objects import CHAT
from blind.src.apps.llm.lib.handler import HandlerResponseJSON

from blind.src.utils.utilities import clearComand
from blind.src.utils.buttons import keymakers

CONDA_PROMPT = """Conda es una programadora profesional que tiene la capacidad de poder desarollar todo lo que le digan en ÚNICAMENTE python, una de las cosas que lo diferencian de los demás es que tiene la capacidad de usar herramientas que le permitirán programar, ejecutar su código y si algo falla durante la ejecución, volverlo a intentar para entregar un trabajo perfecto tal y como el usuario quiere.


Ella tiene la regla ética y moral de solo ejecutar código cuyos fines no sean maliciosos ni que traten de hacking, con el objetivo de evitar que las personas hagan un mal uso de Conda."""

@Client.on_message((filters.command("conda") & filters.text) | (filters.private & filters.text))
async def CUVO(client: Client, message: Message):
        
    text_user = clearComand(message.text)

    # Si el texto adicional está vacío
    if not text_user or text_user == "":
        return await message.reply("Un programador en python!")

    await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)

    # Enviado el mensaje a la IA
    CONDA = CHAT(message, client, PROMPT=CONDA_PROMPT, name_model="conda", tools="code_execution")
    RESPONSE:GenerateContentResponse = await CONDA.talk(text_user)

    if not RESPONSE:
        await client.send_chat_action(message.chat.id, enums.ChatAction.CANCEL)
        return "_"
    
    # Procesando la respuesta
    HANDLER = HandlerResponseJSON(RESPONSE, message, client)
    await HANDLER.execute(functions=functions)

    client.set_parse_mode(enums.ParseMode.MARKDOWN)
    await client.send_chat_action(message.chat.id, enums.ChatAction.CANCEL)