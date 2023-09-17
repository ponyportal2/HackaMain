import os
import io
import time
import requests
import shutil

import json
from flask import Flask, request, jsonify, send_file, redirect, url_for, session, render_template, abort
from flask_cors import CORS, cross_origin
from authlib.integrations.flask_client import OAuth

from sql_main import main_sql_func
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

from thumb_gen import *
from sql_funct import *

import shutil

main_sql_func()
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# pbkdf2:sha256:600000$V8fkPte4iaVXhRNW$d1e84745562ce3c038cb7330164123b9d35cc871b3aa522d817adfaa34ef4b00
# pbkdf2:sha256:600000$V8fkPte4iaVXhRNW$d1e84745562ce3c038cb7330164123b9d35cc871b3aa522d817adfaa34ef4b00


@app.route("/api/login/", methods=["POST", "GET"])  # TESTED
@cross_origin()
def login():
    data = request.json
    # input: {login, password}
    data_error_check(data)

    username = data.get('login')
    password = data.get('password')

    current_datetime = time.time()
    current_time_string = f'{current_datetime}'

    if sql_username_exists(username) == False:
        return jsonify({'status': 'no_user'})
    elif check_password_hash(sql_get_user_password_hash(username), password):
        auth_token = generate_password_hash(
            f'{username}_%_{password}_%_{current_time_string}')
        sql_change_auth_token(username, auth_token)
        print(f'Signed in with token: {auth_token}')
        return jsonify({'status': 'ok', 'token': auth_token})
    else:
        return jsonify({'status': 'invalid'})


@app.route("/api/register/", methods=["POST"])  # TESTED
@cross_origin()
def register():
    # input: {login, password}
    data = request.json
    data_error_check(data)

    username = data.get('login')
    password = data.get('password')

    if sql_username_exists(username) == True:
        return jsonify({'status': 'user_exists'})
    else:
        sql_add_user(username, generate_password_hash(password))
        return jsonify({'status': 'success'})


@app.route("/api/verify_token/", methods=["POST"])  # WORKS
@cross_origin()
def verify_token():
    # input: {token}
    data = request.json
    data_error_check(data)

    token = data.get('token')
    print(f'Token: {token} does exists: {sql_token_exists_in_db(token)}')
    if sql_token_exists_in_db(token) == True:
        username = sql_token_to_user(data.get('token'))
        return jsonify({'status': 'valid', 'user': f'{username}'})
    else:
        return jsonify({'status': 'invalid'}), 400


def send_to_backuper(the_file, file_path):
    key = "HKekm,4qcP0e2KYERmhr#clUsqlED6#yg9U29HN%IRU%JsPr(k"
    files = {
        'file': the_file,
        'filename': ('filename', io.BytesIO(file_path.encode())),
        'token': ('key', io.BytesIO(key.encode()))
    }
    backup_server_url = "http://127.0.0.1:5002/api/upload_file_backup/"
    response = requests.post(backup_server_url, files=files)


@app.route("/api/upload_file/", methods=["POST"])  # WORKS
@cross_origin()
def upload_file():
    # input: {token, filename} , file
    if 'file' not in request.files:
        flash('No file part')
        return jsonify({'status': 'error'}), 400  # No file part

    username = sql_token_to_user(request.form['token'])
    file_path = f'users/{username}/{request.form["filename"]}'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    file = request.files['file'].read()

    if file_path == '':
        flash('No selected file')
        return jsonify({'status': 'error'}), 400  # No selected file

    username = sql_token_to_user(request.form['token'])
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    if file and allowed_file(file_path):
        print("\n" + file_path+"\n")
        with open(file_path, "wb") as fs:
            fs.write(file)
        sql_post_image_location(username, f'{request.form["filename"]}')

        send_to_backuper(file, file_path)
        if not is_video_file(request.form['filename']):
            create_thumb(file_path)

        return jsonify({'status': 'success'}), 200


@app.route("/api/mv_file/", methods=["POST"])  # WORKS
@cross_origin()
def mv_file():
    # input: {token, filename_from, filename_into}
    data = request.json
    data_error_check(data)

    user_id = sql_token_to_user_id(data.get('token'))
    username = sql_token_to_user(data.get('token'))
    file_from = f'users/{username}/{data.get("filename_from")}'
    file_to = f'users/{username}/{data.get("filename_into")}'
    os.makedirs(os.path.dirname(file_to), exist_ok=True)
    try:
        shutil.move(file_from, file_to)
        sql_change_image_location(user_id, data.get(
            'filename_into'), data.get('filename_into'))
        return jsonify({'status': 'success'}), 200
    except:
        if not os.listdir(os.path.dirname(file_to)):
            os.rmdir(os.path.dirname(file_to))
        return jsonify({'status': 'no_from_file'}), 200


