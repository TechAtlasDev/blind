import asyncio
from pyrogram import Client
from pyrogram.types import Message

async def alarma(time_value: float, postdata: str, time_unit: str = "hours", **kwargs):
    """
    Programa un mensaje de recomendación que se enviará después de un tiempo específico,
    definido en horas, minutos o segundos.

    Parámetros:
    -----------
    time_value : float
        La cantidad de tiempo que se espera antes de enviar el mensaje. Puede ser un número entero o decimal.
        
    postdata : str
        El mensaje de recomendación que se enviará al chat después del tiempo especificado.
        
    time_unit : str, opcional
        La unidad de tiempo de `time_value`. Puede ser "hours", "minutes" o "seconds". 
        Por defecto, es "hours".

    Retorna:
    --------
    dict
        Un diccionario que contiene un mensaje indicando que la alarma fue programada exitosamente.
        
        - "results": str
            Un mensaje indicando que la alarma se programó correctamente.
        
        - "error": str (si aplica)
            Un mensaje de error si el `message` o `client` no fueron proporcionados,
            o si la unidad de tiempo es inválida.
    """
    message: Message = kwargs.get("message", None)
    client: Client = kwargs.get("client", None)

    if not message or not client:
        return {"error": "Debe proporcionar el mensaje y el cliente."}

    # Convertir la unidad de tiempo a segundos
    if time_unit == "hours":
        seconds_to_wait = time_value * 3600
    elif time_unit == "minutes":
        seconds_to_wait = time_value * 60
    elif time_unit == "seconds":
        seconds_to_wait = time_value
    else:
        return {"error": "Unidad de tiempo inválida. Use 'hours', 'minutes' o 'seconds'."}

    # Notificar al usuario que la alarma está programada
    """await message.reply_text(
        f"La alarma está programada y se ejecutará en {time_value} {time_unit}."
    )"""

    # Llamar a la función auxiliar para enviar el mensaje después del tiempo de espera
    asyncio.create_task(enviar_mensaje_despues(client, message.chat.id, postdata, seconds_to_wait, message=message))

    return {"results": f"La alarma se programó para dentro de {time_value} {time_unit}."}


async def enviar_mensaje_despues(client: Client, chat_id: int, postdata: str, delay: float, message):
    from src.apps.llm.lib.objects import AICUVO
    from src.apps.llm.lib.handler import HandlerResponseJSON

    """
    Función auxiliar que espera el tiempo especificado y luego envía el mensaje al chat.

    Parámetros:
    -----------
    client : Client
        La instancia de cliente de Pyrogram.
        
    chat_id : int
        El ID del chat donde se enviará el mensaje.
        
    postdata : str
        El contenido del mensaje que se enviará después de la espera.
        
    delay : float
        Tiempo en segundos que se esperará antes de enviar el mensaje.
    """
    await asyncio.sleep(delay)
    await client.send_message(chat_id=chat_id, text=f"[ ⏰ ] LA ALARMA DE {delay} TERMINÓ -> <i>{postdata}</i>")
    
    # Enviado el mensaje a la IA
    RESPONSE = AICUVO.talk(f"[SYSTEM] Se terminó la alarma, su postdata era: {postdata}", message)

    # Procesando la respuesta
    HANDLER = HandlerResponseJSON(RESPONSE, message, client)
    await HANDLER.execute()