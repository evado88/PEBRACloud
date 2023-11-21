import json
import sqlite3
from flask import Blueprint, Response
import assist

mlist = Blueprint('mlist', __name__)

def loadList(query):

    con = sqlite3.connect(assist.DB_NAME)
    cur = con.cursor()

    res = cur.execute(query)

    rows = res.fetchall()
    columns = list(map(lambda x: x[0], cur.description))

    items = assist.getList(rows, columns)
    con.close()

    rs = {'succeeded': True, 'items': items, 'message': None}

    resp = Response(json.dumps(rs))
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@mlist.route('/user/list', methods=['GET'])
def userList():
    return loadList("SELECT *, CASE WHEN user_status=1 THEN 'Active' ELSE 'Disabled' END AS u_status FROM app_users")


@mlist.route('/peer-navigator/list', methods=['GET'])
def peerList():

    return loadList("SELECT *, CASE WHEN status=1 THEN 'Active' ELSE 'Disabled' END AS p_status FROM app_peer_navigators")

@mlist.route('/participant/list', methods=['GET'])
def participantList():

    return loadList("SELECT *, CASE WHEN status=1 THEN 'Active' ELSE 'Disabled' END AS p_status FROM app_participants")

@mlist.route('/followup/list', methods=['GET'])
def followupList():

    return loadList("SELECT *, CASE WHEN status=1 THEN 'Active' ELSE 'Disabled' END AS f_status FROM app_followups")


@mlist.route('/analytic/list', methods=['GET'])
def analyticList():

    return loadList("SELECT * FROM app_analytics")


@mlist.route('/facility/list', methods=['GET'])
def facilityList():

    return loadList("SELECT *, CASE WHEN facility_status=1 THEN 'Active' ELSE 'Disabled' END AS f_status FROM app_facilities")

@mlist.route('/resource/list', methods=['GET'])
def resourceList():

    return loadList("SELECT *, CASE WHEN resource_status=1 THEN 'Active' ELSE 'Disabled' END AS r_status FROM app_resources")

@mlist.route('/country/list', methods=['GET'])
def countryList():

    return loadList("SELECT *, CASE WHEN country_status=1 THEN 'Active' ELSE 'Disabled' END AS c_status FROM app_countries")

@mlist.route('/color/list', methods=['GET'])
def colorList():

    return loadList("SELECT *, CASE WHEN color_status=1 THEN 'Active' ELSE 'Disabled' END AS c_status FROM app_colors")

@mlist.route('/notification/list', methods=['GET'])
def notificatioList():

    return loadList("SELECT * FROM app_notifications")

@mlist.route('/login/list', methods=['GET'])
def loginList():

    return loadList("SELECT * FROM app_logins ORDER BY login_id DESC")

@mlist.route('/audit/list', methods=['GET'])
def auditList():

    return loadList("SELECT * FROM app_audits ORDER BY audit_id DESC")

@mlist.route('/log/list', methods=['GET'])
def logList():

    return loadList("SELECT * FROM app_logs ORDER BY log_id DESC")