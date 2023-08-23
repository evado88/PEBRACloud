import os
import json
import sys
from flask import Flask, send_from_directory, request, Response
from werkzeug.utils import secure_filename
from time import localtime, strftime
import string
import random
import sqlite3

# default parameters, can be overwritten by command line arguments
PORT = 80
UPLOAD_FOLDER = '/home/nkoleevans/mysite/PEBRAcloud_files'

# fixed parameters
ALLOWED_EXTENSIONS = {'txt', 'db', 'xlsx'}
ALLOWED_FOLDERS = {'data', 'backups', 'passwords'}
ALLOWED_FEATURES = {'events', 'analytics', 'users','patients', 'followups', 'appointments', 'medicalRefils'}
# TODO: generate secure key, http://flask.pocoo.org/docs/quickstart/#sessions
SECRET_KEY = 'SECRET'
# TODO: generate secure auth token
AUTH_TOKEN = 'TOKEN'

dev_mode = "dev" in sys.argv
for arg in sys.argv:
    if arg.startswith('port='):
        PORT=int(arg[5:])
    if arg.startswith('files=') and arg[6:].strip():
        UPLOAD_FOLDER=arg[6:]
print("running in development mode" if dev_mode else "running in production mode")
print("running on port '%s'" % PORT)
print("storing files in '%s'" % UPLOAD_FOLDER)


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = SECRET_KEY
app.config['AUTH_TOKEN'] = AUTH_TOKEN


# create all folders
for folder in ALLOWED_FOLDERS:
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], folder), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'archive', '%s-archive' % folder), exist_ok=True)


def check_token(request):
    if 'token' not in request.headers:
        return False
    request_token = request.headers['token']
    return app.config['AUTH_TOKEN'] == request_token


def get_file_extension(filename):
    return filename.rsplit('.', 1)[1].lower()


def allowed_file(filename):
    return '.' in filename and get_file_extension(filename) in ALLOWED_EXTENSIONS


def allowed_folder(foldername):
    return foldername.lower() in ALLOWED_FOLDERS

def allowed_feature(feature):
    return feature in ALLOWED_FEATURES


def move_to_archive(folder, filename):
    """
    Moves the given file to the archive folder and adds a running number '_X' to it for versioning.
    """
    file_ext = get_file_extension(filename)
    filename_no_ext = filename[:-(len(file_ext) + 1)]
    file_version = 1
    source_path = os.path.join(app.config['UPLOAD_FOLDER'], folder, filename)
    archive_path = os.path.join(app.config['UPLOAD_FOLDER'], 'archive', '%s-archive' % folder,
                                '%s_%s.%s' % (filename_no_ext, file_version, file_ext))
    while os.path.isfile(archive_path):
        file_version += 1
        archive_path = os.path.join(app.config['UPLOAD_FOLDER'], 'archive', '%s-archive' % folder,
                                    '%s_%s.%s' % (filename_no_ext, file_version, file_ext))
    os.rename(source_path, archive_path)


@app.route('/upload/<folder>', methods=['POST'])
def upload_file(folder):
    """
    Uploads a file to the given folder. If a file with the same file name exists, it moves the existing one to the
    archive folder.
    """
    if not check_token(request):
        print('Auth error')
        return 'Auth error', 401
    if not allowed_folder(folder):
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
    if not allowed_file(file.filename):
        print('Bad filename')
        return 'Bad filename', 400
    if file:
        filename = secure_filename(file.filename)
        target_path = os.path.join(app.config['UPLOAD_FOLDER'], folder, filename)
        # if file already exists, move the existing file to the archive folder
        if os.path.isfile(target_path):
            move_to_archive(folder, filename)
        file.save(target_path)
        return 'Upload successful', 201

@app.route('/upload/json', methods=['POST'])
def upload_json():
    """
    Uploads a json file
    """
    if not check_token(request):
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

    target_path = os.path.join(app.config['UPLOAD_FOLDER'], 'json', username + '.json')

    f = open(target_path, "w")
    f.write(json)
    f.close()

    return 'json successful', 201

