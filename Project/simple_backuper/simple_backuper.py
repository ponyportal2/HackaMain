import os
import time
import requests
import json
from flask import Flask, request, jsonify, send_file, redirect, url_for, session, render_template, abort
from authlib.integrations.flask_client import OAuth

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import base64

import shutil

expected_token = ""
with open("key", "r") as key_file:
    expected_token = key_file.read().strip()

app = Flask(__name__)


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp', 'bmp', 'mp4'}
    file_extension = filename.rsplit(
        '.', 1)[1].lower() if '.' in filename else ''
    return '.' in filename and file_extension in ALLOWED_EXTENSIONS


@app.route("/api/upload_file_backup/", methods=["POST"])
def upload_file():
    data = request.form

    if "filename" not in request.files or "token" not in request.files or "file" not in request.files:
        return jsonify({'status': 'missing_fields'}), 400

    filename_file = request.files["filename"]
    token_file = request.files["token"]
    token = token_file.read().decode('utf-8')

    if token != expected_token:
        return jsonify({'status': 'invalid_token'}), 400

    file_path = filename_file.read().decode('utf-8')

    if file_path == '':
        flash('No selected file')
        return jsonify({'status': 'error'}), 400  # No selected file

    file_content = request.files["file"].read()

    if file_content and allowed_file(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as fs:
            fs.write(file_content)
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'error'}), 400


if __name__ == "__main__":
    port = 5002
    app.run(host="0.0.0.0", port=port, debug=True)
