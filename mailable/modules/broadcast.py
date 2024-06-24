from mailable import bot
from pymongo import MongoClient
from config import mongouri
from pyrogram import filters
import time

myclient = MongoClient(mongouri)
db = myclient['mailis']
collection = db["usercache"]

@bot.on_message(filters.command(["broadcast"]))
async def broadcast(client, message):  
  chat_id = message.chat.id
  print("=======", chat_id, "========")
  botOwnerID = [1775541139, 1520625615, 1809735866]
  if chat_id in botOwnerID:
    await message.reply_text("Broadcasting...")
    chat = (collection.find({}, {'userid': 1, '_id': 0}))
    chats = [sub['userid'] for sub in chat]
    
    failed = 0
    x = 0
    for chat in chats:
      try:
        await message.reply_to_message.forward(chat)
        print(f"broadcasted to {x} users")
        x += 1
        time.sleep(2)
      except:
        failed += 1
        print("Couldn't send broadcast to %s, group name %s", chat)
    await message.reply_text(
      "Broadcast complete. {} users failed to receive the message, probably due to being kicked."
      .format(failed))
  else:
    await client.send_message(
      1520625615, f"Someone tried to access broadcast command,{chat_id}")
