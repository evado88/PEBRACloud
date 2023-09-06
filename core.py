import os
import json
import sys
from flask import Flask, Blueprint, send_from_directory, request, Response
from werkzeug.utils import secure_filename
import string
import random
import assist

core = Blueprint('core', __name__)


@core.route('/upload/<folder>', methods=['POST'])
def upload_file(folder):
    """
    Uploads a file to the given folder. If a file with the same file name exists, it moves the existing one to the
    archive folder.
    """
    if not assist.check_token(request):
        print('Auth error')
        return 'Auth error', 401
    if not assist.allowed_folder(folder):
        print('Bad folder')
        return 'Bad folder', 400
    # check if the post request has the file part
    if 'file' not in request.files:
        print('No file part')
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        print('Missing filename')
        return 'Missing filename', 400
    if not assist.allowed_file(file.filename):
        print('Bad filename')
        return 'Bad filename', 400
    if file:
        filename = secure_filename(file.filename)
        target_path = os.path.join(assist.UPLOAD_FOLDER, folder, filename)
        # if file already exists, move the existing file to the archive folder
        if os.path.isfile(target_path):
            assist.move_to_archive(folder, filename)
        file.save(target_path)
        return 'Upload successful', 201


@core.route('/upload/json', methods=['POST'])
def upload_json():
    """
    Uploads a json file
    """
    if not assist.check_token(request):
        print('Auth error')
        return 'Auth error', 401

    # check if the post request has required data
    if 'json' not in request.form:
        print('No json part')
        return 'No json part', 400
    if 'username' not in request.form:
        print('No username part')
        return 'No username part', 400

    json = request.form['json']
    username = request.form['username']

    target_path = os.path.join(
        assist.UPLOAD_FOLDER, 'json', username + '.json')

    f = open(target_path, "w")
    f.write(json)
    f.close()

    return 'json successful', 201


@core.route('/testdownload', methods=['GET'])
def testdownload():
    return send_from_directory('PEBRAcloud_files/passwords', 'maria.txt')


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@core.route('/testrandom', methods=['GET'])
def testrandom():
    return id_generator()


@core.route('/download/<folder>/<username>/<random>', methods=['GET'])
def download(folder, username, random):
    """
    Downloads the file with matching username from the given folder.

    if not check_token(request):
        print('Auth error')
        return 'Auth error', 401
    """
    if not assist.allowed_folder(folder):
        print('Bad folder')
        return 'Bad folder', 400
    path = os.path.join(assist.UPLOAD_FOLDER, folder)

    filename = None
    for file in os.listdir(path):
        if file.startswith(username):
            filename = file
            break
    if not filename:
        print('Unknown user')
        return 'Unknown user', 400
    # print("sending path:" + path +  ", filename:" + filename)
    # return "sending path:" + path +  ", filename:" + filename, 401
    return send_from_directory(path, filename)


@core.route('/exists/<folder>/<username>', methods=['GET'])
def exists(folder, username):
    """
    Checks if a file for the given username exists in the given folder.
    """
    if not assist.check_token(request):
        print('Auth error')
        return 'Auth error', 401
    if not assist.allowed_folder(folder):
        print('Bad folder')
        return 'Bad folder', 400
    path = os.path.join(assist.UPLOAD_FOLDER, folder)
    filename = None
    for file in os.listdir(path):
        if file.startswith(username):
            filename = file
            break
    if not filename:
        resp = Response(json.dumps({'exists': False}))
        resp.headers['Content-Type'] = 'application/json'
        return resp
    resp = Response(json.dumps({'exists': True}))
    resp.headers['Content-Type'] = 'application/json'
    return resp



@core.route('/archive/<folder>/<username>', methods=['POST'])
def archive_file(folder, username):
    """
    Moves the file matching the given username to the archive folder.
    """
    if not assist.check_token(request):
        print('Auth error')
        return 'Auth error', 401
    if not assist.allowed_folder(folder):
        print('Bad folder')
        return 'Bad folder', 400
    path = os.path.join(assist.UPLOAD_FOLDER, folder)
    filename = None
    for file in os.listdir(path):
        if file.startswith(username):
            filename = file
            break
    if not filename:
        print('File not found')
        return 'File not found', 400
    assist.move_to_archive(folder, filename)
    return 'Archive successful', 201


