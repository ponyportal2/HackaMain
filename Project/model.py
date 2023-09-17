import os
import time
import requests
import shutil

import json
from flask import Flask, request, jsonify, send_file, redirect, url_for, session, render_template, abort
from authlib.integrations.flask_client import OAuth

from sql_main import main_sql_func
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

from sql_funct import *

import shutil

main_sql_func()
app = Flask(__name__)

# pbkdf2:sha256:600000$V8fkPte4iaVXhRNW$d1e84745562ce3c038cb7330164123b9d35cc871b3aa522d817adfaa34ef4b00
# pbkdf2:sha256:600000$V8fkPte4iaVXhRNW$d1e84745562ce3c038cb7330164123b9d35cc871b3aa522d817adfaa34ef4b00

@app.route("/api/login/", methods=["POST", "GET"]) # TESTED
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
        auth_token = generate_password_hash(f'{username}_%_{password}_%_{current_time_string}') 
        sql_change_auth_token(username, auth_token)
        print(f'Signed in with token: {auth_token}')
        return jsonify({'status': 'ok', 'token': auth_token})
    else:
        return jsonify({'status': 'invalid'})

@app.route("/api/register/", methods=["POST"]) # TESTED
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

@app.route("/api/verify_token/", methods=["POST"]) # WORKS
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

@app.route("/api/upload_file/", methods=["POST"]) # WORKS
def upload_file():
    # input: {token, filename} , file
    if 'file' not in request.files:
        flash('No file part')
        return jsonify({'status': 'error'}), 400 # No file part

    username = sql_token_to_user(request.form['token'])
    file_path = f'users/{username}/{request.form["filename"]}'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    file = request.files['file'].read()

    if file_path == '':
        flash('No selected file')
        return jsonify({'status': 'error'}), 400 # No selected file

    username = sql_token_to_user(request.form['token'])
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    if file and allowed_file(file_path):
        print("\n"+ file_path+"\n")
        with open(file_path, "wb") as fs:
            fs.write(file)
        sql_post_image_location(username, f'{request.form["filename"]}')
        return jsonify({'status': 'success'}), 200

@app.route("/api/mv_file/", methods=["POST"]) # WORKS
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
        sql_change_image_location(user_id, data.get('filename_into'), data.get('filename_into'))
        return jsonify({'status': 'success'}), 200
    except:
        if not os.listdir(os.path.dirname(file_to)):
            os.rmdir(os.path.dirname(file_to))
        return jsonify({'status': 'no_from_file'}), 200

@app.route("/api/del_file/", methods=["POST"]) # WORKS
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

@app.route("/api/get_all_files/", methods=["POST"]) # WORKS
def get_all_files():
    # {token, pattern} (паттерн по типу \*/\*.jpg и т.п.)
    data = request.json
    data_error_check(data)

    username = sql_token_to_user(data.get('token'))
    print_table("users")
    print_table("pictures")
    initial = sql_get_all_user_pictures_with_pattern(username, data.get('pattern'))
    to_return = [item[0] for item in initial]
    print(to_return)
    return jsonify({'returned': to_return})

@app.route("/api/get_all_folders/", methods=["POST"]) # WORKS
def get_all_folders():
    # {token}
    data = request.json
    data_error_check(data)

    username = sql_token_to_user(data.get('token'))
    return jsonify({'returned': list_folders_in_directory(f'users/{username}')})

@app.route("/api/create_folder/", methods=["POST"]) # WORKS
def create_folder_req():
    # {token}
    data = request.json
    data_error_check(data)

    username = sql_token_to_user(data.get('token'))
    return jsonify({'returned': create_folder(f'users/{username}/{data.get("folder")}')})

@app.route("/api/delete_folder/", methods=["POST"]) # WORKS
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

@app.route("/api/set_avatar_pic/", methods=["POST"]) # WORKS
def set_avatar_pic():
    # {token, filename}
    data = request.json
    data_error_check(data)

    username = sql_token_to_user(data.get('token'))
    filename = data.get('filename')

    sql_change_avatar(username, filename) # ????
    return jsonify({'status': 'success'}), 200

@app.route("/api/get_avatar_pic/", methods=["POST"]) # WORKS
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


@app.route("/api/logout/", methods=["POST"]) # TESTED
def logout():
    # {token}
    data = request.json
    data_error_check(data)
    token = data.get('token')
    sql_delete_token(token)
    return jsonify({'status': 'success'}), 200

@app.route("/api/images/<path:kartinka>", methods=["GET"])
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
                return jsonify({'status': 'error'}), 400 # No such file

            return send_file(image_path, mimetype='image/jpeg')
        else: 
            return jsonify({'status': 'invalid_token'}), 400 # No file part
    else:
        return jsonify({'status': 'no_token_found'}), 400 # No file part

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
def home():
  return render_template("home.html", session=session.get("user"), info=json.dumps(session.get("user"), indent=4))

@app.route("/signin-google")
def googleCallback():
  token = oauth.hackmedia.authorize_access_token()
  session["user"] = token
  return redirect(url_for("home"))


@app.route("/google-login")
def googleLogin():
  if "user" in session:
      abort(404)
  return oauth.hackmedia.authorize_redirect(redirect_uri=url_for("googleCallback", _external=True))
  
@app.route("/logauth")
def logauth():
    session.pop("user", None)
    return redirect(url_for("home"))
# --------


# Functions:

def allowed_file(filename): 
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp', 'bmp', 'mp4'}
    file_extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    return '.' in filename and file_extension in ALLOWED_EXTENSIONS

def list_folders_in_directory(directory_path): 
    try:
        items = os.listdir(directory_path)
        folders = [item for item in items if os.path.isdir(os.path.join(directory_path, item))]
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
        return jsonify({'status': 'error'}), 400 # No JSON data provided

if __name__ == "__main__":
    app.run(debug=True, port=appConf.get("FLASK_PORT"))