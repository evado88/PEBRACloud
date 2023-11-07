import json
import sqlite3
from flask import Blueprint, Response, request
import assist
import datetime as dt

mupdate = Blueprint('mupdate', __name__)

def getItemId(title, id):

    con = sqlite3.connect(assist.DB_NAME)
    cur = con.cursor()

    if title == 'user':
        query = "SELECT *, CASE WHEN user_status=1 THEN 'Active' ELSE 'Disabled' END AS u_status FROM app_users WHERE user_id=?"
    elif title=='facility':
        query = "SELECT *, CASE WHEN facility_status=1 THEN 'Active' ELSE 'Disabled' END AS f_status FROM app_facilities WHERE facility_id=?"
    elif title=='resource':
        query = "SELECT *, CASE WHEN resource_status=1 THEN 'Active' ELSE 'Disabled' END AS r_status FROM app_resources WHERE resource_id=?"
    elif title=='country':
        query = "SELECT *, CASE WHEN country_status=1 THEN 'Active' ELSE 'Disabled' END AS c_status FROM app_countries WHERE country_id=?"
    elif title=='color':
        query = "SELECT *, CASE WHEN color_status=1 THEN 'Active' ELSE 'Disabled' END AS c_status FROM app_colors WHERE color_id=?"
    elif title=='notification':
        query = "SELECT * FROM app_notifications WHERE notification_id=?"
    elif title=='login':
        query = "SELECT * FROM app_logins WHERE login_id=?"
    elif title=='audit':
        query = "SELECT * FROM app_audits WHERE audit_id=?"
    elif title=='log':
        query = "SELECT * FROM app_logs WHERE log_id=?"
    else:
        return {'succeeded': False, 'items': [], 'message': f"The specified {title} is not valid"}

    res = cur.execute(query, [id])

    rows = res.fetchall()

    if len(rows) == 0:
        rs = {'succeeded': False, 'items': [], 'message': f"The specified {title} '{id}' could not be found"}
    else:
        columns = list(map(lambda x: x[0], cur.description))
        items = assist.getList(rows, columns)
        rs = {'succeeded': True, 'items': items, 'message': None}

    con.close()
    return rs

@mupdate.route('/user/id/<id>', methods=['GET'])
def userId(id):

   rs = getItemId('user', id)

   resp = Response(json.dumps(rs))

   resp.headers['Content-Type'] = 'application/json'
   resp.headers['Access-Control-Allow-Origin'] = '*'

   return resp

@mupdate.route('/peer-navigator/id/<id>', methods=['GET'])
def peerNavigatorId(id):

   rs = getItemId('peer navigator', id)

   resp = Response(json.dumps(rs))

   resp.headers['Content-Type'] = 'application/json'
   resp.headers['Access-Control-Allow-Origin'] = '*'

   return resp

@mupdate.route('/participant/id/<id>', methods=['GET'])
def participantId(id):

   rs = getItemId('participant', id)

   resp = Response(json.dumps(rs))

   resp.headers['Content-Type'] = 'application/json'
   resp.headers['Access-Control-Allow-Origin'] = '*'

   return resp

@mupdate.route('/followup/id/<id>', methods=['GET'])
def followupId(id):

   rs = getItemId('followup', id)

   resp = Response(json.dumps(rs))

   resp.headers['Content-Type'] = 'application/json'
   resp.headers['Access-Control-Allow-Origin'] = '*'

   return resp

@mupdate.route('/analytic/id/<id>', methods=['GET'])
def analyticId(id):

   rs = getItemId('color', id)

   resp = Response(json.dumps(rs))

   resp.headers['Content-Type'] = 'application/json'
   resp.headers['Access-Control-Allow-Origin'] = '*'

   return resp

@mupdate.route('/facility/id/<id>', methods=['GET'])
def facilityId(id):

   rs = getItemId('facility', id)

   resp = Response(json.dumps(rs))

   resp.headers['Content-Type'] = 'application/json'
   resp.headers['Access-Control-Allow-Origin'] = '*'

   return resp

