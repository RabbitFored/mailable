import importlib
from mailable.modules import ALL_MODULES
from mailable import bot, logger, app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from mailable import strings
from mailable.modules import database as db
from mailable import CONFIG
from mailable.modules.filters import user_filter

#load all modules
def install_modules():
    for module in ALL_MODULES:
        importlib.import_module("mailable.modules." + module)

#check users in banlist and forcesub
@bot.on_message(user_filter)
async def user_check(client, message):
    text = strings.FORCE_SUB_TEXT

    await message.reply_text(
        text,
        disable_web_page_preview=True,
        quote=True,
    )

@bot.on_message(filters.command(["start"]))
async def start(client, message):

    text = strings.WELCOME_TEXT.format(user=message.from_user.mention)
    keyboard = [
        [
            InlineKeyboardButton("HELP", callback_data="getHelp"),
            InlineKeyboardButton("Privacy Policy", callback_data="prp"),
        ]
    ]

    await message.reply_text(
        text,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(keyboard),
        quote=True,
    )
    

@bot.on_message(filters.command(["help"]))
async def get_help(client, message):
    text = strings.HELP_TEXT

    #extended help message for bot administrator
    chatID = message.chat.id
    sudoers = CONFIG.get_sudoers()

    if chatID in sudoers:
        text += strings.ADMIN_HELP_TEXT
        
    group_url =  CONFIG.settings["group_url"]
    
    keyboard = [
        [
            InlineKeyboardButton("Get Help", url=group_url),
        ],
    ]

    await message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        reply_to_message_id=message.id,
    )


@bot.on_message(filters.command(["about"]))
async def aboutTheBot(client, message):
    text = strings.ABOUT_TEXT
    
    channel_url = CONFIG.settings["channel_url"]
    group_url =  CONFIG.settings["group_url"]
    
    keyboard = [
        [
            InlineKeyboardButton("➰Channel", url=channel_url),
            InlineKeyboardButton("👥Support Group", url=group_url)
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await message.reply_text(
        text, reply_markup=reply_markup, disable_web_page_preview=True
    )


@bot.on_message(filters.command(["donate"]))
async def donate(client, message):
    text = strings.DONATE_TEXT
    
    channel_url = CONFIG.settings["channel_url"]
    donation_url =  CONFIG.settings["donation_url"]
    
    keyboard = [
        [
            InlineKeyboardButton("Contribute", url=channel_url),
            InlineKeyboardButton("Paypal Us", url=donation_url)
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await message.reply_text(text, reply_markup=reply_markup)



if __name__ == "__main__":
    install_modules()
    logger.info("Successfully loaded modules: " + str(ALL_MODULES))
    bot.start()
    app.run("0.0.0.0", CONFIG.port, loop=bot.loop, debug=True)
