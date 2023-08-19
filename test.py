from flask import Blueprint, render_template, session,abort

test = Blueprint('test',__name__)

@test.route("/test")
def world():
    return "<h1>Test File!</h1>"