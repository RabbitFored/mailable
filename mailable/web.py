from quart import Quart, send_file, render_template, request
import requests
from mailable.utils import strip_script_tags
import mailparser
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json
from mailable import CONFIG, bot
import os

app = Quart(__name__, template_folder='assets')

@app.route('/')
async def index():
    return await render_template("index.html")

@app.route('/404')
async def error_page():
    return await render_template("404.html")

@app.route('/arc-sw.js')
async def arc():
    return await send_file("web/scripts/arc-sw.js")

@app.route('/favicon.ico')
async def ico():
    return await send_file("web/images/favicon.ico")

@app.route('/ostrich.png')
async def ost():
    return await send_file("mailable/assets/images/ostrich.png")


@app.route('/inbox/<user>/<id>')
async def inbox(user, id):
  m = await bot.get_messages(int(user), int(id))
  file = await m.download()
  f = open(file, "r")
  content = f.read()
  nojs = strip_script_tags(content)
  os.remove(file)
  return await render_template("inbox.html" , content = nojs)



def run():
  app.run(host="0.0.0.0", port=8080)
