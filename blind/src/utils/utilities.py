import google.generativeai as genai
from pyrogram import Client

from .vars import IS_PROD, ADMIN_ID

def clearComand(message:str):
   # Eliminando el comando
    return "" if not message else message[len(message.split(" ")[0]):].strip() if message.startswith("/") else message

def printTest(data:any, spacing=10, **kwargs):
    """
    Prints the given data with a specified spacing.

    Args:
        data (any): The data to be printed.
        spacing (int, optional): The number of spaces to be added before the data. Defaults to 10.
    """
    textKwargs = ""
    for param in kwargs.keys():
        textKwargs += f"\n[+] {param} -> {kwargs[param]}"
    
    print("\n" * spacing + f"------------------------------------\n\n{data}\n\n---\n[+] Type: {type(data)}{textKwargs}\n\n-------------------------------------")

async def printError(data:Exception, client:Client):
    """
    Prints the given data with a specified spacing.

    Args:
        data (any): The data to be printed.
        spacing (int, optional): The number of spaces to be added before the data. Defaults to 10.
    """
    errorMetadata = {
        "error": data,
        "type": type(data),
        "line": data.__traceback__.tb_lineno,
        "file": data.__traceback__.tb_frame.f_code.co_filename,
        "function": data.__traceback__.tb_frame.f_code.co_name,
        "message": data.__traceback__.tb_frame.f_locals.get("message", None),
    }
    textKwargs = ""
    
    for param in errorMetadata.keys():
        textKwargs += f"\n[+] {param} -> {errorMetadata[param]}"

    print("\n" * 2 + f"---------  ERROR  ---------------\n\n{data}\n\n---\n[+] Type: {type(data)}{textKwargs}\n\n-------------  ERROR  --------------")
    if IS_PROD:
        print ("Enviando bug")
        await client.send_message(chat_id=ADMIN_ID, text=f"Error en el servidor:\n\n{data}\n\n[+] Type: {type(data)}{textKwargs}\n\n+++++++++++  ERROR  +++++++++++")

def downloadMedia(client:Client, file_id:str):
  """Downloads the media from the given message and saves it to the specified path.

  Args:
    message: The message containing the media to be downloaded.
    path: The path where the media will be saved.

  Returns:
    The path of the downloaded media.
  """
  file_path = client.download_media(file_id)
  return file_path

def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file
