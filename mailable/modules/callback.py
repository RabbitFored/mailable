from mailable import bot
from mailable.modules import database as db
import string
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
      mail = user + "@" + domain
      text = db.add_mail(query.message.chat.id, mail)
      await query.message.reply_text(
        f"Mail Created successfully.\nYour mail id : {mail}\nNow You can access your mails here."
      )
      return
    if len(mails) < 2:
      cb = query.data.split("_")
      domain = cb[1]
      mail = user + "@" + domain
      text = db.add_mail(query.message.chat.id, mail)
      await bot.send_message(
        query.message.chat.id,
        f"Mail Created successfully.\nYour mail id : {mail}\nNow You can access your mails here."
      )
    elif len(mails) > 1:
      if len(mails) < member_mail_limit:
        try:
          user_exist = await client.get_chat_member('theostrich',
                                                    query.message.chat.id)
          cb = query.data.split("_")
          domain = cb[1]

          mail = user + "@" + domain
          text = db.add_mail(query.message.chat.id, mail)
          await bot.send_message(
            query.message.chat.id,
            f"Mail Created successfully.\nYour mail id : {mail}\nNow You can access your mails here."
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
    await query.message.edit(
      text=f"**Hello {query.message.from_user.mention} 👋 !\n\n"
      "I am mail bot. I can forward all your mails here.\n\nHit help to know more on using me.**",
      disable_web_page_preview=True,
      reply_markup=InlineKeyboardMarkup([[
        InlineKeyboardButton("HELP", callback_data="getHelp"),
        InlineKeyboardButton("Privacy Policy", callback_data="prp"),
      ]]))

  elif query.data == "prp":
    await query.answer()
    prp = '''
**Privacy Policy:**

We are committed to protecting and respecting your privacy.
It is our overriding policy to collect as little user information as possible when using the Service.

This Privacy Policy explains (i) what information we collect through your access and use of our Service, (ii) the use we make of such information

By using this Service, you agree to the terms outlined in this Privacy Policy.

**Data we collect and why we collect it:**

- **Account creation:**
     Data like your telegram username, user id, date of creation are collected at the time of account creation (starting the bot).
This information is necessary to provide the service and support.

- **Mail content:**
    All mail contents are stored temporarily to provide web view access to the users.

**Note:** _These mails will never be accessed by us (or) some others unless you share the access link. It is your sole responsibility to protect the access links shared by bot._

**Changes to our Privacy Policy**

We reserve the right to periodically review and change this Policy and will notify users who have enabled the notification preference about any change. Continued use of the Service will be deemed as acceptance of such changes.

**We may stop this service at any time without prior notice.**

        '''
    await query.message.edit(
      text=prp,
      reply_markup=InlineKeyboardMarkup(
        [[InlineKeyboardButton("Back", callback_data="back_to_start")]]))

  elif query.data.startswith('block'):
    await query.answer()
    option = query.data[6:]
    await mail.block(client, query.message, option)
  elif query.data.startswith("transfer"):
    mail = query.data.split("_")[1]
    await mail.transfer_mail(client, query.message, mail)
  elif query.data.startswith('unblock'):
    await query.answer()
    option = query.data[8:]
    await mail.unblock(client, query.message, option)
  elif query.data.startswith('info'):
    mail = query.data[5:]
    text = f'''**
Mail  : {mail}
Owner : {query.message.reply_to_message.from_user.mention()}
**'''
    await query.message.edit_text(text)

