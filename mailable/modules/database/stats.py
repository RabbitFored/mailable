from mailable.modules.database import database

collection = database["statial"]

def statial(what,how):
  collection.update_one( {}, {"$inc": { what : how }} )
  return "ok"

def get_statial():
  cursor = collection.find()
  for i in cursor:
    value = i
  return value