@mupdate.route('/resource/id/<id>', methods=['GET'])
def resourceId(id):

   rs = getItemId('resource', id)

   resp = Response(json.dumps(rs))

   resp.headers['Content-Type'] = 'application/json'
   resp.headers['Access-Control-Allow-Origin'] = '*'

   return resp

@mupdate.route('/country/id/<id>', methods=['GET'])
def countryId(id):

   rs = getItemId('country', id)

   resp = Response(json.dumps(rs))

   resp.headers['Content-Type'] = 'application/json'
   resp.headers['Access-Control-Allow-Origin'] = '*'

   return resp

@mupdate.route('/color/id/<id>', methods=['GET'])
def colorId(id):

   rs = getItemId('color', id)

   resp = Response(json.dumps(rs))

   resp.headers['Content-Type'] = 'application/json'
   resp.headers['Access-Control-Allow-Origin'] = '*'

   return resp

@mupdate.route('/notification/id/<id>', methods=['GET'])
def notificationId(id):

   rs = getItemId('notification', id)

   resp = Response(json.dumps(rs))

   resp.headers['Content-Type'] = 'application/json'
   resp.headers['Access-Control-Allow-Origin'] = '*'

   return resp

@mupdate.route('/user/update', methods=['POST'])
def updateUser():

    uname = request.form.get('uname')
    ufname = request.form.get('ufname')
    ulname = request.form.get('ulname')
    uphone = request.form.get('uphone')
    uemail = request.form.get('uemail')
    urole = request.form.get('urole')
    ustatus = request.form.get('ustatus')
    uid = request.form.get('uid')
    user = request.form.get('user')
    
    con = sqlite3.connect(assist.DB_NAME)

    cur = con.cursor()

    nw  = dt.datetime.now();
    now = nw.strftime('%Y-%m-%d %H:%M:%S')

    if int(uid) == 0:
        #add a new user
        query = '''INSERT INTO app_users(user_username, user_fname, user_lname, user_phone,
                   user_email, user_role, user_status, 
                   user_createuser, user_createdate, user_lastupdatedate, user_lastupdateuser) 
                   VALUES (?, ?, ?, ?,
                           ?, ?, ?,
                           ?, ?, ?, ?)'''
        cur.execute(query, [uname, ufname, ulname, uphone, 
                            uemail, urole, ustatus, 
                            user, now, now, user])

        #set id of inserted record
        uid = cur.lastrowid
    else:
        #update the user
        query = '''UPDATE app_users SET user_fname=?, user_lname=?, user_phone=?,
                   user_email=?, user_role=?, user_status=?, 
                   user_lastupdatedate=?, user_lastupdateuser=? WHERE user_id=?'''
        
        cur.execute(query, [ufname, ulname, uphone, 
                            uemail, urole, ustatus, 
                            now, user, uid])

    rows = cur.rowcount

    con.commit()
    con.close()

    if rows != 0:
        rs = getItemId('user', uid)
    else:
        rs = {'succeeded': False, 'items': None, 'message': f'Unable to update the specified record'}
        
    resp = Response(json.dumps(rs))

    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp

@mupdate.route('/peer-navigator/update', methods=['POST'])
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
        rs = getItemId('peer navigator', uid)
    else:
        rs = {'succeeded': False, 'items': None, 'message': f'Unable to update the specified record'}
        
    resp = Response(json.dumps(rs))

    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp

