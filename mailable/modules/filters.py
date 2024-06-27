import json
from pyrogram import filters
from mailable import bot, CONFIG
from pyrogram.errors import UserNotParticipant

async def user_check(_, __, m):
  print(m.id)
  json_object = json.loads(f"{m}")
  instance = json_object["_"]

  if instance == "Message":
    user = m.chat.id
  elif instance == "CallbackQuery":
    user = m.message.chat.id
  elif instance == "InlineQuery":
    user = m.from_user.id
  else:
    print(instance)
    
  user_pass = False
  if bool(CONFIG.settings["force_sub"]):
    try:
      await bot.get_chat_member('theostrich',user)
      user_pass = True
    except UserNotParticipant:
      user_pass = False
  else:
    user_pass = True

  if not user_pass:
    return True
    
  return False

async def sudoer_check(_, __, m):
  user = m.chat.id

  sudoers = CONFIG.get_sudoers()
  if user in sudoers:
    return True
  return False

user_filter = filters.create(user_check)
sudo_filter = filters.create(sudoer_check)
