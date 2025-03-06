![Banner telegram](image.png)

---

# BlindAI 🤖 

**BlindAI** es un bot de telegram desarrollado con el objetivo de explotar el potencial de la IA generativa y la disponibilidad de Telegram con el objetivo de crear un asistente cuyas capacidades sean altamente innovadoras gracias a la arquitectura del proyecto.

## 🎯 Objetivo

Desarrollar un bot de Telegram fácil de acceder, **gratuito**, escalable y con un enfoque de integración de herramientas cómodo y fácil, lo que permite enfocar la mayor parte del proyecto en la implementación y búsqueda de **innovación en el LLM** sin preocuparse por el apartado técnico del proyecto.

## 🛠️ Herramientas

El sistema cuenta con varias herramientas creadas de manera predefinida.

> [!NOTE]  
> Puede variar su disponibilidad en la demo oficial.

* 🧮 Calculadora de sumas
* 🔎 Buscador de direcciones IP
* 📈 Gráfica de funciones
* 💌 Enviador de mensajes por privado
* 🕵️‍♀️ Buscador de datos de un usuario en específico
* 🌎 Buscador de Google
* ⏰ Creador de alarmas
* 🌐 Visitador de URLs
* 🗣️ Transcriptor de videos de Youtube
* 🖨️ Creador de PDFs usando HTML

## 🖥️ Stack

* **Pyrogram:** Una librería de python que permite conectarse con la API de Telegram.
* **Google Generative AI:** Un SDK que permite interactuar con el LLM usando python.
* **Watchdogs:** Permite esperar cambios en archivos específicos.
* **Matplotlib:** Permite crear gráficos estadísticos.
* **Requests:** Interactuar con APIs externas.

## 🏁 Instalación

1. Clona este repositorio con:

```bash
git clone https://github.com/TechAtlasDev/blind
```

2. Entra al proyecto e instala las dependencias con:

```bash
cd blind
poetry install
```

3. Establece las variables de entorno en la ruta `blind/.env`, y establece las variables:

```conf
NAME="Nombre de la aplicación de telegram"
API_ID=id_del_bot_de_telegram_
API_HASH="Hash de la API de telegram"
BOT_TOKEN="Token del bot de telegram"
ADMIN_ID=id_del_administrador_del_bot
AI_TOKEN="Token de uso de la API de Google Generative AI, lo puedes encontrar en https://aistudio.google.com/apikey"
GOOGLE_KEY_SEARCH_ENGINE_CUSTOM="API KEY de credenciales de aplicación de Google Cloud Platform (Para realizar busquedas en Google)"
GOOGLE_KEY_CX="KEY CX de la aplicación de Google Cloud Platform"
```

4. Inicia el proyecto con:

```bash
poetry run dev
```

## 🧱 Estructura del proyecto

Como anteriormente se estableció, el bot cuenta con una arquitectura definida con el objetivo de priorizar la escalabilidad, fácil modificación e integración de herramientas.

### 1. Carpetas principales 

```
|- Apps: Las apps son carpetas que contienen un conjunto de herramientas específicas.
|- Downloads: La ruta en donde el bot de telegram hace descargas temporales de contenido, desde imágenes, documentos y cualquier otro contenido que el usuario se lo envíe.
|- Notifiers (En construcción): Sistemas especializados que se encargan de notificar al usuario por diferentes medios (como correos, mensajes de telegram, etc) cosas que el usuario le pidió al asistente.
|- Utils: Conjunto de herramientas auxiliares.
```

### 2. Aplicaciones

```
|- Basics: Comandos básicos como /start o /help
|- Group: Comandos especiales para realizar operaciones en grupos. 
|- LLM: Comandos especiales que se centran en el asistente (Aplicación principal).
|- Programmer (experimental): Un asistente especializado que tiene la capacidad de ejecutar comandos remotodos y programar.
|- postdata_controller.py: Permite controlar todo tipo de callback_querys que el sistema reciba.
```

### 3. Añadir funcionalidades al asistente:

Dentro de la aplicación "LLM", en la ruta `lib/functions` puedes crear un archivo nuevo, con la siguiente estructura inicial:

```python
# Para tipado de variables
from pyrogram import Client
from pyrogram.types.messages_and_media.message import Message

async def nombre_funcion(value:str, **kwargs):
  """
  Función que el LLM ejecutará.

  Params:
    * value: Parámetro que el LLM establecerá
  """

  message:Message = kwargs.get("message", None)
  client:Client = kwargs.get("client", None)

  await message.reply_text(f"<b>CuVo</b> ejecutó esta función nueva <code>{value}</code>.")

  return "La función se ejecutó!" # Este dato se retornará al LLM, no al usuario.
```

#### Cosas a tomar en cuenta:
* `nombre_funcion:` Este nombre de función ejecutará el LLM, asi que tiene que ser explicativo.
* `value`: Este parámetro el LLM retornará (recomiendo que sea explicativa).
* **Documentación de la función:** Si quieres que el LLM comprenda mejor el uso de la función, modifica su documentación dandole indicaciones
* `message` y `client`: Variables que contienen datos del bot de telegram y el usuario, te pueden servir para obtener sus datos y realizar operaciones avanzadas en el chat.
* `await message.reply_text(f"<b>CuVo</b> ejecutó esta función nueva <code>{value}</code>.")`: Mensaje que notificará al usuario que se está ejecutando una función.
* **Retorno:** El resultado de la función que será enviado al LLM, es necesario que el tipo del valor sea primitivo.

> [!WARNING]  
> No olvides tipar los parámetros de la función, para que el asistente sepa cómo responder.

### Función de ejemplo:

Una función que le permite al LLM realizar una resta con 2 digitos:

```python
# Para tipado de variables
from pyrogram import Client
from pyrogram.types.messages_and_media.message import Message

async def restar(x:int, y:int, **kwargs):
  """
  Función que permite al asistente restar dos valores.

  Parámetros:
    x (int): Primer número
    y (int): Segundo número
  """

  message:Message = kwargs.get("message", None)
  client:Client = kwargs.get("client", None)

  await message.reply_text(f"[🧠] <b>CuVo</b> está usando la calculadora.")

  # Realizando la operación
  resultado = x - y

  return resultado
```

### 4. Añadir funcionalidad a la lista de funcionalidades

Dentro de la aplicación "LLM", en la ruta `lib/path.py` vas a encontrar un diccionario, importa tu integración y añadela a la lista.

> [!WARNING]  
> La key tiene que tener el mismo nombre de la función que acabas de crear.

---

## ⚖️ Licencia

El proyecto cuenta con la licencia MIT.

## 📙 Soporte

Si tienes dudas, necesitas ayuda o tienes una sugerencia puedes contactarme en `gjimenezdeza@gmail.com`
