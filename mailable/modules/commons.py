from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from mailable import strings
from mailable.modules import database as db
from mailable.modules.filters import user_filter
from mailable import bot
import yaml

def read_and_modify_one_block_of_yaml_data(filename, key, value):
    with open(f'{filename}.yaml', 'r') as f:
        data = yaml.safe_load(f)
        data[f'{key}'] = f'{value}' 
        print(data) 
    with open(f'{filename}.yaml', 'w') as file:
      yaml.dump(data,file,sort_keys=False)
    print('done!')


@bot.on_message(filters.command(["test"]))
async def test(client, message):
    test_file = open("test.yaml", "r")
    t = yaml.safe_load(test_file)
    read_and_modify_one_block_of_yaml_data('test', key='Age', value=30)

    text = t

    await message.reply_text(text)

