import os
import hashlib

DB_NAME = "twyshe20240409-1554.db"

# default parameters, can be overwritten by command line arguments
PORT = 80
#UPLOAD_FOLDER = 'C:\\Repo\\Python\\PEBRACloud\\appdata'
UPLOAD_FOLDER = '/home/nkoleevans/mysite/twyshe-files'

# fixed parameters
ALLOWED_EXTENSIONS = {'txt', 'db', 'xlsx'}
ALLOWED_FOLDERS = {'data', 'backups', 'passwords'}
ALLOWED_FEATURES = {'events', 'analytics', 'users',
                    'patients', 'followups', 'appointments', 'medicalRefils'}
# TODO: generate secure key, http://flask.pocoo.org/docs/quickstart/#sessions
SECRET_KEY = '80db2fc8b86d89ff7fe871b0481a35880ff9c5bf1acc1cd4686b04fd652fba59'
# TODO: generate secure auth token
AUTH_TOKEN = '64afba44c23870aae335b53498d1eda92b86a43a4376e4839f5759960d2c3016'

# create all folders
for folder in ALLOWED_FOLDERS:
    os.makedirs(os.path.join(UPLOAD_FOLDER, folder), exist_ok=True)
    os.makedirs(os.path.join(UPLOAD_FOLDER, 'archive',
                '%s-archive' % folder), exist_ok=True)


def getMD5(value):
    return hashlib.md5(value.encode('utf-8')).hexdigest()


def getList(rows, columns):
    items = []

    for row in rows:

        item = {}
        index = 0

        for col in columns:
            item[col] = row[index]
            index += 1

        items.append(item)
    return items


def check_token(request):
    if 'token' not in request.headers:
        return False
    request_token = request.headers['token']
    return AUTH_TOKEN == request_token


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
    source_path = os.path.join(UPLOAD_FOLDER, folder, filename)
    archive_path = os.path.join(UPLOAD_FOLDER, 'archive', '%s-archive' % folder,
                                '%s_%s.%s' % (filename_no_ext, file_version, file_ext))
    while os.path.isfile(archive_path):
        file_version += 1
        archive_path = os.path.join(UPLOAD_FOLDER, 'archive', '%s-archive' % folder,
                                    '%s_%s.%s' % (filename_no_ext, file_version, file_ext))
    os.rename(source_path, archive_path)
