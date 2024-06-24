from mailable.modules.database import database

collection = database["usercache"]

def user_exist(chatid,chattype):
  if chattype == 'group' or chattype == "supergroup":
      collection = database["groupcache"]

  result = collection.find_one({'userid': chatid})

  try:
      result['userid']
      userexist = True

  except:
      userexist = False

  return userexist

def is_premium(user):
  result = collection.find_one({'userid': user})
  plan = result["plan"]["type"]
  if plan == "premium":
     return True
  else:
    return False

def user_info(userid):
  if userid.startswith("@"):
    cursor = collection.find({"username":userid[1:]})
    for user in cursor:
     return user

  cursor = collection.find({"userid":int(userid)})
  for user in cursor:
     return user

def find_user(mail):
  mail = mail.lower()
  cursor = collection.find({'mails': mail })

  user = -1001337409011

  for i in cursor:
    user = i['userid']

  return user

def get_limits(user):
  filter = { 'userid': user }
  if isinstance(user, str):
   if user.startswith("@"):
     filter = {"username":user[1:]}
  cursor = collection.find(filter)
  for i in cursor:
    plan = i["plan"]
    return plan

def get_user_domains(user):
  result = collection.find_one({'userid': user})
  if result.get("user_domains"):
    return result["user_domains"]
  else:
    return []


def get_blocked(user):
  cursor = collection.find({"userid":user})
  for i in cursor:
    blocked = i["blocked"]
    return blocked