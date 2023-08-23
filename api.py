from flask import Blueprint, render_template, session,abort

api = Blueprint('api',__name__)

@api.route("/api")
def apif():
    return {'app':'API configuration file'}