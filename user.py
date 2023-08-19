from flask import Blueprint, render_template, session,abort

user = Blueprint('user',__name__)

@user.route("/user")
def hello():
    d1 ={'name':'Martha', 'age':22}
    greet = "<h1>User File Loaded!</h1>"
    return d1