from mailable.modules.database import collection, stats

def is_mail_exist(mailID):
  cursor = list(collection.find({'mails': mailID}))
  if cursor:
    return True
  else:
    return False

def add_mail(userID,mailID):
  
  mailID = mailID.lower()
  if is_mail_exist(mailID):
    return "exist"

  if isinstance(userID, str) and userID.startswith("@"):
     filter = {"username":userID[1:]}
  else:
     filter = { 'userid': userID }
    
  newvalues = { "$addToSet": { 'mails': mailID }}
  collection.update_one(filter, newvalues)
  stats.statial("mails",1)
  
def delete_mail(userID,mailID):
  mailID = mailID.lower()
  filter = {"userid":userID}
  values = { "$pull": { "mails":  mailID}}
  collection.update_one(filter, values)
  stats.statial("mails",-1)
  return True

def block(user,option,value):
  filter = { 'userid': user }
  newvalues = { "$addToSet": {f"blocked.{option}" :{"$each": value}}}
  collection.update_one(filter, newvalues)

def unblock(user,option,values):
  filter = {"userid":user}
  for value in values:
    values = { "$pull": { f"blocked.{option}" : value}}
    collection.update_one(filter, values)

