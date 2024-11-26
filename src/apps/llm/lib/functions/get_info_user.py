from pyrogram import Client
from pyrogram.types.messages_and_media.message import Message
from pyrogram.types.user_and_chats.user import User

async def fetchDataUser(id:int, **kwargs):
  message:Message = kwargs.get("message", None)
  client:Client = kwargs.get("client", None)

  await message.reply_text(f"[👥] <b>CuVo</b> está buscando la información con el ID {id}.")

  try:
    user:User = await client.get_users(user_ids=int(id))
    response = f"ID: {user.id}\nNombre: {user.first_name}\nApellido: {user.last_name}\nUsername: {user.username}"
    await message.reply("[✅] CUVO ESTÁ USANDO EL BUSCADOR DE DATOS DE USUARIOS.")
    return {"results": response}
  except Exception as e:
    return {"results": f"Error al obtener información del usuario: {e}"}