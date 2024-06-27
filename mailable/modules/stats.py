from pyrogram import filters
from mailable import bot
from mailable.modules import database as db
from mailable import PROCESSES

@bot.on_message(filters.command(["stats"]))
async def stats(client, message):
  stat = db.get_statial()

  text = f'''
**Mailable Bot - STATS:**
- User : `{stat['users']}`
- Mails : `{stat['mails']}`
- Sent : `{stat['sent']}`
- Received : `{stat['received']}`

**Processes**:
- boradcast : `{PROCESSES.broadcast}`
'''
  await message.reply_text(text)