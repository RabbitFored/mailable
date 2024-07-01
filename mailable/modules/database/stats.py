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

def get_users():
  collection = database["usercache"]
  user = (collection.find({}, {'userid': 1, '_id': 0}))
  users = [u['userid'] for u in user]
  return users