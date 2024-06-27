from pyrogram import Client
import logging
import pyromod.listen
import os
import yaml
import sys
# Create and configure logger
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger()

from mailable.config import CONFIG
# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    logger.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
    quit(1)

# setting up processes
class proc:
    broadcast = False

PROCESSES = proc()

# Initialize bot
bot = Client("mailable", api_id=CONFIG.apiID, api_hash=CONFIG.apiHASH, bot_token=CONFIG.botTOKEN)


from mailable.web import app
