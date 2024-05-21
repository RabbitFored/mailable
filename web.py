from quart import Quart, send_file, render_template, request
import requests
from utils import strip_script_tags
import mailparser
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json

app = Quart(__name__, template_folder='web')

@app.route('/')
async def index():
    return await render_template("index.html")

@app.route('/404')
async def error_page():
    return await render_template("404.html")

@app.route('/arc-sw.js')
async def arc():
    return await send_file("web/static/scripts/arc-sw.js")

@app.route('/favicon.ico')
async def ico():
    return await send_file("web/static/images/favicon.ico")
  
@app.route('/ostrich.png')
async def ost():
    return await send_file("web/static/images/ostrich.png")


@app.route('/mail/<id>', methods=['GET'])
async def pages(id):
    url = f"https://paste.theostrich.eu.org/raw/{id}"
    req = requests.get(url)
    content = req.text
    nojs = strip_script_tags(content)
    return await render_template("inbox.html" , content = nojs )

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
  requests.post("https://mail.bruva.co/secretmessages",data=multipart_data,headers={'Content-Type': multipart_data.content_type})
  return 'Hello, World!'
    
def run():
  app.run(host="0.0.0.0", port=8080)
