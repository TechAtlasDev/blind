from jinja2 import Template
import pdfkit, os
import random
from pyrogram import Client
from pyrogram.types.messages_and_media.message import Message

async def crear_pdf_html(html_str:str, titulo_pdf:str, **kwargs):
    """
    Convierte un string HTML a un archivo PDF.
    
    Parameters:
        html_str (str): El contenido HTML en formato de cadena.    
    Returns:
        nombre de archivo
    """
    message: Message = kwargs.get("message", None)
    client: Client = kwargs.get("client", None)

    await message.reply_text(f"[📝] <b>CuVo</b> está creando un PDF.")

    # Generar el nombre de archivo único
    filename = f"{titulo_pdf}_{random.randint(0, 100)}.pdf"

    html_str = html_str.replace('\n', '')
    html_str = html_str.replace('\\n', '')
    html_str = html_str.replace('\n', '')
    html_str = html_str.replace('\\\n', '')

    # Renderizar el HTML con el contexto proporcionado
    template = Template(html_str)
    rendered_html = template.render({})

    # Opciones para pdfkit (A4 y sin márgenes)
    options = {
        'margin-top': '10mm',
        'margin-right': '10mm',
        'margin-bottom': '10mm',
        'margin-left': '10mm',
        'encoding': 'UTF-8'
    }
    pdfkit.from_string(rendered_html, filename, options=options)

    # Enviar el PDF como documento en el chat
    await client.send_document(chat_id=message.chat.id, document=filename)
    os.remove(filename)
    return {"results": f"PDF creado con éxito: {filename}"}
