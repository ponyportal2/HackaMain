from flask import Flask, request, Response, redirect, url_for, session, request
# from authlib.integrations.flask_client import OAuth
# from okta import UsersClient
import os
# okta_client = UsersClient("https://dev-828z8l7nmnimevrx.us.auth0.com", "00u9QkUX6Uz2u7o0WCUyN4r9voMSeTtqzraBfCy_zH")

# from werkzeug.security import check_password_hash
import db_methods
# import random
import datetime
from time import sleep

# import json
import requests

from removedupes import remove_dupes
# print(os.urandom(20).hex())
app = Flask(name)
app.config['SECRET_KEY'] = 'af4d15d4951386aa1494672be965a18ea25e6782'
# app.permanent_session_lifetime = datetime.timedelta(days=1)
# oauth = OAuth(app)
# my_app = oauth.register('my_app', {...})
headers = {'Accept': 'application/json'}

db_methods.sql_add_user("rand_all", "123456")
print(db_methods.sql_get_user_telegram_authkey("rand_all"))
db_methods.sql_add_user("abobig69", "3456")
print(db_methods.sql_get_user_telegram_authkey("abobig69"))
db_methods.sql_add_user("good_but", "3456")
print(db_methods.sql_get_user_telegram_authkey("good_but"))

TELEGRAM_BOT_TOKEN = "6444851678:AAFz6FJlzxsLzudQGpMPbREQKWpMaWeKYa4"

def tel_parse_message(message):
    print("message-->", message)
    try:
        chat_id = message['message']['chat']['id']
        txt = message['message']['text']
        print('\nText sender: ' +
                str(message['message']['from']
                    ['username'] + " " + str(chat_id)) + " " + str(chat_id))
        # print("chat_id-->", chat_id)
        print("txt-->", txt)
        print('\n')
        return chat_id, txt
    except:
        print("NO text found-->>")


def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot' + TELEGRAM_BOT_TOKEN + '/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    r = requests.post(url, json=payload)
    return r

@ app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        try:
            chat_id, txt = tel_parse_message(msg)
            tel_login = str(msg['message']['from']['username'])
            tel_code = str(msg['message']['text'])
            # get info from database
            if db_methods.sql_username_exists(tel_login):
                db_authkey = db_methods.sql_get_user_telegram_authkey(tel_login)
            else:
                db_authkey = ""

            # check login and auth code
            if tel_code == db_authkey:
                status_msg = "success"
            else:
                status_msg = "error"
                
            mess_to_send = tel_login + ': ' + status_msg
            tel_send_message(
                        chat_id, mess_to_send)
        except:
            print("from index(exception)-->")

    return Response('ok', status=200)


if name == 'main':
    app.run(threaded=True)