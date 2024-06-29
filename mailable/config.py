import os
import yaml
from mailable import logger

class conf:
  def get_sudoers(self):
      sudoers = []
      sudoers_grps = self.settings["sudoers"]
      grps = self.settings["groups"]
      for grp in grps:
          if grp["name"] in sudoers_grps:
              sudoers = sudoers + grp["users"]
      return sudoers
      
  def get_limits(self,type):
      grps = self.settings["groups"]
      for grp in grps:
          if grp["name"] == type:
              return grp["limits"]
          
      
              
      
      
      

ENV = bool(os.environ.get("ENV", False)) and not os.environ.get("ENV", False) == "False"
secrets_path = "secrets.yaml"
settings_path = "settings.yaml"
if ENV:
    logger.info("Using values from ENV")

    apiID = os.environ.get("apiID", None)
    apiHASH = os.environ.get("apiHASH", None)
    botTOKEN = os.environ.get("botTOKEN", None)
    port = int(os.environ.get("PORT", 5000))
    mongouri = os.environ.get("mongouri", "")
    apikey = os.environ.get("mailgun_api", "")
    baseURL = os.environ.get("baseURL", "")

    database = os.environ.get("database", "mailable")
    user_collection = os.environ.get("userCollection", "users")
    group_collection = os.environ.get("groupCollection", "groups")
    collections = {"user": user_collection, "group": group_collection}

elif os.path.isfile(secrets_path):
    logger.info("Using values from secrets.yaml")

    yaml_file = open(secrets_path, "r")
    yaml_content = yaml.safe_load(yaml_file)

    apiID = yaml_content["telegram"][0]["apiID"]
    apiHASH = yaml_content["telegram"][1]["apiHASH"]
    botTOKEN = yaml_content["telegram"][2]["botTOKEN"]

    mongouri = yaml_content["MongoDB"][0]["URI"]
    database = yaml_content["MongoDB"][1]["database"]
    Ccollection = yaml_content["MongoDB"][2]["collection"]

else:
    print("This app is not configured correctly. Check README or contact support.")
    quit(1)

CONFIG = conf()
CONFIG.apiID = apiID
CONFIG.apiHASH = apiHASH
CONFIG.botTOKEN = botTOKEN
CONFIG.port = port
CONFIG.mongouri = mongouri
CONFIG.database = database
CONFIG.collections = collections
CONFIG.apikey = apikey
CONFIG.baseURL = baseURL

settings_file = open(settings_path, "r")
settings = yaml.safe_load(settings_file)

CONFIG.settings = settings