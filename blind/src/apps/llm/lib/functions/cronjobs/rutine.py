from pyrogram import Client
from pyrogram.types import Message
from .core import Agenda, Rutina
from blind.src.utils.utilities import printTest

async def crear_rutina(nombre_horario:str, hora:str, dias_semana:list[str], zona_horaria:str, **kwargs) -> str:
    """
    Una funcion que el asistente podrá usar para así ayudarlo a establecer rutinas que se repitirán a base de los intervalos que se establezcan, con el objetivo de evitar la procrastinación y aumentar la productividad.
    Antes de establecer la rutina, el asistente debe asegurarse de preguntarle al usuario de qué país es o qué zona horaria debe basarse para que las alarmas se ajusten a base de ello.
    Es necesario solicitar al usuario que ingrese el nombre del horario y los días de la semana en los que se repetirá el recordatorio para evitar que se confunda.

    Args:
        nombre_horario (str): Nombre del horario.
        hora (str): Hora del recordatorio en formato HH:MM de 24 horas.
        dias_semana (list): Lista de días de la semana en los que se repetirá el recordatorio, por ejemplo: ["lunes", "miércoles", "viernes"].
        zona_horaria (str): Zona horaria del recordatorio, por ejemplo: "America/Mexico_City".

    Retorna:
        El ID del horario creado.
    """
    message: Message = kwargs.get("message", None)
    client: Client = kwargs.get("client", None)

    RUTINA = Rutina(
        dias=dias_semana,
        hora=hora,
        utc=zona_horaria,
        id_chat=str(int(message.chat.id)),
        message=nombre_horario
    )
    printTest(message)
    print (RUTINA.__dict__())

    result = Agenda().createRutinas(RUTINA)

    await message.reply_text(f"[📅] <b>CuVo</b> ha creado el horario <i>{nombre_horario}</i> con éxito.")
    return {"results":result}

async def olvidar_rutina(ID_RUTINA:int, **kwargs) -> str:
    """
    Esta función le permite al asistente olvidar una rutina de la lista de rutinas.

    Args:
        ID_RUTINA (int): ID del horario.

    Retorna:
        Un estado de respuesta booleano.
    """
    message: Message = kwargs.get("message", None)
    client: Client = kwargs.get("client", None)

    result = Agenda().deleteRutinas(str(int(message.chat.id)), str(int(ID_RUTINA)))

    await message.reply_text(f"[📅] <b>CuVo</b> está eliminado el horario <i>{str(int(ID_RUTINA))}</i>.")
    return {"results":result}

async def listar_rutinas(**kwargs) -> str:
    """
    Una funcion que el asistente podrá usar para así ayudarlo a listar rutinas que se repitirán a base de los intervalos que se establezcan, con el objetivo de evitar la procrastinación y aumentar la productividad.
    
    Retorna:
        El diccionario con las rutinas encontradas.
    """
    message: Message = kwargs.get("message", None)
    client: Client = kwargs.get("client", None)

    result = Agenda().loadRutinas(ID_CHAT=message.chat.id)

    await message.reply_text(f"[📅] <b>CuVo</b> ha listado los horarios de este chat.")
    return {"results":result}

async def modificar_rutina(ID_RUTINA:int, value:str, key:str, **kwargs) -> str:
    """
    Esta función le permite al asistente modificar una rutina de la lista de rutinas.

    Args:
        ID_RUTINA (int): ID del horario.
        value (str): Valor a modificar.
        key (str): Clave a modificar.

    Retorna:
        Un estado de respuesta booleano.
    """
    message: Message = kwargs.get("message", None)
    client: Client = kwargs.get("client", None)

    RUTINA = Agenda().getRutina(ID_CHAT=str(int(message.chat.id)), ID_RUTINA=str(int(ID_RUTINA)))
    RUTINA[key] = value
    RUTINA = Rutina(**RUTINA)

    result = Agenda().modifyRutinas(str(int(message.chat.id)), str(int(ID_RUTINA)), rutina=RUTINA)

    await message.reply_text(f"[📅] <b>CuVo</b> está modificando el horario <i>{str(int(ID_RUTINA))}</i>.")
    return {"results":result}