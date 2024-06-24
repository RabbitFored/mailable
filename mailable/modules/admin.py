from pyrogram import filters
from mailable import bot
from mailable.modules import database as db


@bot.on_message(filters.command(["whoo"]))
async def whoo(client, message):
  split = message.text.split(" ")
  user = db.find_user(split[1])

  await message.reply_text(f'''
Mail {split[1]} belongs to {user}
    ''')

@bot.on_message(filters.command(["user"]))
async def user(client, message):
  split = message.text.split(" ")
  user = None

  if len(split) > 1:
    id = split[1]
    user = db.user_info(id)
  if message.reply_to_message:
    if message.reply_to_message.forward_from:
      user = db.user_info(str(message.reply_to_message.forward_from.id))
  if not user:
    await message.reply_text("**No user found!**")
    return
  text = f'''
**User:** {user['firstname']}  {user['lastname']}
**Username:** @{user['username']}
**DC:** `{user['dc']}`
**Plan:** `{user['plan']['type']}`
**Mails:** `{user['mails']}`
**First seen:** `{user['firstseen']}`

'''

  await message.reply_text(text)
