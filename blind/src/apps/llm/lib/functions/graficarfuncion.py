from pyrogram import enums
import matplotlib.pyplot as plt
import numpy as np
import os
import tempfile
from pyrogram import Client
from pyrogram.types.messages_and_media.message import Message
from blind.src.utils.utilities import upload_to_gemini

async def graficar(function_code_python_function: str, nombre_funcion:str="Función de CuVo", **kwargs):
    """
    Una función que sirve para graficar funciones en código python usando matplotlib y numpy.

    Parámetros:
    - code_python_function (str): Código de la función en python.
    - nombre_funcion (str): Nombre de la función a graficar.

    Retorna:
    - Un diccionario con los resultados de la función y los partes de la respuesta.
    """

    # Extrayendo argumentos opcionales
    message: Message = kwargs.get("message", None)
    client: Client = kwargs.get("client", None)

    client.set_parse_mode(enums.ParseMode.DEFAULT)
    await message.reply_text(f"[📊] <b>CuVo</b> está graficando la función ```python\n{function_code_python_function}\n```")

    # Generando los valores x y calculando y
    x = np.linspace(-10, 10, 100)
    y = eval(function_code_python_function)

    # Creando la gráfica
    plt.clf()
    plt.plot(x, y)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(nombre_funcion)
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
