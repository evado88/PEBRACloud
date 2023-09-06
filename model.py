import json
import sqlite3
from flask import Blueprint, Response, request
import assist
import datetime as dt

model = Blueprint('model', __name__)

@model.route('/color/id/<id>', methods=['GET'])
def colorId(id):

    rs =  getColorId(id)

    resp = Response(json.dumps(rs))
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp

def getColorId(id):

    con = sqlite3.connect(assist.DB_NAME)
    cur = con.cursor()

    res = cur.execute("SELECT *, CASE WHEN color_status=1 THEN 'Active' ELSE 'Disabled' END AS c_status FROM app_colors WHERE color_id=?", [id])

    rows = res.fetchall()

    if len(rows) == 0:
        rs = {'succeeded': False, 'items': [], 'message': f"The specified color '{id}' could not be found"}
    else:
        columns = list(map(lambda x: x[0], cur.description))
        items = assist.getList(rows, columns)
        rs = {'succeeded': True, 'items': items, 'message': None}

    con.close()
    return rs


@model.route('/user/update', methods=['POST'])
def updateUser():

    uname = request.form.get('uname')
    ucode = request.form.get('ucode')
    ustatus = request.form.get('ustatus')
    uid = request.form.get('uid')
    user = request.form.get('user')
    
    con = sqlite3.connect(assist.DB_NAME)

    cur = con.cursor()

    nw  = dt.datetime.now();
    now = nw.strftime('%Y-%m-%d %H:%M:%S')

    

    if int(uid) == 0:
        #add a new color
        query = '''INSERT INTO app_colors(color_name, color_code, color_status, 
                   color_createuser, color_createdate, color_lastupdatedate, color_lastupdateuser) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)'''
        cur.execute(query, [uname, ucode, ustatus, user, now, now, user])

        #set id of inserted record
        uid = cur.lastrowid
    else:
        #update the color
        query = '''UPDATE app_colors SET color_name=?, color_code=?, color_status=?, color_lastupdatedate=?,
                   color_lastupdateuser=? WHERE color_id=?'''
        
        cur.execute(query, [uname, ucode, ustatus, now, user, uid])

    rows = cur.rowcount

    con.commit()
    con.close()

    if rows != 0:
        rs = getColorId(uid)
    else:
        rs = {'succeeded': False, 'items': None, 'message': f'Unable to update the specified record'}
        
    resp = Response(json.dumps(rs))

    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp

@model.route('/peer-navigator/update', methods=['POST'])
def updatePeerNavigator():

    uname = request.form.get('uname')
    ucode = request.form.get('ucode')
    ustatus = request.form.get('ustatus')
    uid = request.form.get('uid')
    user = request.form.get('user')
    
    con = sqlite3.connect(assist.DB_NAME)

    cur = con.cursor()

    nw  = dt.datetime.now();
    now = nw.strftime('%Y-%m-%d %H:%M:%S')

    

    if int(uid) == 0:
        #add a new color
        query = '''INSERT INTO app_colors(color_name, color_code, color_status, 
                   color_createuser, color_createdate, color_lastupdatedate, color_lastupdateuser) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)'''
        cur.execute(query, [uname, ucode, ustatus, user, now, now, user])

        #set id of inserted record
        uid = cur.lastrowid
    else:
        #update the color
        query = '''UPDATE app_colors SET color_name=?, color_code=?, color_status=?, color_lastupdatedate=?,
                   color_lastupdateuser=? WHERE color_id=?'''
        
        cur.execute(query, [uname, ucode, ustatus, now, user, uid])

    rows = cur.rowcount

    con.commit()
    con.close()

    if rows != 0:
        rs = getColorId(uid)
    else:
        rs = {'succeeded': False, 'items': None, 'message': f'Unable to update the specified record'}
        
    resp = Response(json.dumps(rs))

    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp

@model.route('/facility/update', methods=['POST'])
def updateFacility():

    uname = request.form.get('uname')
    ucode = request.form.get('ucode')
    ustatus = request.form.get('ustatus')
    uid = request.form.get('uid')
    user = request.form.get('user')
    
    con = sqlite3.connect(assist.DB_NAME)

    cur = con.cursor()

    nw  = dt.datetime.now();
    now = nw.strftime('%Y-%m-%d %H:%M:%S')

    

    if int(uid) == 0:
        #add a new color
        query = '''INSERT INTO app_colors(color_name, color_code, color_status, 
                   color_createuser, color_createdate, color_lastupdatedate, color_lastupdateuser) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)'''
        cur.execute(query, [uname, ucode, ustatus, user, now, now, user])

        #set id of inserted record
        uid = cur.lastrowid
    else:
        #update the color
        query = '''UPDATE app_colors SET color_name=?, color_code=?, color_status=?, color_lastupdatedate=?,
                   color_lastupdateuser=? WHERE color_id=?'''
        
        cur.execute(query, [uname, ucode, ustatus, now, user, uid])

    rows = cur.rowcount

    con.commit()
    con.close()

    if rows != 0:
        rs = getColorId(uid)
    else:
        rs = {'succeeded': False, 'items': None, 'message': f'Unable to update the specified record'}
        
    resp = Response(json.dumps(rs))

    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp

@model.route('/resource/update', methods=['POST'])
def updateResource():

    uname = request.form.get('uname')
    ucode = request.form.get('ucode')
    ustatus = request.form.get('ustatus')
    uid = request.form.get('uid')
    user = request.form.get('user')
    
    con = sqlite3.connect(assist.DB_NAME)

    cur = con.cursor()

    nw  = dt.datetime.now();
    now = nw.strftime('%Y-%m-%d %H:%M:%S')

    

    if int(uid) == 0:
        #add a new color
        query = '''INSERT INTO app_colors(color_name, color_code, color_status, 
                   color_createuser, color_createdate, color_lastupdatedate, color_lastupdateuser) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)'''
        cur.execute(query, [uname, ucode, ustatus, user, now, now, user])

        #set id of inserted record
        uid = cur.lastrowid
    else:
        #update the color
        query = '''UPDATE app_colors SET color_name=?, color_code=?, color_status=?, color_lastupdatedate=?,
                   color_lastupdateuser=? WHERE color_id=?'''
        
        cur.execute(query, [uname, ucode, ustatus, now, user, uid])

    rows = cur.rowcount

    con.commit()
    con.close()

    if rows != 0:
        rs = getColorId(uid)
    else:
        rs = {'succeeded': False, 'items': None, 'message': f'Unable to update the specified record'}
        
    resp = Response(json.dumps(rs))

    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp

@model.route('/country/update', methods=['POST'])
def updateCountry():

    uname = request.form.get('uname')
    ucode = request.form.get('ucode')
    ustatus = request.form.get('ustatus')
    uid = request.form.get('uid')
    user = request.form.get('user')
    
    con = sqlite3.connect(assist.DB_NAME)

    cur = con.cursor()

    nw  = dt.datetime.now();
    now = nw.strftime('%Y-%m-%d %H:%M:%S')

    

    if int(uid) == 0:
        #add a new color
        query = '''INSERT INTO app_colors(color_name, color_code, color_status, 
                   color_createuser, color_createdate, color_lastupdatedate, color_lastupdateuser) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)'''
        cur.execute(query, [uname, ucode, ustatus, user, now, now, user])

        #set id of inserted record
        uid = cur.lastrowid
    else:
        #update the color
        query = '''UPDATE app_colors SET color_name=?, color_code=?, color_status=?, color_lastupdatedate=?,
                   color_lastupdateuser=? WHERE color_id=?'''
        
        cur.execute(query, [uname, ucode, ustatus, now, user, uid])

    rows = cur.rowcount

    con.commit()
    con.close()

    if rows != 0:
        rs = getColorId(uid)
    else:
        rs = {'succeeded': False, 'items': None, 'message': f'Unable to update the specified record'}
        
    resp = Response(json.dumps(rs))

    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp

@model.route('/color/update', methods=['POST'])
def updateColor():

    uname = request.form.get('uname')
    ucode = request.form.get('ucode')
    ustatus = request.form.get('ustatus')
    uid = request.form.get('uid')
    user = request.form.get('user')
    
    con = sqlite3.connect(assist.DB_NAME)

    cur = con.cursor()

    nw  = dt.datetime.now();
    now = nw.strftime('%Y-%m-%d %H:%M:%S')

    

    if int(uid) == 0:
        #add a new color
        query = '''INSERT INTO app_colors(color_name, color_code, color_status, 
                   color_createuser, color_createdate, color_lastupdatedate, color_lastupdateuser) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)'''
        cur.execute(query, [uname, ucode, ustatus, user, now, now, user])

        #set id of inserted record
        uid = cur.lastrowid
    else:
        #update the color
        query = '''UPDATE app_colors SET color_name=?, color_code=?, color_status=?, color_lastupdatedate=?,
                   color_lastupdateuser=? WHERE color_id=?'''
        
        cur.execute(query, [uname, ucode, ustatus, now, user, uid])

    rows = cur.rowcount

    con.commit()
    con.close()

    if rows != 0:
        rs = getColorId(uid)
    else:
        rs = {'succeeded': False, 'items': None, 'message': f'Unable to update the specified record'}
        
    resp = Response(json.dumps(rs))

    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp

@model.route('/color/delete', methods=['POST'])
def deleteColor():

    uid = request.form.get('uid')

    con = sqlite3.connect(assist.DB_NAME)

    cur = con.cursor()

    #update the color
    query = '''DELETE FROM app_colors WHERE color_id=?'''
        
    cur.execute(query, [uid])

    rows = cur.rowcount

    con.commit()
    con.close()

    if rows != 0:
        rs = {'succeeded': True, 'items': None, 'message': f"The specified color with id '{uid}' has been successfully deleted"}
    else:
        rs = {'succeeded': False, 'items': None, 'message': f"Unable to delete the specified color with id '{uid}'"}
        
    resp = Response(json.dumps(rs))

    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp