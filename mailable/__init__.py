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

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    logger.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
    quit(1)


secrets_path = "secrets.yaml"
ENV = bool(os.environ.get("ENV", False)) and not os.environ.get("ENV", False) == "False"

CONFIG = {}

if ENV:
    logger.info("Using values from ENV")

    CONFIG["apiID"] = os.environ.get("apiID", None)
    CONFIG["apiHASH"] = os.environ.get("apiHASH", None)
    CONFIG["botTOKEN"] = os.environ.get("botTOKEN", None)
    CONFIG["port"] = int(os.environ.get("PORT", 5000))
    CONFIG["mongouri"] = os.environ.get("mongouri", "")
    CONFIG["apikey"] = os.environ.get("mailgun_api", "")
    CONFIG["baseURL"] = os.environ.get("baseURL", "")

    CONFIG["database"] = os.environ.get("database", "mailable")
    user_collection = os.environ.get("userCollection", "users")
    group_collection = os.environ.get("groupCollection", "groups")
    CONFIG["collections"] = {"user": user_collection, "group": group_collection}

elif os.path.isfile(secrets_path):
    logger.info("Using values from secrets.yaml")

    yaml_file = open(secrets_path, "r")
    yaml_content = yaml.safe_load(yaml_file)

    CONFIG.apiID = yaml_content["telegram"][0]["apiID"]
    CONFIG.apiHASH = yaml_content["telegram"][1]["apiHASH"]
    CONFIG.botTOKEN = yaml_content["telegram"][2]["botTOKEN"]

    CONFIG.mongouri = yaml_content["MongoDB"][0]["URI"]
    CONFIG.database = yaml_content["MongoDB"][1]["database"]
    CONFIG.collection = yaml_content["MongoDB"][2]["collection"]

else:
    print("This app is not configured correctly. Check README or contact support.")
    quit(1)

settings_file = open("settings.yaml", "r")
settings = yaml.safe_load(settings_file)

CONFIG["settings"] = settings


# Initialize bot
bot = Client("mailable", api_id=CONFIG["apiID"], api_hash=CONFIG["apiHASH"], bot_token=CONFIG["botTOKEN"])


from mailable.web import app

class proc:
    broadcast = False

PROCESSES = proc()