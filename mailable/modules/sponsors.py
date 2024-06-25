from pyrogram import filters
from mailable import bot
from mailable.strings import SPONSORS_TEXT

@bot.on_message(filters.command(["sponsors"]))
async def sponsors(client, message):
  text = SPONSORS_TEXT
  await message.reply_text(text, disable_web_page_preview=True)

