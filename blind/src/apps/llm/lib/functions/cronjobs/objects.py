import random
from proto.marshal.collections.repeated import RepeatedComposite

class Rutina:
  def __init__(self, dias:RepeatedComposite, hora:str, message:str, id_chat:str, utc:int|str, id_rutina:int=0):
    self.dias = list(dias)
    self.hora = hora
    self.message = message
    self.id_chat = id_chat
    self.id_rutina = random.randint(0, 100) if id_rutina == 0 else id_rutina
    self.utc = utc

  def __dict__(self):
      return {
          "dias": self.dias,
          "hora": self.hora,
          "message": self.message,
          "id_chat": self.id_chat,
          "id_rutina": self.id_rutina,
          "utc": self.utc
      }