@app.route('/testdownload', methods=['GET'])
def testdownload():
    return send_from_directory('PEBRAcloud_files/passwords', 'maria.txt')

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@app.route('/testrandom', methods=['GET'])
def testrandom():
    return id_generator()

@app.route('/testsqlite', methods=['GET'])
def testsqlite():

    con = sqlite3.connect("tutorial.db")
    cur = con.cursor()

    """
    cur.execute("CREATE TABLE IF NOT EXISTS movie(title, year, score)")

    data = [
    ("Monty Python Live at the Hollywood Bowl", 1982, 7.9),
    ("Monty Python's The Meaning of Life", 1983, 7.5),
    ("Monty Python's Life of Brian", 1979, 8.0),
          ]
    cur.executemany("INSERT INTO movie VALUES(?, ?, ?)", data)
    con.commit()
    """

    res = cur.execute("SELECT title, score FROM movie")

    movies = res.fetchall()
    con.close()

    items = []

    if len(movies) > 0:

        id = 0;

        for mv in movies:

            id += 1

            items.append({'id': id, 'title':mv[0], 'score':mv[1]})

    else:
       print('No movies found')

    resp = Response(json.dumps(items))
    resp.headers['Content-Type'] = 'application/json'

    return resp

@app.route('/download/<folder>/<username>/<random>', methods=['GET'])
def download(folder, username, random):
    """
    Downloads the file with matching username from the given folder.

    if not check_token(request):
        print('Auth error')
        return 'Auth error', 401
    """
    if not allowed_folder(folder):
        print('Bad folder')
        return 'Bad folder', 400
    path = os.path.join(app.config['UPLOAD_FOLDER'], folder)

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


@app.route('/exists/<folder>/<username>', methods=['GET'])
def exists(folder, username):
    """
    Checks if a file for the given username exists in the given folder.
    """
    if not check_token(request):
        print('Auth error')
        return 'Auth error', 401
    if not allowed_folder(folder):
        print('Bad folder')
        return 'Bad folder', 400
    path = os.path.join(app.config['UPLOAD_FOLDER'], folder)
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


@app.route('/list-users', methods=['GET'])
def list_users():
    """
    Returns the username, first and last name of all users who have a backup.
    """
    if not check_token(request):
        print('Auth error')
        return 'Auth error', 401
    path = os.path.join(app.config['UPLOAD_FOLDER'], 'backups')
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

@app.route('/list-users-web', methods=['GET'])
def list_users_web():
    #Returns the username, first and last name of all users who have a backup.
    path = os.path.join(app.config['UPLOAD_FOLDER'], 'backups')
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

@app.route('/get-user-data/<feature>', methods=['GET'])
def get_user_data(feature):
    #json
    items = []

    if not allowed_feature(feature):
        data = {"succeeded": "true","message":"The specified feature '" + feature + "' is invalid", "items":items}
        resp = Response(json.dumps(data))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Content-Type'] = 'application/json'
        return resp, 400

    path = os.path.join(app.config['UPLOAD_FOLDER'], 'json')

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


@app.route('/archive/<folder>/<username>', methods=['POST'])
def archive_file(folder, username):
    """
    Moves the file matching the given username to the archive folder.
    """
    if not check_token(request):
        print('Auth error')
        return 'Auth error', 401
    if not allowed_folder(folder):
        print('Bad folder')
        return 'Bad folder', 400
    path = os.path.join(app.config['UPLOAD_FOLDER'], folder)
    filename = None
    for file in os.listdir(path):
        if file.startswith(username):
            filename = file
            break
    if not filename:
        print('File not found')
        return 'File not found', 400
    move_to_archive(folder, filename)
    return 'Archive successful', 201


@app.route('/', methods=['GET'])
def root():
    return "<h1>PEBRAcloud</h1>"

"""
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=dev_mode, use_reloader=dev_mode)
"""
