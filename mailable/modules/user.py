from pyrogram import filters
from mailable import bot
from mailable.modules import database as db


@bot.on_message(filters.command(["me"]))
async def user_info(client, message):
  limits = db.get_limits(message.from_user.id)
  plan = limits["type"]
  member_mail_limit = limits["limits"]["mails"]["member"]
  non_member_mail_limit = limits["limits"]["mails"]["non_member"]
  at_once = limits["limits"]["send"]["at_once"]
  text = f'''```User : {message.from_user.mention}
Plan : {plan}
Limits:
  • Mails:
       - member  : {member_mail_limit}
       - !member : {non_member_mail_limit}
  • Send : 
       - at_once : {at_once}
```
   '''
  await message.reply_text(text)

@bot.on_message(filters.command(["blocks"]))
async def blocks(client, message):
  blocks = db.get_blocked(message.chat.id)
  domains = "- **Domains:**\n"
  mails = "- **Mails:**\n"
  regex = "- **Regex:**\n"

  for i in blocks["domains"]:
    domains = domains + f"     - {i}\n"
  for i in blocks["mails"]:
    mails = mails + f"     - {i}\n"
  for i in blocks["regex"]:
    regex = regex + f"     - {i}\n"

  if len(blocks['domains']) == 0:
    domains = domains + "     - None"
  if len(blocks['mails']) == 0:
    mails = mails + "     - None"
  if len(blocks['regex']) == 0:
    regex = regex + "     - None"

  text = f'''
**Your blocklist:**

{domains}
{mails}
{regex}
__Use /unblock to stop blocking mails here.__
'''
  await message.reply_text(text, disable_web_page_preview=True)