@mupdate.route('/facility/update', methods=['POST'])
def updateFacility():

    uname = request.form.get('uname')
    uaddress = request.form.get('uaddress')
    utollfree = request.form.get('utollfree')
    uwhatsapp = request.form.get('uwhatsapp')
    uemail = request.form.get('uemail')
    uwebsite = request.form.get('uwebsite')
    uphone = request.form.get('uphone')

    ucontraception = request.form.get('ucontraception')
    uprep= request.form.get('uprep')
    uabortion= request.form.get('uabortion')
    umenstrual = request.form.get('umenstrual')
    ustis = request.form.get('usti')
    uart = request.form.get('uart')

    ulat = request.form.get('ulat')
    ulon = request.form.get('ulon')

    uthumbnail = request.form.get('uthumbnail')

    ustatus = request.form.get('ustatus')

    uid = request.form.get('uid')
    user = request.form.get('user')
    
    con = sqlite3.connect(assist.DB_NAME)

    cur = con.cursor()

    nw  = dt.datetime.now();
    now = nw.strftime('%Y-%m-%d %H:%M:%S')

    

    if int(uid) == 0:
        #add a new facility
        query = '''INSERT INTO  app_facilities (facility_name, facility_address, facility_tollfree, facility_whatsapp,
                   facility_email, facility_website, facility_phone,
                   facility_contraception, facility_prep, facility_abortion, facility_menstrual, facility_sti, facility_art,
                   facility_lat, facility_lon, facility_thumbnailUrl, facility_status, 
                   facility_createuser, facility_createdate, facility_lastupdatedate, facility_lastupdateuser) 
                   VALUES (?, ?, ?, ?,
                           ?, ?, ?, 
                           ?, ?, ?, ?, ?, ?,
                           ?, ?, ?, ?,
                           ?, ?, ?, ?)'''
        cur.execute(query, [uname, uaddress, utollfree, uwhatsapp,
                            uemail, uwebsite, uphone,
                            ucontraception, uprep, uabortion, umenstrual, ustis, uart,  
                            ulat, ulon, uthumbnail, ustatus, 
                            user, now, now, user])

        #set id of inserted record
        uid = cur.lastrowid
    else:
        #update the facility
        query = '''UPDATE  app_facilities SET facility_name=?, facility_address=?, facility_tollfree=?, facility_whatsapp=?,
                   facility_email=?, facility_website=?, facility_phone=?,
                   facility_contraception=?, facility_prep=?, facility_abortion=?, facility_menstrual=?, facility_sti=?, facility_art=?,
                   facility_lat=?, facility_lon=?, facility_thumbnailUrl=?, facility_status=?, 
                   facility_lastupdatedate=?, facility_lastupdateuser=? WHERE facility_id=?'''
        
        cur.execute(query, [uname, uaddress, utollfree, uwhatsapp,
                            uemail, uwebsite, uphone,
                            ucontraception, uprep, uabortion, umenstrual, ustis, uart,  
                            ulat, ulon, uthumbnail, ustatus, 
                            now, user, uid])

    rows = cur.rowcount

    con.commit()
    con.close()

    if rows != 0:
        rs = getItemId('facility', uid)
    else:
        rs = {'succeeded': False, 'items': None, 'message': f'Unable to update the specified record'}
        
    resp = Response(json.dumps(rs))

    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp


@mupdate.route('/resource/update', methods=['POST'])
def updateResource():

    uname = request.form.get('uname')
    udescription = request.form.get('udescription')
    uurl = request.form.get('uurl')
    uthumbnail = request.form.get('uthumbnail')
    ustatus = request.form.get('ustatus')
    uid = request.form.get('uid')
    user = request.form.get('user')
    
    con = sqlite3.connect(assist.DB_NAME)

    cur = con.cursor()

    nw  = dt.datetime.now();
    now = nw.strftime('%Y-%m-%d %H:%M:%S')

    

    if int(uid) == 0:
        #add a new resource
        query = '''INSERT INTO app_resources(resource_name, resource_description, 
                   resource_url, resource_thumbnailUrl, resource_status, 
                   resource_createuser, resource_createdate, resource_lastupdatedate, resource_lastupdateuser) 
                   VALUES (?, ?, 
                           ?, ?, ?, 
                           ?, ?, ?, ?)'''
        cur.execute(query, [uname, udescription, uurl, uthumbnail, ustatus, user, now, now, user])

        #set id of inserted record
        uid = cur.lastrowid
    else:
        #update the resource
        query = '''UPDATE app_resources SET resource_name=?, resource_description=?, 
                   resource_url=?, resource_thumbnailUrl=?, resource_status=?, 
                   resource_lastupdatedate=?, resource_lastupdateuser=? WHERE resource_id=?'''
        
        cur.execute(query, [uname, udescription, uurl, uthumbnail, ustatus, now, user, uid])

    rows = cur.rowcount

    con.commit()
    con.close()

    if rows != 0:
        rs = getItemId('resource', uid)
    else:
        rs = {'succeeded': False, 'items': None, 'message': f'Unable to update the specified record'}
        
    resp = Response(json.dumps(rs))

    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp

