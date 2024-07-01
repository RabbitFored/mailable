from mailable import bot
from mailable.modules import database as db
from mailable.strings import PRIVACY_POLICY, WELCOME_TEXT
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from mailable.modules.mail import *
from mailable.__main__ import get_help
from mailable import utils

@bot.on_callback_query()
async def cb_handler(client, query):

  if query.data.startswith('new'):

    await query.answer()
    await query.message.delete()
    
    user = db.get_user(query.message.chat.id)
    limits = user.get_limits()
    max_mails = limits["max_mails"]
    
    if len(user.mails) >= max_mails:
      await bot.send_message(
        query.message.chat.id,
        f"**Your plan includes reserving {max_mails} mails only.\nSwitch to premium plan to make more mails.**")
      return
      
    
    domain = query.data.split("_")[1]
    mailID =  utils.gen_rand_string(8) + "@" + domain

    db.add_mail(query.message.chat.id, mailID)
    await query.message.reply_text(
            f"Mail Created successfully.\nYour mail id : {mailID}\nNow You can access your mails here."
          )

  elif query.data.startswith('dl'):
    await query.answer()
    mailID = query.data.split("_")[1]
    db.delete_mail(query.message.chat.id, mailID)
    await query.message.edit_text("**Mail deleted successfully**")
    
 # elif query.data.startswith('send'):
 #   await query.answer()
 #   sender = query.data[5:]
 #   await mail.send_mail(sender, client, query.message)

  elif query.data == "getHelp":
    await query.answer()
    await get_help(client, query.message.reply_to_message)
    await query.message.delete()

  elif query.data == "back_to_start":
    await query.answer()
    
    text = WELCOME_TEXT.format(user=query.message.from_user.mention)
    keyboard = [
        [
            InlineKeyboardButton("HELP", callback_data="getHelp"),
            InlineKeyboardButton("Privacy Policy", callback_data="prp"),
        ]
    ]
    await query.message.edit(
      text,
      disable_web_page_preview=True,
      reply_markup=InlineKeyboardMarkup(keyboard))

  elif query.data == "prp":
    await query.answer()
    text = PRIVACY_POLICY
    keyboard = [
        [
          InlineKeyboardButton("Back", callback_data="back_to_start")
        ]
    ]
    
    await query.message.edit(
      text,
      reply_markup=InlineKeyboardMarkup(keyboard))

  elif query.data.startswith('block'):
    await query.answer()
    option = query.data[6:]
    await mail.block(client, query.message, option)
    
  elif query.data.startswith("tr"):
    mailID = query.data.split("_")[1]
    await transfer_mail(client, query.message, mailID)
    
  elif query.data.startswith('unblock'):
    await query.answer()
    option = query.data[8:]
    await mail.unblock(client, query.message, option)
    
  elif query.data.startswith('info'):
    mailID = query.data[5:]
    text = f'''**
Mail  : {mailID}
Owner : {query.message.reply_to_message.from_user.mention()}
**'''
    keyboard = [
        [
            InlineKeyboardButton("Transfer", callback_data=f"tr_{mailID}") ],
         [   InlineKeyboardButton("Delete", callback_data=f"dl_{mailID}")
        ]
    ]
    await query.message.edit(text,reply_markup=InlineKeyboardMarkup(keyboard))

