from blind.src.utils.utilities import printTest
import json
from .objects import Rutina

class Agenda:
  def __init__(self, PATH_FILE:str="agenda.json"):
    self.PATH_FILE = PATH_FILE
    self.data = self.loadData()
  
  def loadData(self):
    try:
      with open(self.PATH_FILE, "r") as f:
        data = json.load(f)
      return data
    except FileNotFoundError:
      TEMPLATE = {
        "rutinas": {},
      }
      return TEMPLATE
    
  def saveData(self):
    with open(self.PATH_FILE, "w") as f:
      json.dump(self.data, f, indent=4)

  def createProfile(self, id_chat:int):
    if not self.data.get("rutinas", None):
      self.data["rutinas"] = {}
    if not self.data["rutinas"].get(str(id_chat), None):
      self.data["rutinas"][str(id_chat)] = {}

    self.saveData()

  # -- OPERACION DE LAS RUTINAS
  def createRutinas(self, rutina:Rutina):
    self.createProfile(rutina.id_chat)
    printTest(rutina.__dict__(), lista=type(rutina.dias))
    self.data["rutinas"][str(rutina.id_chat)][str(rutina.id_rutina)] = rutina.__dict__()
    self.saveData()
    return {"rutina": rutina.__dict__()}
  
  def loadRutinas(self, ID_CHAT:int):
    self.createProfile(ID_CHAT)

    RUTINAS = self.data.get("rutinas", {}).get(str(ID_CHAT), {})
    return {"rutinas": RUTINAS}  
  
  def deleteRutinas(self, ID_CHAT:int, ID_RUTINA:int):
    self.createProfile(ID_CHAT)

    RUTINAS = self.data.get("rutinas", {}).get(str(ID_CHAT), {})
    if RUTINAS.get(str(ID_RUTINA), None):
      del RUTINAS[str(ID_RUTINA)]
      self.saveData()
      return True
    return False
  
  def modifyRutinas(self, ID_CHAT:int, ID_RUTINA:int, rutina:Rutina):
    self.createProfile(ID_CHAT)

    RUTINAS = self.data.get("rutinas", {}).get(str(ID_CHAT), {})
    if RUTINAS.get(str(ID_RUTINA), None):
      RUTINAS[str(ID_RUTINA)] = rutina.__dict__()
      self.saveData()
      return True
    return False
  
  def getRutina(self, ID_CHAT:int, ID_RUTINA:int) -> Rutina:
    self.createProfile(ID_CHAT)

    RUTINAS = self.data.get("rutinas", {}).get(str(ID_CHAT), {})
    if RUTINAS.get(str(ID_RUTINA), None):
      return RUTINAS[str(ID_RUTINA)]
    return None
  
  def loadAllRutinas(self):
    return self.data.get("rutinas", {})