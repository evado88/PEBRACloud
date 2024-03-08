# App: Twyshe Server
# Date: August 2023
# Author: Nkole Evans

from flask import Flask, send_from_directory, request, Response
from werkzeug.utils import secure_filename
import assist

#link database and api files
from core import core
from mapi import mapi
from db import db

from mlist import mlist
from mdelete import mdelete
from mupdate import mupdate

#init flask app
app = Flask(__name__)

#register blueprints
app.register_blueprint(core)
app.register_blueprint(mapi)
app.register_blueprint(db)

app.register_blueprint(mlist)
app.register_blueprint(mdelete)
app.register_blueprint(mupdate)

#root path
@app.route("/")
def hello():
    return {'app':'Twyshe App Server', 'version': 3}