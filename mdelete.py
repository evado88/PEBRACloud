import json
import sqlite3
from flask import Blueprint, Response, request
import assist

mdelete = Blueprint('mdelete', __name__)

def deleteItem(title, uid, query):

    con = sqlite3.connect(assist.DB_NAME)

    cur = con.cursor()

    cur.execute(query, [uid])

    rows = cur.rowcount

    con.commit()
    con.close()

    if rows != 0:
        rs = {'succeeded': True, 'items': None, 'message': f"The specified {title} with id '{uid}' has been successfully deleted"}
    else:
        rs = {'succeeded': False, 'items': None, 'message': f"Unable to delete the specified {title} with id '{uid}'"}
        
    resp = Response(json.dumps(rs))

    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp

@mdelete.route('/user/delete', methods=['POST'])
def deleteUser():

    uid = request.form.get('uid')
    query = '''DELETE FROM app_users WHERE user_id=?'''
        
    return deleteItem('user', uid, query)

@mdelete.route('/facility/delete', methods=['POST'])
def deleteFacility():

    uid = request.form.get('uid')
    query = '''DELETE FROM app_facilities WHERE facility_id=?'''
        
    return deleteItem('facility', uid, query)

@mdelete.route('/resource/delete', methods=['POST'])
def deleteResource():

    uid = request.form.get('uid')
    query = '''DELETE FROM app_resources WHERE resource_id=?'''
        
    return deleteItem('resource', uid, query)

@mdelete.route('/country/delete', methods=['POST'])
def deleteCountry():

    uid = request.form.get('uid')
    query = '''DELETE FROM app_countries WHERE country_id=?'''
        
    return deleteItem('country', uid, query)

@mdelete.route('/color/delete', methods=['POST'])
def deleteColor():

    uid = request.form.get('uid')
    query = '''DELETE FROM app_colors WHERE color_id=?'''
        
    return deleteItem('color', uid, query)

@mdelete.route('/notification/delete', methods=['POST'])
def deleteNotification():

    uid = request.form.get('uid')
    query = '''DELETE FROM app_notifications WHERE notification_id=?'''
        
    return deleteItem('notification', uid, query)