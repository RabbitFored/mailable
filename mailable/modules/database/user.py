from mailable.modules.database import database
from mailable.modules.user import USER

collection = database["usercache"]

def get_user(userID):
  if isinstance(userID, str) and userID.startswith("@"):
    result = collection.find_one({"username": userID[1:]})
  elif isinstance(userID, str) and userID.isdigit():
    result = collection.find_one({'userid': int(userID)})
  else:
    result = collection.find_one({'userid': userID})
  if result:
    user = USER(result)
    return user
  else:
    return None

def add_user(msg):
  userID = msg.from_user.id
  now = msg.date
  username = msg.from_user.username
  firstname = msg.from_user.first_name
  lastname = msg.from_user.last_name
  dc = msg.from_user.dc_id

  user = {}
  user['userid'] = userID
  user['username'] = username
  user['firstname'] = firstname
  user['lastname'] = lastname
  user['is-banned'] = False
  user['dc'] = dc
  user['type'] = "free"

#mailable  <<start>>
  user['blocks'] = {
    "domains": [],
    "mails": [],
    "regex": []
  }
  user['mails'] = []
#mailable  <<end>>
  
  user['firstseen'] = now
  user['lastseen'] = now

  
  collection.insert_one(user)
  return True
  
def update_user(userID,values):
  if isinstance(userID, str) and userID.startswith("@"):
    filter = {"username": userID[1:]}
  elif isinstance(userID, str) and userID.isdigit():
    filter = {'userid': int(userID)}
  else:
    filter = {'userid': userID}
  newvalues = { "$set": values }
  
  collection.update_one(filter, newvalues)

def find_user(mailID):
  mailID = mailID.lower()
  result = collection.find_one({'mails': mailID })
  if result:
    user = USER(result)
    return user
  else:
    return None


def refresh_user(msg):
    user = {}
    user['firstname'] = msg.from_user.first_name
    user['lastname'] = msg.from_user.last_name
    user['username'] = msg.from_user.username
    user['lastseen'] = msg.date

    filter = { 'userid': msg.from_user.id }
    newvalues = { "$set": user }

    update_user(msg.from_user.id , user)
  
def ban_user(userID):
  user = {
    "is-banned": True
  }

  update_user(userID , user)

def unban_user(userID):
  user = {
    "is-banned": False
  }
  update_user(userID , user)
