import os
from flask import Flask, request, jsonify

from main_sql import main_sql_func

app = Flask(__name__)

@app.route("/api/auth/", methods=["POST"])
def our_auth():
    # {username, password}
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400
    
    username = data.get('username')
    password = data.get('password')


if __name__ == "__main__":
    sql_engine = main_sql_func()
    app.run(debug=True)

def push_image_to_database(image_name, user_name):
    user_folder = "/" + str(user_name)
    if os.path.exists(user_folder):
        pass
    else:
        os.mkdir(user_folder)
    image_path = user_folder + "/" + image_name
    if image_exists():
        # copy image to imagepath
        pass
    else:
        # add 1 to name and push
        pass

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

    