@mupdate.route('/country/update', methods=['POST'])
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
        #add a new country
        query = '''INSERT INTO app_countries (country_name, country_code, country_status, 
                   country_createuser, country_createdate, country_lastupdatedate, country_lastupdateuser) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)'''
        cur.execute(query, [uname, ucode, ustatus, user, now, now, user])

        #set id of inserted record
        uid = cur.lastrowid
    else:
        #update the country
        query = '''UPDATE app_countries SET country_name=?, country_code=?, country_status=?, country_lastupdatedate=?,
                   country_lastupdateuser=? WHERE country_id=?'''
        
        cur.execute(query, [uname, ucode, ustatus, now, user, uid])

    rows = cur.rowcount

    con.commit()
    con.close()

    if rows != 0:
        rs = getItemId('country', uid)
    else:
        rs = {'succeeded': False, 'items': None, 'message': f'Unable to update the specified record'}
        
    resp = Response(json.dumps(rs))

    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp

@mupdate.route('/color/update', methods=['POST'])
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
        rs = getItemId('color', uid)
    else:
        rs = {'succeeded': False, 'items': None, 'message': f'Unable to update the specified record'}
        
    resp = Response(json.dumps(rs))

    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp

@mupdate.route('/notification/update', methods=['POST'])
def updateNotification():

    utype = request.form.get('utype')
    utitle = request.form.get('utitle')
    ubody = request.form.get('ubody')
    udescription = request.form.get('udescription')
    uid = request.form.get('uid')
    user = request.form.get('user')
    
    con = sqlite3.connect(assist.DB_NAME)

    cur = con.cursor()

    nw  = dt.datetime.now();
    now = nw.strftime('%Y-%m-%d %H:%M:%S')

    
    if int(uid) == 0:
        #add a new country
        query = '''INSERT INTO app_notifications (notification_type, notification_title, notification_body, notification_description,
                   notification_createuser, notification_createdate, notification_lastupdatedate, notification_lastupdateuser) 
                   VALUES (?, ?, ?, ?, 
                           ?, ?, ?, ?)'''
        cur.execute(query, [utype, utitle, ubody, udescription,
                            user, now, now, user])

        #set id of inserted record
        uid = cur.lastrowid
    else:
        #update the country
        query = '''UPDATE app_notifications SET notification_type=?, notification_title=?, notification_body=?, notification_description=?,
                   notification_lastupdatedate=?, notification_lastupdateuser=? WHERE notification_id=?'''
        
        cur.execute(query, [utype, utitle, ubody, udescription, 
                            now, user, uid])

    rows = cur.rowcount

    con.commit()
    con.close()

    if rows != 0:
        rs = getItemId('notification', uid)
    else:
        rs = {'succeeded': False, 'items': None, 'message': f'Unable to update the specified record'}
        
    resp = Response(json.dumps(rs))

    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp

@mupdate.route('/login/update', methods=['POST'])
def updateLogin():

    uusername = request.form.get('uusername')
    usource = request.form.get('usource')
    uid = request.form.get('uid')
    
    con = sqlite3.connect(assist.DB_NAME)

    cur = con.cursor()

    nw  = dt.datetime.now();
    now = nw.strftime('%Y-%m-%d %H:%M:%S')

    if int(uid) == 0:
        #add a new color
        query = '''INSERT INTO app_logins(login_username, login_source, login_date) 
                   VALUES (?, ?, ?)'''
        cur.execute(query, [uusername, usource, now])

        #set id of inserted record
        uid = cur.lastrowid
    else:
        #update the color
        query = '''UPDATE app_logins SET login_username=?, login_source=?, login_date=? WHERE login_id=?'''
        
        cur.execute(query, [uusername, usource, now, uid])

    rows = cur.rowcount

    con.commit()
    con.close()

    if rows != 0:
        rs = getItemId('login', uid)
    else:
        rs = {'succeeded': False, 'items': None, 'message': f'Unable to update the specified record'}
        
    resp = Response(json.dumps(rs))

    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp

@mupdate.route('/audit/update', methods=['POST'])
def updateAudit():

    uusername = request.form.get('uusername')
    utitle = request.form.get('utitle')
    uaction = request.form.get('uaction')
    udescription = request.form.get('udescription')
    uid = request.form.get('uid')

    con = sqlite3.connect(assist.DB_NAME)

    cur = con.cursor()

    nw  = dt.datetime.now();
    now = nw.strftime('%Y-%m-%d %H:%M:%S')

    if int(uid) == 0:
        #add a new color
        query = '''INSERT INTO app_audits(audit_username, audit_title, audit_action, 
                                          audit_description, audit_date) 
                   VALUES (?, ?, ?, 
                           ?, ?)'''
        cur.execute(query, [uusername, utitle, uaction, 
                            udescription, now])

        #set id of inserted record
        uid = cur.lastrowid
    else:
        #update the color
        query = '''UPDATE app_audits SET audit_username=?, audit_title=?, audit_action=?, 
                   audit_description=?, audit_date=? WHERE audit_id=?'''
        
        cur.execute(query, [uusername, utitle, uaction, 
                            udescription, now, uid])

    rows = cur.rowcount

    con.commit()
    con.close()

    if rows != 0:
        rs = getItemId('audit', uid)
    else:
        rs = {'succeeded': False, 'items': None, 'message': f'Unable to update the specified record'}
        
    resp = Response(json.dumps(rs))

    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp

@mupdate.route('/log/update', methods=['POST'])
def updateLog():

    uusername = request.form.get('uusername')
    utitle = request.form.get('utitle')
    uaction = request.form.get('uaction')
    udescription = request.form.get('udescription')
    uexception = request.form.get('uexception')
    uid = request.form.get('uid')
    
    con = sqlite3.connect(assist.DB_NAME)

    cur = con.cursor()

    nw  = dt.datetime.now();
    now = nw.strftime('%Y-%m-%d %H:%M:%S')

    if int(uid) == 0:
        #add a new color
        query = '''INSERT INTO app_logs(log_username, log_title, log_action, 
                                        log_description, log_exception, log_date) 
                   VALUES (?, ?, ?, 
                           ?, ?, ?)'''
        cur.execute(query, [uusername, utitle, uaction, 
                            udescription, uexception, now])

        #set id of inserted record
        uid = cur.lastrowid
    else:
        #update the color
        query = '''UPDATE app_logs SET log_username=?, log_title=?, log_action=?, 
                   log_description=?, log_exception=?, log_date=? WHERE log_id=?'''
        
        cur.execute(query, [uusername, utitle, uaction, 
                            udescription, uexception, now, uid])

    rows = cur.rowcount

    con.commit()
    con.close()

    if rows != 0:
        rs = getItemId('log', uid)
    else:
        rs = {'succeeded': False, 'items': None, 'message': f'Unable to update the specified record'}
        
    resp = Response(json.dumps(rs))

    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp