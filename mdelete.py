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

@mdelete.route('/color/delete', methods=['POST'])
def deleteColor():

    uid = request.form.get('uid')
    query = '''DELETE FROM app_colors WHERE color_id=?'''
        
    return deleteItem('color', uid, query)