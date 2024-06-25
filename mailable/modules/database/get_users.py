from mailable.modules.database import database

collection = database["usercache"]

def get_users():
  user = (collection.find({}, {'userid': 1, '_id': 0}))
  users = [u['userid'] for u in user]

  return users