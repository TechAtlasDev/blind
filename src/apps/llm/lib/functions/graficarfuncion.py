import matplotlib.pyplot as plt
import numpy as np
import os
import tempfile
from pyrogram import Client
from pyrogram.types.messages_and_media.message import Message
from src.utils.utilities import upload_to_gemini

async def graficar(function: str, **kwargs):
    """
    Una función que sirve para graficar funciones basadas en una entrada de función.

    Recibe: 
      function (str): La ecuación de la función sin incluir el signo "=".
                      Ejemplo: graficar("2*x+2")

    returns:
      Mensaje de confirmación.
    """

    # Extrayendo argumentos opcionales
    message: Message = kwargs.get("message", None)
    client: Client = kwargs.get("client", None)

    # Generando los valores x y calculando y
    x = np.linspace(-10, 10, 100)
    y = eval(function)

    # Creando la gráfica
    plt.clf()
    plt.plot(x, y)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Gráfica de la función: " + function)
    plt.grid(True)

    # Guardando la imagen en un archivo temporal
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        plt.savefig(temp_file, format="png")
        temp_file_path = temp_file.name

    # Subiendo la imagen a Gemini
    partPlot = upload_to_gemini(temp_file_path, "image/png")

    # Enviando la imagen al chat
    await client.send_photo(message.chat.id, temp_file_path)

    # Eliminando el archivo temporal
    os.remove(temp_file_path)

    return {"results": "Gráfica enviada al chat con éxito", "parts": [partPlot]}
