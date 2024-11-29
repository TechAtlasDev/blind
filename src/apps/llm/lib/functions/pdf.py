from jinja2 import Template
import pdfkit, os
import random
from pyrogram import Client
from pyrogram.types.messages_and_media.message import Message

async def crear_pdf_html(html_str:str, titulo_pdf:str="pdf_document", **kwargs):
    """
    Creador de PDFs que le permite al asistente crear un PDF a partir de código HTML, para esto, en el código HTML no tienen que haber saltos de linea (\\n), ya que provoca bugs en el documento.
    Es recomendable que se ponga un título en el HTML, ya que si no, el PDF no se creará correctamente.
    
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
    html_str = html_str.replace('\\', '')

    # Renderizar el HTML con el contexto proporcionado
    template = Template(html_str)
    rendered_html = template.render({})

    # Opciones para pdfkit (A4 y sin márgenes)
    options = {
        'encoding': 'UTF-8'
    }
    pdfkit.from_string(rendered_html, filename, options=options)

    # Enviar el PDF como documento en el chat
    await client.send_document(chat_id=message.chat.id, document=filename)
    os.remove(filename)
    return {"results": f"PDF creado con éxito: {filename}"}
