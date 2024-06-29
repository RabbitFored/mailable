from pyrogram import filters
from mailable import bot, app
from mailable.modules import database as db
from pyrogram.enums import MessageEntityType
from mailable.constants import domains, sudoers, reserved_keyword
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from tldextract import extract
import re
from pyromod.helpers import ikb
from mailable import CONFIG
import requests 
import os
from quart import request, Response, send_file
import json
import mailparser

apikey = CONFIG.apikey
baseURL = CONFIG.baseURL

async def no_mails(message):
  text = "**You don't own any mail.\nUse /generate to get a new mail.**"
  await message.reply_text(text,quote=True)


@bot.on_message(filters.command(["delete"]))
async def delete(client, message):
  user =  db.get_user(message.from_user.id)
  mailIDs = user.mails

  if len(mailIDs) == 0:
      await no_mails(message)
      return

  text = "**Select a mail:**"
  keyboard = []
  for mailID in mailIDs:
      keyboard.append([InlineKeyboardButton(mailID, f"del_{mailID}")])

  await message.reply_text(
      text, reply_markup=InlineKeyboardMarkup(keyboard), quote=True
  )


@bot.on_message(filters.command(["mails"]))
async def mails(client, message):
  user =  db.get_user(message.from_user.id)
  mailIDs = user.mails

  if len(mailIDs) == 0:
      await no_mails(message)
      return

  text = "**Select a mail:**"
  keyboard = []
  for mailID in mailIDs:
      keyboard.append([InlineKeyboardButton(mailID, f"info_{mailID}")])

  await message.reply_text(
      text, reply_markup=InlineKeyboardMarkup(keyboard), quote=True
  )


@bot.on_message(filters.command(["transfer"]))
async def transfer(client, message):
  user =  db.get_user(message.from_user.id)
  mailIDs = user.mails

  if len(mailIDs) == 0:
      await no_mails(message)
      return

  text = "**Select a mail:**"
  keyboard = []
  for mailID in mailIDs:
      keyboard.append([InlineKeyboardButton(mailID, f"tr_{mailID}")])

  await message.reply_text(
      text, reply_markup=InlineKeyboardMarkup(keyboard), quote=True
  )



async def transfer_mail(client, message, mail):
  recipient = await message.chat.ask("**Please enter new owners username**")
  args = recipient.text.split(" ")
  
  if not args[0].startswith("@"):
    await client.send_message(
      message.chat.id,
      "**Provide a valid Username. Use /transfer to restart this process**")
    return
  try:
    await client.send_message(
      args[0],
      f"**Incoming mail transfer request for {mail} by {message.reply_to_message.from_user.mention()}**"
    )
  except:
    await message.reply_text(
      f"**Cannot transfer {mail} to {args[0]}.\nBe sure that the user started me.**"
    )
    return

  user = db.get_user(args[0])

  limits = user.get_limits()
  max_mails = limits["max_mails"]

  if len(user.mails) >= max_mails:
    await message.reply_text(
      f"**Cannot transfer {mail} to {args[0]}.\nThis user had exhausted free mail limits.**"
    )
    return

  db.delete_mail(message.chat.id, mail)
  db.add_mail(args[0], mail)

  await client.send_message(
    args[0], f'''
**New mail transferred to your account.

`Mail `: {mail}
`Transferred by :` {message.reply_to_message.from_user.mention()}

Check your mails using /mails command.**''')
  await message.reply_text(
    f"**Successfully transferred {mail} to {recipient.text}")




@bot.on_message(filters.command(["generate"]))
async def generate(client, message):
  buttons = []
  domains = CONFIG.settings["domains"]
  
#  user = db.get_user(message.chat.id)
  
  
#  if db.is_premium(message.chat.id):
#    user_domains = db.get_user_domains(message.chat.id)
#    all_domains = domains + user_domains
#  else:
#    all_domains = domains

  for domain in domains:
    buttons.append([InlineKeyboardButton(domain, f"new_{domain}")])

  await message.reply_text(text="**Select a domain:**",
                           disable_web_page_preview=True,
                           reply_markup=InlineKeyboardMarkup(buttons),
                           quote=True)
  

