# Funcion que sirve para controlar acciones que se reciban
from pyrogram import Client
from pyrogram.types.bots_and_keyboards.callback_query import CallbackQuery
#from src.apps.llm.lib.objects import AICUVO

from src.utils.vars import ADMIN_ID
from src.apps.llm.lib.objects import CHAT_USER_ACTIONS

async def main(client:Client, CallbackQuery:CallbackQuery, postdata=0):
  if postdata == "clear":
    if CallbackQuery.from_user.id == int(ADMIN_ID):
      CHAT_USER_ACTIONS(CallbackQuery.message).deleteChat(CallbackQuery.from_user.id)
#      AICUVO.chat = AICUVO.model.start_chat(history=[])
      await CallbackQuery.answer("Memoria limpia con exito")
      await CallbackQuery.message.reply_text("[⚠️] LA MEMORIA DE CUVO ESTÁ LIMPIA.")
    else:
      await CallbackQuery.answer(f"Oye 😡 no permitiré que me borres la memoria, me lo ordenó mi creador.")

  else:
    await CallbackQuery.answer(f"No se encontró un comando cuyo nombre sea: {postdata}")