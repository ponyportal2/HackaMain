from flask import Flask
from flask import request
from flask import Response

import random

from time import sleep

import json
import requests

from removedupes import remove_dupes

app = Flask(__name__)

headers = {'Accept': 'application/json'}

TELEGRAM_BOT_TOKEN = "6683299914:AAFWywdA-pr6hcoAjCIs9KgU-ldCw9YbdKg"

mac_folder = '/Users/sharkmer/HackaTest/'
pc_folder = 'c:/Projects/VK/'

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
        # ZAMENIT
        idiz = []
        with open('idiz.txt') as my_file:
            for line in my_file:
                idiz.append(line[:-1])
        remove_dupes()
        idiz = list(set(idiz))
        # --------
        msg = request.get_json()
        try:
            chat_id, txt = tel_parse_message(msg)
            # ZAMENIT
            file_object = open('idiz.txt', 'a')
            file_object.write(str(chat_id) + '\n')
                # --------
            mess_to_send = str(msg['message']['from']['username']) + \
                ': ' + str(msg['message']['text'])
            # ZAMENIT
            for id in idiz:
                sleep(0.01)
                # if id != str(chat_id):
                tel_send_message(
                        id, mess_to_send)
            # --------
            else:
                tel_send_message(
                    chat_id, mess_to_send)
        except:
            print("from index(exception)-->")

    return Response('ok', status=200)


if __name__ == '__main__':
    app.run(threaded=True)


# mess_to_send = '[' + str(chat_id) + \
#     '] ' + str(msg['message']['text'])

# sdvig = random.randint(1, 100)

# def encrypt(text, s):
#     result = ""
#     for i in range(len(text)):
#         char = text[i]
#         if (char.isupper()):
#             result += chr((ord(char) + s-65) % 26 + 65)
#         else:
#             result += chr((ord(char) + s - 97) % 26 + 97)
#     return result[0:6]


# def VKblasthack(id, text):
#     bh.method('messages.send', {'user_id': id,
#               'message': text, 'random_id': 0})


# def send_photo(chat_id, file_opened):
#     method = "sendPhoto"
#     params = {'chat_id': chat_id}
#     files = {'photo': file_opened}
#     resp = requests.post('https://api.telegram.org/bot' +
#                          TELEGRAM_BOT_TOKEN + '/' + method, params, files=files)
#     return resp

    # def tel_upload_file(file_id):
    #     url = f'https://api.telegram.org/bot' + \
    #         TELEGRAM_BOT_TOKEN + '/getFile?file_id=' + file_id
    #     a = requests.post(url)
    #     json_resp = json.loads(a.content)
    #     print("a-->", a)
    #     # print("json_resp-->", json_resp)
    #     file_pathh = json_resp['result']['file_path']
    #     print("file_path-->", file_pathh)

    #     url_1 = f'https://api.telegram.org/file/bot' + \
    #         TELEGRAM_BOT_TOKEN + '/' + file_pathh
    #     b = requests.get(url_1)
    #     file_content = b.content
    #     with open(file_pathh, "wb") as f:
    #         f.write(file_content)
    #     return file_pathh

    #   def send_image(chat_id, image):
    #     url = f'https://api.telegram.org/bot' + TELEGRAM_BOT_TOKEN + '/sendPhoto'
    #     payload = {
    #         'chat_id': chat_id,
    #         'photo': image,
    #     }
    #     r = requests.post(url, json=payload)
    #     return r

    # def send_video(chat_id, video):
    #     url = f'https://api.telegram.org/bot' + TELEGRAM_BOT_TOKEN + '/sendVideo'
    #     payload = {
    #         'chat_id': chat_id,
    #         'video': video,
    #     }
    #     r = requests.post(url, json=payload)
    #     return r

    # def send_animation(chat_id, anim):
    #     url = f'https://api.telegram.org/bot' + TELEGRAM_BOT_TOKEN + '/sendAnimation'

    #     payload = {
    #         'chat_id': chat_id,
    #         'animation': anim,
    #     }
    #     r = requests.post(url, json=payload)
    #     return r