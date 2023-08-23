from flask import Blueprint, render_template, session,abort

db = Blueprint('db',__name__)

@db.route("/db")
def dbf():
    return {'app':'Database configuration file'}