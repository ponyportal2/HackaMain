import os
import time
from flask import Flask, request, jsonify, send_file

from sql_main import main_sql_func
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

from sql_funct import *

import shutil

main_sql_func()
app = Flask(__name__)

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
    if sql_token_exists_in_db(token) == True:
        print("YES")
        return jsonify({'status': 'valid'})
    else:
        print("NO")
        return jsonify({'status': 'invalid'})

@app.route("/api/upload_file/", methods=["POST"]) # WORKS
def upload_file():
    # input: {token, filename} , file
    if 'file' not in request.files:
        flash('No file part')
        return jsonify({'status': 'error'}), 400 # No file part

    username = sql_token_to_user(request.form['token'])
    file_path = username + '/' + request.form['filename']
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
        sql_post_image_location(username, file_path)
        return jsonify({'status': 'success'}), 200

@app.route("/api/mv_file/", methods=["POST"]) # WORKS
def mv_file():
    # input: {token, filename_from, filename_into}
    data = request.json
    data_error_check(data)

    # username = sql_token_to_user(data.get('token'))
    username = "a"
    file_from = username + "/" + data.get('filename_from')
    file_to = username + "/" + data.get('filename_into')
    os.makedirs(os.path.dirname(file_to), exist_ok=True)
    try:
        shutil.move(file_from, file_to)
        sql_change_image_location(file_from, file_to)
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
    file_name = username + '/' + data.get('filename')
    os.remove(file_name)
    sql_remove_image_location(file_name)
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
    return jsonify({'returned': list_folders_in_directory(username)})

@app.route("/api/set_avatar_pic/", methods=["POST"]) # WORKS
def set_avatar_pic():
    # {token, filename}
    data = request.json
    data_error_check(data)

    username = sql_token_to_user(data.get('token'))
    filename = data.get('filename')

    sql_change_avatar(username, username + "/" + filename) # ????
    return jsonify({'status': 'success'}), 200

@app.route("/api/get_avatar_pic/", methods=["POST"]) # WORKS
def get_avatar_pic():
    # {token}
    data = request.json
    data_error_check(data)
    username = sql_token_to_user(data.get('token'))

    return jsonify({'returned': sql_get_avatar(username)})

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
        pictures = sql_get_all_user_pictures_with_pattern(sql_token_to_user(token))
        if kartinka in pictures:
            image_path = os.path.join(kartinka)
            if not os.path.exists(image_path):
                return jsonify({'status': 'error'}), 400 # No such file
            return send_file(image_path, mimetype='image/jpeg')
        else: 
            return jsonify({'status': 'invalid_token'}), 400 # No file part
    else:
        return jsonify({'status': 'no_token_found'}), 400 # No file part

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

def data_error_check(data):
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error'}), 400 # No JSON data provided

if __name__ == "__main__":
    app.run(debug=True)