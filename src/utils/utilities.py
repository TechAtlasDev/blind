import google.generativeai as genai

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

def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file
