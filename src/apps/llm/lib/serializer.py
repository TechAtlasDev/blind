import json

class SerializerResponse:

  def __init__(self, data:str):
    self.object = json.loads(data)

  def sendObject(self) -> dict:
    return self.object
  
  def keys(self) -> list:
    return list(self.object.keys())