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
    return loadList('''SELECT *, CASE WHEN user_status=1 THEN 'Active' ELSE 'Disabled' END AS u_status FROM app_users''')

@mlist.route('/sent-resource/list', methods=['GET'])
def sentResourceList():

    return loadList("SELECT *, CASE WHEN status=1 THEN 'Pending' ELSE 'Processed' END AS p_status FROM app_sent_resources")

@mlist.route('/peer-upload/list', methods=['GET'])
def peerUploadList():

    return loadList("SELECT *, CASE WHEN upload_status=1 THEN 'Active' ELSE 'Disabled' END AS p_status FROM app_peer_uploads")

def getListWhere(type, id, field):

    if int(type) == 1:
        return 'WHERE status=1'
    elif int(type) == 2:
        return f"WHERE {field}='{id}' AND status=2"
    else:
        return ''

@mlist.route('/peer-navigator/list/<type>/<id>/<field>', methods=['GET'])
def peerList(type, id, field):

    return loadList(f"""SELECT pn.*, CASE WHEN status=1 THEN 'Active' ELSE 'Disabled' END AS p_status, 
                       IFNULL(t_seconds,0)/60 t_minutes, IFNULL(t_participants, 0) n_participants,
                       IFNULL(t_followups, 0) n_followups, IFNULL(t_analytics, 0) n_analytics,
                       up.upload_date
                       FROM app_peer_navigators pn 
                       LEFT JOIN (SELECT username, COUNT(*) t_participants 
                                  FROM app_participants WHERE status=1 GROUP BY username) p ON p.username=pn.username
                       LEFT JOIN (SELECT username, COUNT(*) t_followups
                                  FROM app_followups WHERE status=1 GROUP BY username) f ON f.username=pn.username
                       LEFT JOIN (SELECT username, COUNT(*) t_analytics, SUM(duration) t_seconds
                                  FROM app_analytics GROUP BY username) a ON a.username=pn.username
                       LEFT JOIN app_peer_uploads up ON pn.upload=up.upload_id {getListWhere(type, id, 'username')}
                       ORDER BY upload_date DESC""")

@mlist.route('/participant/list/<type>/<id>/<field>', methods=['GET'])
def participantList(type, id, field):

    return loadList(f"""SELECT *, CASE WHEN status=1 THEN 'Active' ELSE 'Disabled' END AS p_status FROM app_participants ps 
                        LEFT JOIN app_peer_uploads up ON ps.upload=up.upload_id {getListWhere(type, id, 'na')}
                        ORDER BY upload_date DESC""")

@mlist.route('/followup/list/<type>/<id>/<field>', methods=['GET'])
def followupList(type, id, field):

    return loadList(f"""SELECT *, CASE WHEN status=1 THEN 'Active' ELSE 'Disabled' END AS f_status FROM app_followups fu 
                        LEFT JOIN app_peer_uploads up ON fu.upload=up.upload_id {getListWhere(type, id, 'na')}
                        ORDER BY upload_date DESC""")

@mlist.route('/analytic/list', methods=['GET'])
def analyticList():

    return loadList("""SELECT * FROM app_analytics al
                       LEFT JOIN app_peer_uploads up ON al.upload=up.upload_id
                       ORDER BY created_date DESC""")


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

@mlist.route('/phone/list', methods=['GET'])
def phoneList():

    return loadList("""SELECT *, IFNULL(t_participants , 0) n_participants,
                    CASE 
                    WHEN phone_status=1 THEN 'Public' 
                    WHEN phone_status=2 THEN 'Peer Navigator'
                    WHEN phone_status=3 THEN 'Participant'
                    ELSE 'Unknown' 
                    END AS p_status 
                    FROM app_phones pr
                    LEFT JOIN (SELECT part_peer, COUNT(*) t_participants 
                    FROM app_peer_participants GROUP BY part_peer) ps
                    ON pr.phone_number=ps.part_peer
                    ORDER BY phone_id DESC""")

@mlist.route('/phone-participant/list', methods=['GET'])
def phoneParticipantList():

    return loadList("""SELECT *
                    FROM app_phones WHERE phone_status=3
                    ORDER BY phone_number""")

@mlist.route('/handshake/list', methods=['GET'])
def handshakeList():

    return loadList("SELECT * FROM app_handshakes ORDER BY shake_id DESC")