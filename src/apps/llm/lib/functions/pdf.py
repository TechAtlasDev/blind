import os
import markdown2
import pdfkit
import random
from pyrogram import Client
from pyrogram.types.messages_and_media.message import Message

async def crear_pdf_markdown(markdown_text: str, **kwargs):
    """Crea un archivo PDF a partir de texto en markdown.

    Args:
        markdown_text: El texto en formato markdown.

    Returns:
        El nombre del archivo PDF generado.
    """
    
    message: Message = kwargs.get("message", None)
    client: Client = kwargs.get("client", None)

    # Reemplazar saltos de línea \n con dos saltos de línea para respetar el formato de Markdown
    markdown_text = markdown_text.replace('\n', '  \n')

    # Generar el nombre de archivo único
    filename = f"{message.from_user.id}_{random.randint(0, 100)}.pdf"

    # Convertir Markdown a HTML
    html = markdown2.markdown(markdown_text, extras=["fenced-code-blocks", "tables"])

    # Opciones de configuración para pdfkit para que use UTF-8
    pdfkit_options = {
        "encoding": "UTF-8",
        "enable-local-file-access": None,  # Necesario si usas rutas locales
    }

    # Convertir HTML a PDF
    pdfkit.from_string(html, filename, options=pdfkit_options)

    # Enviar el PDF como documento en el chat
    await client.send_document(chat_id=message.chat.id, document=filename)
    os.remove(filename)
    return {"results": f"PDF creado con éxito: {filename}"}
