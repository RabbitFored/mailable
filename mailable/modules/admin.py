from pyrogram import filters
from mailable import bot
from mailable.modules import database as db
from mailable.modules.filters import sudo_filter

@bot.on_message(filters.command(["whois"]) & sudo_filter )
async def whois(client, message):
  split = message.text.split(" ")
  user = db.find_user(split[1])

  await message.reply_text(f'''Mail {split[1]} belongs to {user}''')

@bot.on_message(filters.command(["user"])  & sudo_filter )
async def user(client, message):
  split = message.text.split(" ")
  user = None

  if len(split) > 1:
    id = split[1]
    user = db.get_user(id)
  if message.reply_to_message:
    if message.reply_to_message.forward_from:
      user = db.get_user(str(message.reply_to_message.forward_from.id))
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
