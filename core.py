import os
import json
import sys
from flask import Flask, Blueprint, send_from_directory, request, Response
from werkzeug.utils import secure_filename
import string
import random
import assist
import sqlite3
import datetime as dt
from time import localtime, strftime

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


def process_json_data(data, type, username, upload):

    #check which table to update
    table = ''

    if type == 'users':
        table = 'app_peer_navigators'

    elif type == 'followups':
        table = 'app_followups'

    elif type == 'analytics':
        table = 'app_analytics'

    else:
        table = 'app_participants'

    con = sqlite3.connect(assist.DB_NAME)
    cur = con.cursor()

    rs = None

    #loop through the list of items
    for item in data[type]:

        columns = ''
        placeHolder = ''

        values = []

        item['username']=username
        item['upload']=upload
        
        #analytics do not use parents or status
        if type != 'analytics':
            item['status']=1
            item['parent']=item['id']


            #mark the other items as old
            cur.execute(f"UPDATE {table} SET status=2 WHERE username=? AND status=1", [username])

        for field in item:

            if field != 'id':
                if len(values) != 0:
                    columns += ','
                    placeHolder += ','

                columns += field
                placeHolder += '?'
                values.append(item[field])

        query = f'INSERT INTO {table} ({columns}) VALUES ({placeHolder})'
        cur.execute(query, values)

        rows = cur.rowcount

        if rows != 0:
            rs = {'succeeded': True, 'items': None,
                    'message': f'The record has been successfully inserted'}
        else:
            rs = {'succeeded': False, 'items': None,
                    'message': f'Unable to insert the specified record'}
            break

    #close the database and return the result
    con.commit()
    con.close()

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

    con = sqlite3.connect(assist.DB_NAME)
    cur = con.cursor()

    #mark the other items as old
    cur.execute(f"UPDATE app_peer_uploads SET upload_status=2 WHERE upload_username=? AND upload_status=1", [username])
     
    #insert main uplaod for user
    nw  = dt.datetime.now();
    now = nw.strftime('%Y-%m-%d %H:%M:%S')

    #add a new user
    query = '''INSERT INTO app_peer_uploads(upload_username, upload_status, upload_date) 
               VALUES (?, ?, ?)'''
    
    cur.execute(query, [username, 1, now])

    #set id of inserted record
    upload_id = cur.lastrowid

    #stop using database
    con.commit()
    con.close()

    #process each feature in the json file
    for feature in items:
        if len(data[feature]) != 0:
           rsFeature = process_json_data(data, feature, username, upload_id)
        
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

@core.route('/list-users', methods=['GET'])
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

@core.route('/list-users-web', methods=['GET'])
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
    resp = Response(json.dumps(users))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json'
    return resp