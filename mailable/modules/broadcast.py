from mailable import bot, logger, CONFIG, PROCESSES
from pyrogram import filters
import time
from mailable.modules import database as db
from mailable.modules.filters import sudo_filter

@bot.on_message(filters.command(["broadcast"]) & sudo_filter)
async def broadcast(client, message):
        if PROCESSES.broadcast:
            await message.reply_text("Another broadcast is already in progress. Please try again later.")
            return
        broadcast_msg = message.reply_to_message
        if not broadcast_msg:
            await message.reply(
                "Please reply to a message to broadcast it.", quote=True
            )
            return
        users = db.get_users()
        await message.reply_text(f"Broadcasting to {len(users)}...")
        PROCESSES.broadcast = True
        failed = 0
        x = 0
        mode = CONFIG.settings["broadcast"]["mode"]
        if len(message.text.split(" ")) > 1:
            mode = message.text.split(" ")[1]
        for user in users:
            try:
                if mode == "copy":
                    await broadcast_msg.copy(user)
                else:
                    await broadcast_msg.forward(user)

                x += 1
                time.sleep(2)

            except:
                failed += 1
        text = f"Broadcast complete. {failed} users failed to receive the message, probably due to being kicked."
        await message.reply_text(text)
        logger.info(text)
        PROCESSES.broadcast = False