@app.route("/api/del_file/", methods=["POST"])  # WORKS
@cross_origin()
def del_file():
    # input: {token, filename}
    data = request.json
    data_error_check(data)

    username = sql_token_to_user(data.get('token'))
    user_id = sql_token_to_user_id(data.get('token'))
    file_name = f'users/{username}/{data.get("filename")}'
    try:
        os.remove(file_name)
    except Exception as e:
        pass

    sql_remove_image_location(user_id, f'{data.get("filename")}')
    return jsonify({'status': 'success'}), 200


@app.route("/api/get_all_files/", methods=["POST"])  # WORKS
@cross_origin()
def get_all_files():
    # {token, pattern} (паттерн по типу \*/\*.jpg и т.п.)
    data = request.json
    data_error_check(data)

    username = sql_token_to_user(data.get('token'))
    print_table("users")
    print_table("pictures")
    initial = sql_get_all_user_pictures_with_pattern(
        username, data.get('pattern'))
    to_return = [item[0] for item in initial]
    print(to_return)
    return jsonify({'returned': to_return})


@app.route("/api/get_all_folders/", methods=["POST"])  # WORKS
@cross_origin()
def get_all_folders():
    # {token}
    data = request.json
    data_error_check(data)

    username = sql_token_to_user(data.get('token'))
    return jsonify({'returned': list_folders_in_directory(f'users/{username}')})


@app.route("/api/create_folder/", methods=["POST"])  # WORKS
@cross_origin()
def create_folder_req():
    # {token}
    data = request.json
    data_error_check(data)

    username = sql_token_to_user(data.get('token'))
    return jsonify({'returned': create_folder(f'users/{username}/{data.get("folder")}')})


@app.route("/api/delete_folder/", methods=["POST"])  # WORKS
@cross_origin()
def delete_folder_req():
    # {token}
    data = request.json
    data_error_check(data)

    username = sql_token_to_user(data.get('token'))
    user_id = sql_token_to_user_id(data.get('token'))
    delete_folder(f'users/{username}/{data.get("folder")}')
    # print_table('pictures')
    print("REMOVING WHERE ", user_id, data.get("folder"))
    sql_remove_image_by_pattern(user_id, f'{data.get("folder")}/%')
    return jsonify({'status': 'ok'})


@app.route("/api/set_avatar_pic/", methods=["POST"])  # WORKS
@cross_origin()
def set_avatar_pic():
    # {token, filename}
    data = request.json
    data_error_check(data)

    username = sql_token_to_user(data.get('token'))
    filename = data.get('filename')

    sql_change_avatar(username, filename)  # ????
    return jsonify({'status': 'success'}), 200


@app.route("/api/get_avatar_pic/", methods=["POST"])  # WORKS
@cross_origin()
def get_avatar_pic():
    # {token}
    data = request.json
    data_error_check(data)
    token = data.get('token')
    if (token and sql_token_exists_in_db(token)):
        username = sql_token_to_user(token)
        avatar = sql_get_avatar(username)
        if (avatar):
            return jsonify({'exists': True, 'returned': avatar}), 200
        else:
            return jsonify({'exists': False, 'returned': 'ur dumb'}), 200
    else:
        return jsonify({'status': 'failed'}), 401


@app.route("/api/logout/", methods=["POST"])  # TESTED
@cross_origin()
def logout():
    # {token}
    data = request.json
    data_error_check(data)
    token = data.get('token')
    sql_delete_token(token)
    return jsonify({'status': 'success'}), 200


@app.route("/api/images/<path:kartinka>", methods=["GET"])
@cross_origin()
def get_image(kartinka):
    token = ""
    auth_header = request.headers.get("Authorization")
    if auth_header:
        token = auth_header.split("Bearer ")[1]

    if sql_token_exists_in_db(token) == True:
        user = sql_token_to_user(token)
        if sql_does_image_exist(f'{user}/{kartinka}'):
            image_path = os.path.join(f'users/{user}/{kartinka}')
            if not os.path.exists(image_path):
                return jsonify({'status': 'error'}), 400  # No such file

            return send_file(image_path, mimetype='image/jpeg')
        else:
            return jsonify({'status': 'invalid_token'}), 400  # No file part
    else:
        return jsonify({'status': 'no_token_found'}), 400  # No file part


@app.route("/api/thumbs/<path:kartinka>", methods=["GET"])
@cross_origin()
def get_thumb(kartinka):
    token = ""
    auth_header = request.headers.get("Authorization")
    if auth_header:
        token = auth_header.split("Bearer ")[1]

    if sql_token_exists_in_db(token) == True:
        user = sql_token_to_user(token)
        if sql_does_image_exist(f'{user}/{kartinka}'):
            image_path = os.path.join(f'thumb/users/{user}/{kartinka}')
            if not os.path.exists(image_path):
                return jsonify({'status': 'error'}), 400  # No such file

            return send_file(image_path, mimetype='image/jpeg')
        else:
            return jsonify({'status': 'invalid_token'}), 400  # No file part
    else:
        return jsonify({'status': 'no_token_found'}), 400  # No file part

