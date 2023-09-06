import json
from flask import Blueprint, Response, request
import requests
import sqlite3
import assist

api = Blueprint('api', __name__)

@api.route('/login', methods=['POST'])
def loginUser():

    username = request.form.get('username')
    password = request.form.get('password')

    con = sqlite3.connect(assist.DB_NAME)
    cur = con.cursor()

    res = cur.execute(
        "SELECT *, CASE WHEN user_status=1 THEN 'Active' ELSE 'Disabled' END AS u_status FROM app_users WHERE user_username=? OR user_email=?", [username, username])

    rows = res.fetchall()

    rs = {}

    if len(rows) == 0:
        rs = {'succeeded': False, 'items': None,
              'message': f"The specified user '{username}' could not be found"}
    else:
        columns = list(map(lambda x: x[0], cur.description))
        items = assist.getList(rows, columns)

        if items[0]['user_password'] != assist.getMD5(password):
            rs = {'succeeded': False, 'items': items[0]['user_password'],
                  'message': f"The specified user '{username}' or password is incorrect"}
        else:
            rs = {'succeeded': True, 'items': items, 'message': None}

    con.close()

    resp = Response(json.dumps(rs))

    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp




@api.route('/send-fcm-device-message', methods=['POST'])
def sendFcmDeviceMessage():
    url = 'https://fcm.googleapis.com/fcm/send'

    token = request.form.get('token')
    title = request.form.get('title')
    body = request.form.get('body')

    headers = {'Content-type': 'application/json',
               'Authorization': 'key=AAAAzHFkGzo:APA91bEy37CQFjUFuctbKsA8Z0kjZNuWSgJBLe6JpEafRhwTEjZCxPbvcv8zhUc2yCO1fNjoybTubBE0UGRBkSkIdl7ePrYUcaIYC9Exb9mr-UIsGNlNaps1iJ9E--cOUHNq0tCX-f03'}

    data = {"to": token,
            "notification":
               {
                   "title": title,
                   "body": body
             }
           }

    response = requests.post(url, data=json.dumps(data), headers=headers)
    # wait for the response. it should not be higher
    # than keep alive time for TCP connection

    # render template or redirect to some url:
    # return redirect("some_url")
    resp = Response(response)

    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return response.text

@api.route('/send-fcm-topic-message', methods=['POST'])
def sendFcmTopicMessage():
    url = 'https://fcm.googleapis.com/fcm/send'

    topic = request.form.get('topic')
    title = request.form.get('title')
    body = request.form.get('body')

    headers = {'Content-type': 'application/json',
               'Authorization': 'key=AAAAzHFkGzo:APA91bEy37CQFjUFuctbKsA8Z0kjZNuWSgJBLe6JpEafRhwTEjZCxPbvcv8zhUc2yCO1fNjoybTubBE0UGRBkSkIdl7ePrYUcaIYC9Exb9mr-UIsGNlNaps1iJ9E--cOUHNq0tCX-f03'}

    data = {"condition": f"'{topic}' in topics",
            "notification":
               {
                   "title": title,
                   "body": body
             }
           }

    response = requests.post(url, data=json.dumps(data), headers=headers)
    # wait for the response. it should not be higher
    # than keep alive time for TCP connection

    # render template or redirect to some url:
    # return redirect("some_url")
    resp = Response(response)

    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return response.text

