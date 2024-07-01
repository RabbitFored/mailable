from pyrogram import filters
from mailable import bot, utils
from mailable.modules import database as db
from mailable.modules.filters import sudo_filter

  

@bot.on_message(filters.command(["whois"]) & sudo_filter )
async def whois(client, message):
  args = message.text.split(" ")
  user = db.find_user(args[1])

  await message.reply_text(f'Mail {args[1]} belongs to `{user.ID}`')

@bot.on_message(filters.command(["user"])  & sudo_filter )
async def user(client, message):
  userID = utils.get_user(message)
  user = db.get_user(userID)
  
  if not user:
    await message.reply_text("**No user found!**")
    return
  text = f'''
**User:** {user.firstname} {user.lastname if user.lastname else "" }
**Username:** @{user.username}
**DC:** `{user.dc}`
**Type:** `{user.type}`
**Mails:** `{user.mails}`
**First seen:** `{user.firstseen}`
**Last seen:** `{user.lastseen}`
**Banned** `{user.is_banned}`
'''

  await message.reply_text(text)

@bot.on_message(filters.command(["ban"])  & sudo_filter )
async def ban(client, message):
  userID = utils.get_user(message)
  if not userID:
    await message.reply_text("**No user found!**")
    return
  db.ban_user(userID)
  await message.reply_text(f"Banned {userID}")

@bot.on_message(filters.command(["unban"])  & sudo_filter )
async def unban(client, message):
  userID = utils.get_user(message)
  if not userID:
    await message.reply_text("**No user found!**")
    return
  db.unban_user(userID)
  await message.reply_text(f"Unbanned {userID}")
