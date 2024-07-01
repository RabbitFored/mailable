import json
from pyrogram import filters
from mailable import bot, CONFIG
from pyrogram.errors import UserNotParticipant
from mailable.modules import database as db
from functools import wraps

async def user_check(_, __, msg):
  json_object = json.loads(f"{msg}")
  instance = json_object["_"]

  if instance == "Message":
    userID = msg.chat.id
  elif instance == "CallbackQuery":
    userID = msg.message.chat.id
  elif instance == "InlineQuery":
    userID = msg.from_user.id
  else:
    print(instance)

  user = db.get_user(userID)
  
  if not user:
    db.add_user(msg)
  else:
    db.refresh_user(msg)
    if bool(user.is_banned):
      return True
  
  user_pass = False
  
  if bool(CONFIG.settings["force_sub"]):
    try:
      await bot.get_chat_member('theostrich', userID)
      user_pass = True
    except UserNotParticipant:
      user_pass = False
  else:
    user_pass = True

  if not user_pass:
    return True
    
  return False

async def sudoer_check(_, __, msg):
  user = msg.chat.id

  sudoers = CONFIG.get_sudoers()
  if user in sudoers:
    return True
  return False

user_filter = filters.create(user_check)
sudo_filter = filters.create(sudoer_check)