@bot.on_message(filters.command(["set"]))
async def set_mail(client, message):
  mailID = None
  for entity in message.entities:
    if entity.type == MessageEntityType.EMAIL:
      o = entity.offset
      l = entity.length
      mailID = message.text[o:o + l]
  if mailID == None:
    await message.reply_text(text="**Provide a valid mail ID.**")
    return

  domain = mailID.split("@")

  if domain[0].lower() in reserved_keyword:
    await bot.send_message(message.chat.id,
                               f"**Sorry this mail ID is unavailable**")
    return
  user = db.get_user(message.chat.id)

  limits = user.get_limits()
  max_mails = limits["max_mails"]


 # if db.is_premium(message.chat.id):
 #   user_domains = db.get_user_domains(message.chat.id)
 #   print(user_domains)
  #  all_domains = domains + user_domains
 # else:
 #   all_domains = domains
  
  if domain[1].lower() not in domains:
    await bot.send_message(
      message.chat.id,
      f"**The domain {domain[1]} is not maintained by us.\nUse /domains to check list of available domains.\n\nIf you are the owner of {domain[1]} and interested to use it in this bot, contact us at @ostrichdiscussion.**"
    )
    return
  if len(user.mails) >= max_mails:
    await bot.send_message(
      message.chat.id,
      f"**Your plan includes reserving {max_mails} mails only.\nSwitch to premium plan to make more mails.**")
    return
  text = db.add_mail(message.chat.id, mailID)
  if text == "exist":
        await bot.send_message(message.chat.id,
                                   f"Sorry this mail ID is unavailable")
        return
  await message.reply_text(
          f"Mail Created successfully.\nYour mail id : {mailID}\nNow You can access your mails here."
        )

@bot.on_message(filters.command(["block"]))
async def block_mail(client, message):

  await message.reply_text(
    "**Select an option:**",
    reply_markup=InlineKeyboardMarkup([[
      InlineKeyboardButton("mail", callback_data="block_mails"),
      InlineKeyboardButton("domain", callback_data="block_domains"),
    ], [InlineKeyboardButton("regex", callback_data="block_regex")]]),
    disable_web_page_preview=True)




@bot.on_message(filters.command(["unblock"]))
async def unblock_mail(client, message):

  await message.reply_text(
    "**Select an option:**",
    reply_markup=InlineKeyboardMarkup([[
      InlineKeyboardButton("mail", callback_data="unblock_mails"),
      InlineKeyboardButton("domain", callback_data="unblock_domains"),
    ], [InlineKeyboardButton("regex", callback_data="unblock_regex")]]),
    disable_web_page_preview=True)




async def unblock(client, message, option):

  trigger = []
  if option == "mails":
    value = await message.chat.ask(
      "**Provide a mail to unblock:\nEx:** ```ostrich@notaspammer.com```")
    for entity in value.text.entities:
      if entity.type == MessageEntityType.EMAIL:
        o = entity.offset
        l = entity.length
        trigger.append(value.text[o:o + l])
  if option == "domains":
    value = await message.chat.ask(
      "**Provide a domain to unblock:\nEx:** ```notaspammer.com```")
    for entity in value.text.entities:
      if entity.type == MessageEntityType.URL:
        o = entity.offset
        l = entity.length
        url = value.text[o:o + l]
        tsd, td, tsu = extract(url)
        domain = td + '.' + tsu
        if tsd:
          domain = tsd + '.' + td + '.' + tsu
        trigger.append(domain)
  if option == "regex":
    value = await message.chat.ask(
      "**Provide a regex to unblock its matches:\nEx:** ```(.*)@notaspammer.com```"
    )
    pattern = value.text
    try:
      re.compile(pattern)
      trigger.append(pattern)
    except re.error:
      print(f"invalid regex - {message.from_user.first_name}")

  if len(trigger) == 0:
    await message.reply_text(
      f"**No valid {option} provided.\nUse /unblock to restart this process**")
    return

  db.unblock(message.chat.id, option, trigger)
  await message.reply_text(f"**Unblocked successfully**")



