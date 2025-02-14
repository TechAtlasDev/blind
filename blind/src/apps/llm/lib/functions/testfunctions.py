from pyrogram import Client
from pyrogram.types.messages_and_media.message import Message

def sumar(valor1:int, valor2:int, **kwargs):
  return {"resultado": valor1+valor2}