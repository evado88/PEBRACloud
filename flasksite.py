# App: Twyshe Server
# Date: August 2023
# Author: Nkole Evans

from flask import Flask, send_from_directory, request, Response
from werkzeug.utils import secure_filename
import assist

#link database and api files
from api import api
from db import db

#init flask app
app = Flask(__name__)

#register blueprints
app.register_blueprint(api)
app.register_blueprint(db)


#root path
@app.route("/")
def hello():
    return {'app':'Twyshe App Server', 'version': 1}