'''

async def send_mail(sender, client, message):
  prrm = db.is_premium(message.chat.id)
  domain = sender.split("@")[1]
  if db.is_premium(message.chat.id):
    user_domains = db.get_user_domains(message.chat.id)
    print(user_domains)
    all_domains = domains + user_domains
  else:
    all_domains = domains
  if domain.lower() not in all_domains:

    await bot.send_message(
      message.chat.id,
      f"**The domain {domain} is not maintained by us.\nUse /domains to check list of available domains.\n\nIf you are the owner of {domain} and interested to use it in this bot, contact us at @ostrichdiscussion.**"
    )
    return
  if domain.lower() in db.get_user_domains(message.chat.id):
    await bot.send_message(
      message.chat.id,
      "Sending mails from custom domains is not included in your plan.\nPlease contact @ostrichdiscussion to upgrade your plan."
    )
    return
  to = await message.chat.ask('**Send me recipient mail**')

  mail = []
  for entity in to.text.entities:
    if entity.type == MessageEntityType.EMAIL:
      o = entity.offset
      l = entity.length
      mail.append(to.text[o:o + l])

  if len(mail) == 0:
    await bot.send_message(
      message.chat.id,
      f"**Please provide a valid mail./nUse /send to redo this task.**")
    return
  limits = db.get_limits(message.chat.id)
  at_once = limits["limits"]["send"]["at_once"]
  if len(mail) > at_once:
    await bot.send_message(
      message.chat.id,
      f"**You cannot send mail to more than {at_once} users at once. Upgrade your account to remove limitations.**"
    )
    return

  subject = await message.chat.ask("Provide mail subject")
  body = await message.chat.ask("Send any text to send.")
  if prrm:
    keyboard = ikb([[('Add an attachment', 'atch')],
                    [('Send mail', 'noatch')]])

    attachment = await message.chat.ask("Mail ready to send",
                                        reply_markup=keyboard)
    #,listener_type=ListenerTypes.CALLBACK_QUERY

    if attachment.data == "noatch":
      files = []
    else:
      attachment = await message.chat.ask("Send me an attachment to send")
      try:
        download_location = await client.download_media(attachment)
        print(download_location)
        files = [("attachment", (download_location.split("/")[-1],
                                 open(download_location, "rb").read()))]
      except:
        files = []
  files = []
  api = f"https://api.mailgun.net/v3/{domain}/messages"
  token = apikey
  if domain in ["slayy.tv", "seemsgood.us"]:
    token = os.environ.get('token2', '')
  r = requests.post(api,
                    auth=("api", token),
                    data={
                      "from": sender,
                      "to": mail,
                      "subject": subject.text,
                      "text": body.text
                    },
                    files=files)

  print(r.text)
  await bot.send_message(message.chat.id,
                             "**Mail queued successfully.**",
                             reply_markup=InlineKeyboardMarkup([[
                               InlineKeyboardButton(
                                 "Get Help",
                                 url="https://telegram.dog/ostrichdiscussion"),
                             ]]))
  db.statial("sent", 1)


@bot.on_message(filters.command(["send"]))
async def send(client, message):
  user = message.chat.id
  mails = db.mails(user)

  if len(mails) != 0:
    buttons = []

    for mail in mails:
      buttons.append([InlineKeyboardButton(mail, f"send_{mail}")])
    await message.reply_text(text="**Select a mail:**",
                             reply_markup=InlineKeyboardMarkup(buttons))
  else:
    await message.reply_text(
      text="**You don't own any mail.\nUse /generate to get a new domain.**")

'''


