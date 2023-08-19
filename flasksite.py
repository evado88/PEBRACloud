from flask import Flask

from test import test
from user import user

app = Flask(__name__)

app.register_blueprint(test)
app.register_blueprint(user)

@app.route("/")
def hello():
    return "<h1>Main File!</h1>"