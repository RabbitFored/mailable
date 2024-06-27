from mailable import bot
from mailable.modules import database as db
import string
from mailable.strings import PRIVACY_POLICY, WELCOME_TEXT
import secrets
from mailable.constants import sudoers
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from mailable.modules import mail
from mailable.__main__ import get_help


@bot.on_callback_query()
async def cb_handler(client, query):
  if query.data.startswith('new'):

    await query.answer()
    await query.message.delete()
    
    alphabet = string.ascii_letters + string.digits
    user = ''.join(secrets.choice(alphabet) for i in range(8))
    mails = db.mails(query.message.chat.id)

    limits = db.get_limits(query.message.chat.id)
    member_mail_limit = limits["limits"]["mails"]["member"]
    non_member_mail_limit = limits["limits"]["mails"]["non_member"]

    if query.message.chat.id in sudoers:
      cb = query.data.split("_")
      domain = cb[1]
      mailID = user + "@" + domain
      text = db.add_mail(query.message.chat.id, mailID)
      await query.message.reply_text(
        f"Mail Created successfully.\nYour mail id : {mailID}\nNow You can access your mails here."
      )
      return
    if len(mails) < 2:
      cb = query.data.split("_")
      domain = cb[1]
      mailID = user + "@" + domain
      text = db.add_mail(query.message.chat.id, mailID)
      await bot.send_message(
        query.message.chat.id,
        f"Mail Created successfully.\nYour mail id : {mailID}\nNow You can access your mails here."
      )
    elif len(mails) > 1:
      if len(mails) < member_mail_limit:
        try:
          user_exist = await client.get_chat_member('theostrich',
                                                    query.message.chat.id)
          cb = query.data.split("_")
          domain = cb[1]

          mailID = user + "@" + domain
          text = db.add_mail(query.message.chat.id, mailID)
          await bot.send_message(
            query.message.chat.id,
            f"Mail Created successfully.\nYour mail id : {mailID}\nNow You can access your mails here."
          )

        except UserNotParticipant:
          await query.message.reply_text(
            text=
            f"**Due to limited resource, making mails more than {non_member_mail_limit} requires channel membership.**",
            reply_markup=InlineKeyboardMarkup([[
              InlineKeyboardButton(text="Join theostrich",
                                   url=f"https://t.me/theostrich")
            ]]))
      else:
        await bot.send_message(
          query.message.chat.id,
          f"**Your plan includes reserving {member_mail_limit} mails only.\nSwitch to premium plan or delete any mail using /delete to make more mails.**"
        )
        
  elif query.data == 'close':
    await query.message.delete()
  elif query.data == 'del':
    id = query.message.reply_markup.inline_keyboard[0][0].url.split("/")[-1]
    print(id)

    await client.send_message(
      query.message.chat.id,
      "**Are you sure?**",
      reply_markup=InlineKeyboardMarkup([[
        InlineKeyboardButton("YES", callback_data=f"yes_{id}"),
      ], [
        InlineKeyboardButton("NO", callback_data=f"nope"),
      ]]))
  elif query.data.startswith("yes"):
    key = query.data.split("_")[1]

    requests.get(f"https://paste.theostrich.eu.org/api/delete/aio/{key}")
    await query.answer("Mail deleted successfully")
    await query.message.delete()

  elif query.data == "nope":
    await query.message.delete()
  elif query.data.startswith('delete'):
    await query.answer()
    mail = query.data[7:]
    db.delete_mail(query.message.chat.id, mail)
    await query.message.edit_text("**Mail deleted successfully**")
  elif query.data.startswith('send'):
    await query.answer()
    sender = query.data[5:]
    await mail.send_mail(sender, client, query.message)

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
  elif query.data.startswith("transfer"):
    mailID = query.data.split("_")[1]
    await mail.transfer_mail(client, query.message, mailID)
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
            InlineKeyboardButton("Transfer", callback_data=f"transfer_{mailID}") ],
         [   InlineKeyboardButton("Delete", callback_data=f"delete_{mailID}")
        ]
    ]
    await query.message.edit(text,reply_markup=InlineKeyboardMarkup(keyboard))

