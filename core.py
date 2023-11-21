import os
import json
import sys
from flask import Flask, Blueprint, send_from_directory, request, Response
from werkzeug.utils import secure_filename
import string
import random
import assist
import sqlite3

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


def process_json_data(data, type):

    columns = ''
    placeHolder = ''

    values = []

    table = ''

    if type == 'users':
        table = 'app_peer_navigators'

    elif type == 'followups':
        table = 'app_followups'

    elif type == 'analytics':
        table = 'app_analytics'

    else:
        table = 'app_participants'

    for followup in data[type]:

        for field in followup:

            if field != 'id':
                if len(values) != 0:
                    columns += ','
                    placeHolder += ','

                columns += field
                placeHolder += '?'
                values.append(followup[field])

    query = f'INSERT INTO {table} ({columns}) VALUES ({placeHolder})'

    con = sqlite3.connect(assist.DB_NAME)
    cur = con.cursor()

    cur.execute(query, values)

    rows = cur.rowcount

    con.commit()
    con.close()

    if rows != 0:
        rs = {'succeeded': True, 'items': None,
              'message': f'The record has been successfully inserted'}
    else:
        rs = {'succeeded': False, 'items': None,
              'message': f'Unable to insert the specified record'}

    return rs


@core.route('/upload/json', methods=['POST'])
def upload_json():
    
    #Uploads a json file
    if not assist.check_token(request):
        rs = {'succeeded': False, 'items': None, 'message': 'The token has not been specified or is incorrect'}

        resp = Response(json.dumps(rs))
        resp.headers['Content-Type'] = 'application/json'
        resp.headers['Access-Control-Allow-Origin'] = '*'

        return resp

    # check if the post request has required data
    if 'json' not in request.form or 'username' not in request.form:
        rs = {'succeeded': False, 'items': None, 'message': 'The required parameters for the user or json data have not been provided'}

        resp = Response(json.dumps(rs))
        resp.headers['Content-Type'] = 'application/json'
        resp.headers['Access-Control-Allow-Origin'] = '*'

        return resp

    #get the parameters provided
    jsonData = request.form['json']
    username = request.form['username']

    #write the file to the file system
    target_path = os.path.join(
        assist.UPLOAD_FOLDER, 'json', username + '.json')

    f = open(target_path, "w")
    f.write(jsonData)
    f.close()

    #store the json data in the database
    data = json.loads(jsonData)

    items = ['patients', 'followups', 'users', 'analytics']
     
    rsFeature = None
    success = True

    for feature in items:
        rsFeature = process_json_data(data, feature)
        
        if not rsFeature['succeeded']:
           break
            
    if success:

        rs = {'succeeded': True, 'items': None, 'message': 'The JSON file has been uploaded and processed successfully'}

        resp = Response(json.dumps(rs))
        resp.headers['Content-Type'] = 'application/json'
        resp.headers['Access-Control-Allow-Origin'] = '*'

        return resp
    else:
        resp = Response(json.dumps(rsFeature))
        resp.headers['Content-Type'] = 'application/json'
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp 

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@core.route('/testrandom', methods=['GET'])
def testrandom():
    return id_generator()


@core.route('/download/<folder>/<username>/<random>', methods=['GET'])
def download(folder, username, random):

    # Downloads the file with matching username from the given folder.

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
