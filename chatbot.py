import sys
from io import BytesIO
from telegram import ReplyKeyboardMarkup,KeyboardButton
import telegram
from flask import Flask, request, send_file
from fsm import TocMachine
from choose import *

API_TOKEN = '397040538:AAEPi9-yoIPjox1xyrYkfUtDSX6aVrAxVUg'
WEBHOOK_URL = 'https://b0a80be7.ngrok.io/hook'

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)

machine = TocMachine(
    bot,
    states=[
        'user',
        'state1',
        'state2',
        'state3',
        'state4'
    ],
    transitions=[
        {
            'trigger': 'noodle',
            'source': 'user',
            'dest': 'state1',
        },
        {
            'trigger': 'rice',
            'source': 'user',
            'dest': 'state2',
        },
        {
            'trigger': 'cookie',
            'source': 'user',
            'dest': 'state3',
        },
        {
            'trigger': 'cake',
            'source': 'user',
            'dest': 'state4',
        },
        {
            'trigger': 'go_back',
            'source': [
                'state1',
                'state2',
                'state3',
                'state4'
            ],
            'dest': 'user'
        }
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)
def btn():
    button_list = [
    [KeyboardButton("noodle"),
    KeyboardButton("rice")],
    [KeyboardButton("cookie"),
     KeyboardButton("cake")]
    ]
    reply_markup = ReplyKeyboardMarkup(button_list)
    bot.send_message(update.message.chat_id, "Recipes", reply_markup=reply_markup)

def choice():
    global input
    input = input.lower()
    recipe(input)
    if input == "noodle":
        machine.noodle(update);
        cook(update)
    elif input == "rice":
        machine.rice(update);
        cook(update)
    elif input == "cookie":
        machine.cookie(update);
        cook(update)
    elif input == "cake":
        machine.cake(update);
        cook(update)
    if input == "/start":
        update.message.reply_text("You can choose:\n noodle\n rice\n coockie\n cake")
    btn()
        
def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    global update
    global input
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    input = update.message.text
    print(input)
    choice()
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')

if __name__ == "__main__":
    _set_webhook()
    app.run()