async def block(client, message, option):
  trigger = []
  if option == "mails":
    value = await message.chat.ask(
      "**Provide a mail to block:\nEx:** ```ostrich@spammer.com```")
    for entity in value.text.entities:
      if entity.type == MessageEntityType.EMAIL:
        o = entity.offset
        l = entity.length
        trigger.append(value.text[o:o + l])

    text = f"**Blocked successfully.\nNow you won't receive mails from {trigger}**"

  if option == "domains":
    value = await message.chat.ask(
      "**Provide a domain to block:\nEx:** ```spammer.com```")
    for entity in value.text.entities:
      if entity.type == MessageEntityType.URL:
        o = entity.offset
        l = entity.length
        url = value.text[o:o + l]
        tsd, td, tsu = extract(url)
        domain = td + '.' + tsu
        if tsd:
          domain = tsd + '.' + td + '.' + tsu
        trigger.append(domain)
    text = f"**Blocked successfully.\nNow you won't receive mails from {trigger}**"

  if option == "regex":
    value = await message.chat.ask(
      "**Provide a regex to block its matches:\nEx:** ```(.*)@spammer.com```")
    pattern = value.text
    try:
      re.compile(pattern)
      trigger.append(pattern)
    except re.error:
      print(f"invalid regex - {message.from_user.first_name}")
    text = f"**Blocked successfully.\nNow you won't receive mails matching {trigger}**"

  if len(trigger) == 0:
    await message.reply_text(
      f"**No valid {option} provided.\nUse /block to restart this process**")
    return

  db.block(message.chat.id, option, trigger)
  await value.reply_text(text)
































'''
@app.route('/cust', methods=['POST'])
async def reciever():
  mailbytes = await request.get_data()
  mail = mailparser.parse_from_bytes(mailbytes)
  multipart_data = MultipartEncoder(
    fields={
      "data":json.dumps({
    "from" : mail.from_,
    "to" : mail.to,
    "cc" : mail.cc,
    "bcc" : mail.bcc,
    "subject" : mail.subject,
    "body" : mail.body,
    "text" : mail.text_plain,
    "html" : mail.text_html,
    "reply_to" : mail.reply_to,
    "message_id" : mail.message_id
    })}
  )
  requests.post(f"{CONFIG.baseURL}/secretmessages",data=multipart_data,headers={'Content-Type': multipart_data.content_type})
  return 'Hello, World!'
'''
@app.route('/cust', methods=['POST'])
async def secretmessages():
  mailbytes = await request.get_data()
  print(mailbytes)
  mail = mailparser.parse_from_bytes(mailbytes)
  
  data =  { 
    "from" : mail.from_,
    "to" : mail.to,
    "cc" : mail.cc,
    "bcc" : mail.bcc,
    "subject" : mail.subject,
    "body" : mail.body,
    "text" : mail.text_plain,
    "html" : mail.text_html,
    "reply_to" : mail.reply_to,
    "message_id" : mail.message_id
    }
  
  
 # data = json.loads((await request.form).get("data"))
  userID = db.find_user(data['to'][0][1])

  f = open("inbox.html", "w")
  f.write(str(data["html"][0]))
  f.close()

  text = f"\
**Sender     :** {data['from'][0][1]}\n\
**Recipient  :** {data['to'][0][1]}\n\
**Subject    :** {data['subject']}\n\
**Message    :** {str(data['text'][0][:200])}\n...\
"

  file = await bot.send_document(chat_id=userID, document="inbox.html")
  await file.reply(
    text=text,
    reply_markup=InlineKeyboardMarkup([[
      InlineKeyboardButton(
        "View mail",
        web_app=WebAppInfo(url=f"{baseURL}/inbox/{userID}/{file.id}")),
    ], [
      InlineKeyboardButton("OPEN", url=f"{baseURL}/inbox/{userID}/{file.id}"),
    ]]),quote = True)  
  os.remove("inbox.html")
  return Response(status=200)

