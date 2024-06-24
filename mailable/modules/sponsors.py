from pyrogram import filters
from mailable import bot

@bot.on_message(filters.command(["sponsors"]))
async def sponsors(client, message):
  text = '''
**Our sponsor list:**
  >> [Ž€ ₣ΔŁĆØŇ](https://t.me/Ze_Falcon)

__Help us by sponsoring a domain or [buy us a cup of tea](https://ko-fi.com/rabbitfored/) and become one of the premium members.__
'''
  await message.reply_text(text, disable_web_page_preview=True)

