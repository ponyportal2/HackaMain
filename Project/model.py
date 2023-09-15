import os
from flask import Flask, request, jsonify

from sql_main import main_sql_func
from werkzeug.security import check_password_hash, generate_password_hash

import shutil

sql_engine = main_sql_func()
app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/api/login/", methods=["POST"])
def login():
    # input: {login, password}

    data = request.get_json()
    if not data:
        return jsonify({'status': 'error'}), 400
    
    username = data.get('login')
    password_hash = generate_password_hash(data.get('password'))

    current_datetime = datetime.now()
    current_time_string = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    if sql_username_exists(username) == False:
        return jsonify({'status': 'no_user'})
    elif sql_get_user_password_hash(username) == password_hash:
        auth_token = generate_password_hash(f'{username}_%_{password_hash}_%_{current_time_string}') 
        sql_change_user_token(username)
        return jsonify({'status': 'ok', 'token': auth_token})
    else:
        return jsonify({'status': 'invalid'})



@app.route("/api/register/", methods=["POST"])
def register():
    # input: {login, password}

    data = request.get_json()
    if not data:
        return jsonify({'status': 'error'}), 400
    
    username = data.get('username')
    password = data.get('password')

    if sql_username_exists(username) == True:
        return jsonify({'status': 'user_exists'})
    else:
        sql_add_user(username, generate_password_hash(password))
        return jsonify({'status': 'success'})

@app.route("/api/verify_token/", methods=["POST"])
def verify_token():
    # input: {token}

    data = request.get_json()
    if not data:
        return jsonify({'status': 'error'}), 400
    
    token = data.get('token')
    if sql_token_exists_in_db(token) == True:
        return jsonify({'status': 'valid'})
    else:
        return jsonify({'status': 'invalid'})


@app.route("/api/upload_file/", methods=["POST"])
def upload_file():
    # input: {token, filename} , file
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error'}), 400 # No JSON data provided

    if 'file' not in request.files:
        flash('No file part')
        return jsonify({'status': 'error'}), 400 # No file part

    username = sql_token_to_user(data.get('token'))
    file_path = username + data.get(filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return jsonify({'status': 'error'}), 400 # No selected file

    if file and allowed_file(file.filename):
        unique_file_path = secure_filename(file.filename)
        file.save(file_path)
        return jsonify({'status': 'success'}), 200

@app.route("/api/mv_file/", methods=["POST"])
def mv_file():
    # input: {token, filename_from, filename_into}
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error'}), 400 # No JSON data provided

    username = sql_token_to_user(data.get('token'))
    file_from = username + data.get('filename_from')
    file_to = username + data.get('filename_into')
    os.makedirs(os.path.dirname(file_to), exist_ok=True)
    shutil.move(file_from, file_to)
    os.remove(file_from)
    sql_change_image_location(file_from, file_to)
    return jsonify({'status': 'success'}), 200 # No selected file

@app.route("/api/del_file/", methods=["POST"])
def del_file():
    # input: {token, filename}
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error'}), 400 # No JSON data provided

    username = sql_token_to_user(data.get('token'))
    file_name = username + data.get('filename')'
    os.remove(file_name)
    sql_remove_image_location(file_name)
    return jsonify({'status': 'success'}), 200 # No selected file

@app.route("/api/get_all_files/", methods=["POST"])
    # { token, pattern } (паттерн по типу \*/\*.jpg и т.п.)
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error'}), 400 # No JSON data provided

    username = sql_token_to_user(data.get('token'))
    return jsonify(sql_get_all_user_pictures_with_pattern(username, data.get('pattern')))

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp', 'bmp', 'mp4'}
    file_extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    return '.' in filename and file_extension in ALLOWED_EXTENSIONS

    # sql_get_user_password(username)
    # sql_add_user(username, password)
    # sql_set_user_auth_status(username, status) # status will be 1 or 0
    # sql_get_all_user_album_pictures(username)
    # sql_post_image_location(username, album)
    # sql_get_user_telegram_authkey(username)