import os
import json
import sys
from flask import Flask,Blueprint, send_from_directory, request, Response
from werkzeug.utils import secure_filename
from time import localtime, strftime
import string
import random
import sqlite3
import assist

api = Blueprint('api',__name__)

@api.route("/api")
def apif():
    return {'app':'API configuration file'}


@api.route('/upload/<folder>', methods=['POST'])
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

@api.route('/upload/json', methods=['POST'])
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

    target_path = os.path.join(assist.UPLOAD_FOLDER, 'json', username + '.json')

    f = open(target_path, "w")
    f.write(json)
    f.close()

    return 'json successful', 201

@api.route('/testdownload', methods=['GET'])
def testdownload():
    return send_from_directory('PEBRAcloud_files/passwords', 'maria.txt')

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@api.route('/testrandom', methods=['GET'])
def testrandom():
    return id_generator()


@api.route('/download/<folder>/<username>/<random>', methods=['GET'])
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
    #print("sending path:" + path +  ", filename:" + filename)
    #return "sending path:" + path +  ", filename:" + filename, 401
    return send_from_directory(path, filename)


@api.route('/exists/<folder>/<username>', methods=['GET'])
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


@api.route('/list-users', methods=['GET'])
def list_users():
    """
    Returns the username, first and last name of all users who have a backup.
    """
    if not assist.check_token(request):
        print('Auth error')
        return 'Auth error', 401
    path = os.path.join(assist.UPLOAD_FOLDER, 'backups')
    users = []
    for file in os.listdir(path):
        filepath = os.path.join(path, file)
        if os.path.isfile(filepath) and not file.startswith('.'):
            filename = file.split('.')[0]  # remove .pb extension
            split = filename.split('_')
            username = split[0]
            firstname = split[1]
            lastname = split[2]
            last_upload = os.path.getmtime(filepath)
            last_upload = localtime(last_upload)
            last_upload = strftime("%Y-%m-%dT%H:%M:%S%z", last_upload)
            users.append({
                'username': username,
                'firstname': firstname,
                'lastname': lastname,
                'file': id_generator(),
                'last_upload': last_upload
            })
    resp = Response(json.dumps(users))
    resp.headers['Content-Type'] = 'application/json'
    return resp

@api.route('/list-users-web', methods=['GET'])
def list_users_web():
    #Returns the username, first and last name of all users who have a backup.
    path = os.path.join(assist.UPLOAD_FOLDER, 'backups')
    users = []
    for file in os.listdir(path):
        filepath = os.path.join(path, file)
        if os.path.isfile(filepath) and not file.startswith('.'):
            filename = file.split('.')[0]  # remove .pb extension
            split = filename.split('_')
            username = split[0]
            firstname = split[1]
            lastname = split[2]
            last_upload = os.path.getmtime(filepath)
            last_upload = localtime(last_upload)
            last_upload = strftime("%Y-%m-%dT%H:%M:%S%z", last_upload)
            users.append({
                'username': username,
                'firstname': firstname,
                'lastname': lastname,
                'last_upload': last_upload,
                'datafile': id_generator(),
            })
    data = {"odata.metadata": "list-users-web", "value":users}
    resp = Response(json.dumps(data))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json'
    return resp

@api.route('/get-user-data/<feature>', methods=['GET'])
def get_user_data(feature):
    #json
    items = []

    if not assist.allowed_feature(feature):
        data = {"succeeded": "true","message":"The specified feature '" + feature + "' is invalid", "items":items}
        resp = Response(json.dumps(data))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Content-Type'] = 'application/json'
        return resp, 400

    path = os.path.join(assist.UPLOAD_FOLDER, 'json')

    itemId = 1
    for file in os.listdir(path):
        filepath = os.path.join(path, file)
        if os.path.isfile(filepath) and not file.startswith('.'):
            f = open(filepath, "r")
            userJson = json.loads(f.read())
            f.close()
            for item in userJson[feature]:
                item['itemId']=itemId
                items.append(item)
                itemId += 1
    data = {"succeeded": True,"message":"", "items":items}
    resp = Response(json.dumps(data))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json'
    return resp


@api.route('/archive/<folder>/<username>', methods=['POST'])
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