from pyrogram import filters
from mailable import bot
from mailable import CONFIG


@bot.on_message(filters.command(["domains"]))
async def list_domains(client, message):
    domains = CONFIG["settings"]["domains"]
    if len(domains) == 0:
        await message.reply_text("No domains found.")
    else:
        text = """**List of available domains:**"""
        for domain in domains:
            text += f"\n- `{domain}`"
    await message.reply_text(text)
