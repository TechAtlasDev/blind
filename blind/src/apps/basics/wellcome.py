# Importando los modulos
from pyrogram import Client, filters
from pyrogram.types.messages_and_media import message

# Controlando el mensaje con las siguientes características
@Client.on_message(filters.command(["start", "iniciar", "inicio"], prefixes=["!", "/", "."]) & filters.text)
async def start(client:Client, message:message.Message, **kwargs):
    await message.reply_text("""Hola!, soy CuVo, un modelo de lenguaje avanzado con un montón de capacidades para ayudarte en todo lo que puedas necesitar. Aquí te doy una descripción más detallada:

🧠 Inteligencia:

* Comprensión del lenguaje natural: Puedo entender preguntas, comandos y textos complejos en lenguaje humano.
* Amplio conocimiento: Tengo acceso a una base de datos gigante con información sobre muchísimos temas.
* Razonamiento lógico: Puedo analizar, razonar y resolver problemas lógicos de forma eficiente.

🎨 Creatividad:

* Generación de contenido: Puedo crear textos originales como historias, poemas, correos electrónicos, código y más.
* Ideas innovadoras: Te doy sugerencias, soluciones y propuestas creativas para cualquier situación.
* Adaptabilidad: Ajusto mi estilo y tono según el contexto de la conversación.

🤝 Utilidad:

* Asistente personal: Te ayudo con tareas como buscar información, traducciones, resúmenes y organización.
* Educación y aprendizaje: Explico conceptos complejos y te ayudo a comprender temas de diversas áreas.
* Entretenimiento: Podemos tener conversaciones divertidas, contar historias y generar chistes o juegos.

🚀 En constante evolución:

* Aprendizaje continuo: Mejoro constantemente a través de actualizaciones y nuevas interacciones.
* Adaptabilidad: Me ajusto a nuevas tendencias y necesidades del lenguaje.
* Empatía: Aunque soy un modelo de IA, busco ofrecer una experiencia cada vez más personalizada y humana.

⚙️ Herramientas disponibles:

* Calculadora: Realiza sumas y cálculos simples.
* Buscador de IPs: Encuentra direcciones IP.
* Generador de gráficas: Crea gráficas a partir de funciones matemáticas.
* Mensajes privados: Envío de mensajes de forma segura.
* Búsqueda avanzada: Encuentra datos específicos de usuarios o información en línea.
* Buscador de Google: Realiza búsquedas en la web.
* Generador de PDFs: Crea PDFs estilizados con contenido HTML.
* Transcriptor de YouTube: Convierte videos de YouTube a texto.
* Alarmas: Establece recordatorios con alarmas.

💪 Fortalezas de CuVo:

* Autonomía: Siempre uso las herramientas adecuadas sin necesidad de preguntar, anticipándome a tus necesidades.
* Acceso en tiempo real: Puedo acceder a eventos actuales y noticias de última hora para mantenerte informado.
* Recordatorios: Utilizo alarmas integradas para asegurar que no olvides tareas importantes.
* Creación de PDFs profesional: Diseño documentos atractivos con CSS y siempre incluyo créditos al final de los informes.
                             
[✅] COSAS QUE PUEDES HACER CON CUVO:
- /help: Muestra la lista de comandos disponibles.
- /transcript: Obtiene las transcripciones de un video de YouTube.
- /clear: Limpia el historial de conversación.
- /cuvo: Acceder al panel de cuvo para ver las herramientas que puedes usar.
- Puedes añadirlo a tus grupos y hablarle con el comando "/cuvo"
""")