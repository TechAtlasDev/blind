from pyrogram import Client
from pyrogram.types.messages_and_media.message import Message

async def ejecutar(file_name:str, **kwargs):
  """
  Ejecuta esta función para poder ejecutar el script de python, está diseñado para probar el output para que el asistente pueda comprender si el script está listo o necesita mejorar algo.

  Args:
    file_name (str): El nombre del archivo de desarrollo (ejemplo: script.py)

  Returns:
  El output del archivo de desarrollo.
  """
  message:Message = kwargs.get("message", None)
  client:Client = kwargs.get("client", None)

  await message.reply_text(f"[⚡️] <b>Conda</b> está ejecutando el script.")

  try:
    with open(file_name, "r") as f:
      code = f.read()
    output = exec(code)
    return {"results": output}
  except FileNotFoundError:
    return {"results":"Archivo script.py no encontrado."}
  except Exception as e:
    return {"results":f"Error al ejecutar el código: {e}"}