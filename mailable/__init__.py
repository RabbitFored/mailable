from pyrogram import Client
from config import apiID, apiHASH, botTOKEN
import logging
import pyromod.listen
from mailable.web import app 
# Create and configure logger
logging.basicConfig(
  format="%(asctime)s - %(levelname)s - %(message)s",
  level=logging.INFO)

logger = logging.getLogger()

# Initialize bot
bot = Client("mailable",
                 api_id=apiID,
                 api_hash=apiHASH,
                 bot_token=botTOKEN)


