from pyrogram import Client
from pyrogram.types.messages_and_media.message import Message
import matplotlib.pyplot as plt
import numpy as np
import io

async def graficar(function:str, **kwargs):
    message:Message = kwargs.get("message", None)
    client:Client = kwargs.get("client", None)

    x = np.linspace(-10, 10, 100)
    y = eval(function)

    plt.clf()

    # Creando la nueva gráfica
    plt.plot(x, y)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Gráfica de la función: " + function)
    plt.grid(True)

    # Guardando la gráfica como una imagen en memoria
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    await client.send_photo(message.chat.id, buffer)
    return {"results": "Grafica enviada al chat con exito"}