'''
@app.route('/messages', methods=['POST'])
async def foo():
  token = (await request.form).get('token')
  timestamp = (await request.form).get('timestamp')
  signature = (await request.form).get('signature')

  mail = (await request.form).get('sender')
  domain = mail.split("@")[1]

  isMailgun = verify_mailgun(domain, token, timestamp, signature)
  print(isMailgun)
  if not isMailgun:
    print("UNKNOWN SENDER")
    return Response(status=403)

  sender = (await request.form).get('sender')
  print(sender)
  recipient = (await request.form).get('recipient')
  db.statial("received", 1)

  user = db.find_user(recipient)

  subject = (await request.form).get('subject', '@penkerBot')
  subject = subject[:55]

  body_html = (await request.form).get('body-html', '')
  body_plain = (await request.form).get('body-plain', '')
  stripped_text = (await request.form).get('stripped-text', '')
  if body_html:
    body = body_html[:65532]
  else:
    body = body_plain[:65532]

  attachment_count = (await request.form).get('attachment-count', 0)

  #for i in range(int(attachment_count)):
  #print(request.files)
  # request.files[f'attachment-1'].save('ff.jpg')
  #ostrich.send_document(user,attachment)

  blocked = db.get_blocked(user)
  default_blocks = db.defaults("blocked")

  reDomain = recipient.split("@")[1]

  b_mails = blocked["mails"]
  b_domains = blocked["domains"]
  b_regex = blocked["regex"]
  #  print(reDomain.lower() != "themails.ml" and reDomain.lower != "seemsgood.us" )
  if reDomain.lower() != "themails.ml" and reDomain.lower() != "seemsgood.us":
    # print("su")
    b_mails = blocked["mails"] + default_blocks["mails"]
    b_domains = blocked["domains"] + default_blocks["domains"]
    b_regex = blocked["regex"] + default_blocks["regex"]

  print(b_domains, b_mails, b_regex)

  if mail in b_mails:
    print(f"blocked mail - {mail}")
    if mail == "bounces@heroku.com" or mail == "noreply@heroku.com":
      await bot.send_message(
        user,
        "**Incoming mail from heroku.com.\n\nNote: You can receive mails from heroku only for mails which belongs to themails.ml**"
      )

    return Response(status=200)

  if domain in b_domains:
    print(f"blocked domain - {domain}")
    if domain == "heroku.com":
      await bot.send_message(
        user,
        "**Incoming mail from heroku.com.\n\nNote: You can receive mails from heroku only for mails which belongs to themails.ml**"
      )
    return Response(status=200)

  for exp in b_regex:
    regex = re.compile(exp)
    match = regex.search(mail)
    if match:
      print(f"blocked {mail} : matches regex {exp}")
      return Response(status=200)

  headers = {"Content-Type": "application/json"}
  data = {"Title": subject, "Author": "Penker", "Content": body}

  req = requests.post("https://paste.theostrich.eu.org/api/documents",
                      data=json.dumps(data),
                      headers=headers)
  res = json.loads(req.text)

  key = res['result']['key']
  #mail_content = strip_tags(body).strip()

  text = f"\
**Sender     :** {sender}\n\
**Recipient  :** {recipient}\n\
**Subject    :** {subject}\n\
**Content    :** [Raw](https://paste.theostrich.eu.org/{key})\n\n\
**Message    :** \n{stripped_text[:200]}...\
"

  if sender.startswith("bounce"):
    by = (await request.form).get("from")
    text = f"\
**Sender     :** {sender}\n\
**From       :** {by}\n\
**Recipient  :** {recipient}\n\
**Subject    :** {subject}\n\
**Content    :** [Raw](https://paste.theostrich.eu.org/{key})\n\n\
**Message    :** \n{stripped_text[:200]}...\
"

  try:
    if True:
      m = await bot.send_message(
        user,
        text,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([[
          InlineKeyboardButton("View mail",
                               url=f"https://inbox.seemsgood.us/{key}"),
        ], [
          InlineKeyboardButton("Delete", callback_data=f"del"),
        ]]))
      for i in range(int(attachment_count)):
        file = (await request.files)[f'attachment-{i+1}']
        path = f"user/{user}{file.filename}"
        await file.save(path)
        await bot.send_document(user, path, reply_to_message_id=m.id)
        os.remove(path)

  except:
    return Response(status=200)

  #ostrich.send_message(
  #   user,
  #   f'**Message:**\n\n{mail_content[:200]}...',
  #   disable_web_page_preview=True,
  #   reply_markup=InlineKeyboardMarkup([ [
  #      InlineKeyboardButton("Close", callback_data=f"close"),
  #   ]]))

  return Response(status=200)

'''