import string
import secrets

def gen_rand_string(len):
  alphabet = string.ascii_letters + string.digits
  return ''.join(secrets.choice(alphabet) for i in range(len))

def get_user(message):
  userID = None
  args = message.text.split(" ")
  if len(args) > 1:
    userID = args[1]
    return userID
  elif message.reply_to_message:
    if message.reply_to_message.forward_from:
      userID = message.reply_to_message.forward_from.id
      return userID
  else:
    return None