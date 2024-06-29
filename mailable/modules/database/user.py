from mailable.modules.database import database
from mailable.modules.user import USER

collection = database["usercache"]

def get_user(userID):
  if isinstance(userID, str) and userID.startswith("@"):
    result = collection.find_one({"username": userID[1:]})
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
  
def update_user(msg):
  user = {}
  user['firstname'] = msg.from_user.first_name
  user['lastname'] = msg.from_user.last_name
  user['username'] = msg.from_user.username
  user['lastseen'] = msg.date

  filter = { 'userid': msg.from_user.id }
  newvalues = { "$set": user }
  
  collection.update_one(filter, newvalues)

def find_user(mail):
  mail = mail.lower()
  cursor = collection.find({'mails': mail })

  userID = -1001337409011

  for i in cursor:
    userID = i['userid']

  return userID

