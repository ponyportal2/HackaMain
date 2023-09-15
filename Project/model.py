import os
from flask import Flask, request, jsonify

from sql_main import main_sql_func

sql_engine = main_sql_func()
app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/api/auth/", methods=["POST"])
def our_auth():
    # input: {username, password}
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400
    
    username = data.get('username')
    password = data.get('password')

    sql_username_exists(username)
    sql_get_user_password(username)
    sql_add_user(username, password)
    sql_set_uset_auth_status(username, status) # status will be 1 or 0

    if yes:
        return jsonify({'status': 'valid'})
    elif no:
        return jsonify({'status': 'invalid'})

@app.route("/upload/", methods=["GET"])
def push_image_to_database():
    if 'file' not in request.files:
        flash('No file part') # what is flash?
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['/aboba/'], filename))
        return redirect(url_for('download_file', name=filename))
    # user_folder = "/" + str(user_name)
    # if os.path.exists(user_folder):
    #     pass
    # else:
    #     os.mkdir(user_folder)
    # image_path = user_folder + "/" + image_name
    # if image_exists():
    #     # copy image to imagepath
    #     pass
    # else:
    #     # add 1 to name and push
    #     pass

def get_all_user_images_from_database(user_name):
    result = []
    # from sql
    return result

def image_exists(image_name, user_name):
    image_path = "/" + user_name + "/" + image_name
    if os.path.exists(image_path):
        return True
    else:
        return False

    


