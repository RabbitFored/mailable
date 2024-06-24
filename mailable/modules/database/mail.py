from mailable.modules.database import database, stats

collection = database["usercache"]

def add_mail(user,mail):
  mail = mail.lower()
  cursor = collection.find({'mails': mail })

  if len(list(cursor)) != 0:
    return "exist"


  filter = { 'userid': user }
  if isinstance(user, str):
   if user.startswith("@"):
     filter = {"username":user[1:]}
  newvalues = { "$addToSet": { 'mails': mail }}
  collection.update_one(filter, newvalues)
  stats.statial("mails",1)


def mails(user):
  filter = { 'userid': user }
  if isinstance(user, str):
   if user.startswith("@"):
     filter = {"username":user[1:]}
  cursor = collection.find(filter)
  mails = []
  for i in cursor:
    for mail in i["mails"]:
      mails.append(mail)

  return mails

def block(user,option,value):
  collection = database["usercache"]
  filter = { 'userid': user }
  newvalues = { "$addToSet": {f"blocked.{option}" :{"$each": value}}}
  collection.update_one(filter, newvalues)

def unblock(user,option,values):
  collection=database["usercache"]
  filter = {"userid":user}
  for value in values:
    values = { "$pull": { f"blocked.{option}" : value}}
    collection.update_one(filter, values)

def delete_mail(user,mail):
  mail = mail.lower()
  collection=database["usercache"]
  filter = {"userid":user}
  values = { "$pull": { "mails":  mail}}
  collection.update_one(filter, values)
  stats.statial("mails",-1)
  return mails
