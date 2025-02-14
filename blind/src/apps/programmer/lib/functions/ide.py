from pyrogram import Client
from pyrogram.types.messages_and_media.message import Message
import re

async def ide(code: str, file_name: str, **kwargs):
    """
    Permite escribir en el archivo de desarrollo código en python, para poder ser ejecutado luego con la función "ejecutar".

    IMPORTANTE: No se tiene que usar funciones como "input" ni cualquier otra cosa que requiera interacción con la terminal, ya que esto causará que el sistema espere respuesta del usuario, en su lugar establece variables.

    Args:
        code (str): El código a escribir en el archivo de desarrollo, ejemplo: 'import random\\n# Genera un número aleatorio entre 1 y 10\\nnumero_aleatorio = random.randint(1, 10)\\n\\nprint("Número aleatorio generado: ", numero_aleatorio)'

        file_name (str): El nombre del archivo de desarrollo (ejemplo: script.py)
    Returns:
        True o False dependiendo del éxito al guardar el código en el archivo de desarrollo.
    """
    message = kwargs.get("message", None)
    client = kwargs.get("client", None)

    await message.reply_text(f"[⚡️] <b>Conda</b> está verificando el script.")

    # Validar que el código no contenga funciones problemáticas
    prohibited_patterns = [r'\binput\b', r'\bgetpass\b']  # Palabras clave prohibidas
    for pattern in prohibited_patterns:
        if re.search(pattern, code):
            return {"results": "[⚠️] El script contiene funciones problemáticas como 'input'. Por favor, elimínalas y vuelve a intentarlo. (consejo: reemplaza el valor de los input por constantes)"}

    try:
        with open(file_name, "w") as f:
            code = code.replace("\\n", "\n")
            code = code.replace("\\", '')
            f.write(str(code))
        await message.reply_text(f"[✅] Script guardado correctamente en {file_name}.")
        return {"results": True}
    except FileNotFoundError:
        return {"results": "Archivo no encontrado."}
    except Exception as e:
        return {"results": f"Error al guardar el código: {e}"}