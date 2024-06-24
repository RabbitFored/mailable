from pyrogram import filters
from mailable import bot


@bot.on_message(filters.command(["domains"]))
async def list_domains(client, message):
  text = '''
**List of available domains:**    

  - mail.bruva.co
'''
  await message.reply_text(text)

