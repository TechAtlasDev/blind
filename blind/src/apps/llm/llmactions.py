# Funcion que sirve para controlar acciones que se reciban
from asyncio import sleep
from pyrogram import Client, filters
from pyrogram.types.bots_and_keyboards.callback_query import CallbackQuery
from pyrogram.types.messages_and_media.message import Message
#from blind.src.apps.llm.lib.objects import AICUVO

from blind.src.utils.vars import ADMIN_ID
from blind.src.apps.llm.lib.objects import CHAT_USER_ACTIONS

async def main(client:Client, CallbackQuery:CallbackQuery, postdata=0):
  if postdata == "clear":
    if CallbackQuery.from_user.id:
      CHAT_USER_ACTIONS(CallbackQuery.message).deleteChat(CallbackQuery.from_user.id)
      await CallbackQuery.answer("Memoria limpia con exito")
      await CallbackQuery.message.reply_text("[⚠️] LA MEMORIA DE CUVO ESTÁ LIMPIA.")
    else:
      await CallbackQuery.answer(f"Oye 😡 no permitiré que me borres la memoria, me lo ordenó mi creador.")

  else:
    await CallbackQuery.answer(f"No se encontró un comando cuyo nombre sea: {postdata}")

@Client.on_message(filters.command("clear"))
async def clear(client:Client, message:Message):
  if message.from_user.id:
    sticker_loading = await client.send_sticker(message.chat.id, "CAACAgIAAxkBAAENIfZnOBR8ghBQF2ksQk-vFX3XVXeDMwACSQIAAladvQoqlwydCFMhDjYE")
    CHAT_USER_ACTIONS(message).deleteChat(message.from_user.id)
    await sleep(2)
    await sticker_loading.delete()
    await message.reply_text("[✅] LA MEMORIA DE CUVO ESTÁ LIMPIA.")
  else:
    await message.reply_text(f"Oye 😡 no permitiré que me borres la memoria, me lo ordenó mi creador.")