# ------------------------------------------------------------------------------------
# TELEGRAM_BOT:


TELEGRAM_BOT_TOKEN = "6444851678:AAFz6FJlzxsLzudQGpMPbREQKWpMaWeKYa4"
# ПРОБРОС:
# https://api.telegram.org/bot6444851678:AAFz6FJlzxsLzudQGpMPbREQKWpMaWeKYa4/setWebhook?url=<URL_ИЗ_НГРОКА>


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


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        try:
            chat_id, txt = tel_parse_message(msg)
            tel_login = str(msg['message']['from']['username'])
            telegram_code = str(msg['message']['text'])

            if telegram_code == str(sql_get_user_telegram_authkey(tel_login)):
                status_msg = "You are now an authorized user."
                sql_set_user_auth_status(tel_login, 1)
            else:
                status_msg = "Wrong key."

            mess_to_send = status_msg
            tel_send_message(
                chat_id, mess_to_send)
        except:
            print("from index(exception)-->")

    return Response('ok', status=200)


# ------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------
# TELEGRAM_METHODS:


@app.route("/api/get_auth_status/", methods=["POST"])
def get_auth_status():
    # {token}
    data = request.json
    data_error_check(data)

    username = sql_token_to_user(data.get('token'))

    return_value = str(sql_get_user_auth_status(username))
    return jsonify({'status': return_value}), 200


@app.route("/api/get_auth_key/", methods=["POST"])
def get_auth_key():
    # {token}
    data = request.json
    data_error_check(data)

    username = sql_token_to_user(data.get('token'))

    return_value = str(sql_get_user_telegram_authkey(username))
    return jsonify({'status': return_value}), 200


# ------------------------------------------------------------------------------------
# AUTH
appConf = {
    "OAUTH2_CLIENT_ID": "116203304654-fp8noi61ff6kdo5gnu40b7d41nbojn6b.apps.googleusercontent.com",
    "OAUTH2_CLIENT_SECRET": "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",
    "OAUTH2_META_URL": "https://accounts.google.com/.well-known/openid-configuration",
    "FLASK_SECRET": "91db5be4-d545-4a28-9212-5b03b642bbab",
    "FLASK_PORT": 5000
}

app.secret_key = appConf.get("FLASK_SECRET")

oauth = OAuth(app)

oauth.register(
    name="hackmedia",
    client_id=appConf.get("OAUTH2_CLIENT_ID"),
    client_secret=appConf.get("OAUTH2_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'{appConf.get("OAUTH2_META_URL")}',
)
# -----

# AUTH_APP_ROUTES:


@app.route("/home")
@cross_origin()
def home():
    return render_template("home.html", session=session.get("user"), info=json.dumps(session.get("user"), indent=4))


@app.route("/signin-google")
@cross_origin()
def googleCallback():
    token = oauth.hackmedia.authorize_access_token()
    session["user"] = token
    return redirect(url_for("home"))


@app.route("/google-login")
@cross_origin()
def googleLogin():
    if "user" in session:
        abort(404)
    return oauth.hackmedia.authorize_redirect(redirect_uri=url_for("googleCallback", _external=True))


@app.route("/logauth")
@cross_origin()
def logauth():
    session.pop("user", None)
    return redirect(url_for("home"))
# --------


# Functions:

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png',
                          'webp', 'bmp', 'mp4', 'avi', 'mov', 'mkv', 'gif'}
    file_extension = filename.rsplit(
        '.', 1)[1].lower() if '.' in filename else ''
    return '.' in filename and file_extension in ALLOWED_EXTENSIONS


def is_video_file(filename):
    ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'gif'}
    file_extension = filename.rsplit(
        '.', 1)[1].lower() if '.' in filename else ''
    return '.' in filename and file_extension in ALLOWED_EXTENSIONS


def list_folders_in_directory(directory_path):
    try:
        items = os.listdir(directory_path)
        folders = [item for item in items if os.path.isdir(
            os.path.join(directory_path, item))]
        return folders
    except OSError as e:
        print(f"Error: {e}")
        return []


def create_folder(directory):
    os.makedirs(directory, exist_ok=True)


def delete_folder(directory):
    shutil.rmtree(directory)


def data_error_check(data):
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error'}), 400  # No JSON data provided


if __name__ == "__main__":
    app.run(debug=True, port=appConf.get("FLASK_PORT"))
