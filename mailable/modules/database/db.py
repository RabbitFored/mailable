from mailable.modules.database import database, stats

def scrape(data):
    collection = database["usercache"]
    userid = data.from_user.id

    firstseen = data.date
    result = collection.find_one({'userid': userid})

    try:
        result['userid']
        userexist = True

    except:
        userexist = False

    username = data.from_user.username
    firstname = data.from_user.first_name
    lastname = data.from_user.last_name
    dc = data.from_user.dc_id

    scraped = {}
    scraped['userid'] = userid
    scraped['username'] = username
    scraped['firstname'] = firstname
    scraped['lastname'] = lastname
    scraped['is-banned'] = False
    scraped['dc'] = dc
    scraped['mails'] = []

    plan = "free"
    mail_limit = { "member":5,"non_member":2 }
    send_limits = {"at_once":3}

    scraped['plan'] = {
      "type"  : plan,
      "limits": {
         "mails" : mail_limit,
         "send"  : send_limits
      }
    }

    scraped['blocked'] = {
      "domains": [],
      "mails": [],
      "regex": []
    }
    scraped['firstseen'] = firstseen

    if (userexist == False):
        collection.insert_one(scraped)
        stats.statial("users",1)


def defaults(key):
  collection=database["defaults"]
  cursor = collection.find()
  for i in cursor:
    value = i[key.lower()]
  return value

