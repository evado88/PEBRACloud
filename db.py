import json
import sqlite3
from flask import Blueprint, Response, render_template, request, session, abort
import assist

db = Blueprint('db', __name__)


@db.route("/db")
def dbr():
    return {'app': 'Database configuration file'}


@db.route('/initialize-db', methods=['GET'])
def initializeDb():

    con = sqlite3.connect("twyshe.db")
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_users (
          user_id INTEGER PRIMARY KEY,
          user_username TEXT NOT NULL,
          user_fname TEXT,
          user_lname TEXT,
          user_phone TEXT,
          user_email TEXT,
          user_password TEXT,
          user_role INTEGER,
          user_thumbnailUrl,
          user_status INTEGER,
          user_createuser TEXT,
          user_createdate TEXT,
          user_lastupdatedate TEXT,
          user_lastupdateuser TEXT
        );
        """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_countries (
          country_id INTEGER PRIMARY KEY,
          country_name TEXT NOT NULL,
          country_code TEXT,
          country_thumbnailUrl TEXT,
          country_status INTEGER,
          country_createuser TEXT,
          country_createdate TEXT,
          country_lastupdatedate TEXT,
          country_lastupdateuser TEXT
        );
        """)


    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_resources (
          resource_id INTEGER PRIMARY KEY,
          resource_name TEXT NOT NULL,
          resource_description TEXT,
          resource_url TEXT,
          resource_thumbnailUrl TEXT,
          resource_status INTEGER,
          resource_createuser TEXT,
          resource_createdate TEXT,
          resource_lastupdatedate TEXT,
          resource_lastupdateuser TEXT
        );
        """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_colors (
          color_id INTEGER PRIMARY KEY,
          color_name TEXT NOT NULL,
          color_code,
          color_thumbnailUrl,
          color_status INTEGER,
          color_createuser TEXT,
          color_createdate TEXT,
          color_lastupdatedate TEXT,
          color_lastupdateuser TEXT
        );
        """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_facilities (
          facility_id INTEGER PRIMARY KEY,
          facility_name TEXT NOT NULL,
          facility_address TEXT,
          facility_tollfree TEXT,
          facility_whatsapp TEXT,
          facility_email TEXT,
          facility_website TEXT,
          facility_phone TEXT,
          facility_contraception BIT,
          facility_prep BIT,
          facility_abortion BIT,
          facility_menstrual BIT,
          facility_sti BIT,
          facility_art BIT,
          facility_lat REAL,
          facility_lon REAL,
          facility_thumbnailUrl,
          facility_status INTEGER,
          facility_createuser TEXT,
          facility_createdate TEXT,
          facility_lastupdatedate TEXT,
          facility_lastupdateuser TEXT
        );
        """)

    con.close()

    rs = {'succeeded': True, 'items': None,
          'message':'The database structure has been initialized'}

    resp = Response(json.dumps(rs))
    resp.headers['Content-Type'] = 'application/json'

    return resp


@db.route('/initialize-data', methods=['POST'])
def initializeData():

    con = sqlite3.connect("twyshe.db")
    cur = con.cursor()

    data = [
        ("admin", 'Evans', 'Nkole', 'nkoleevans@hotmail.com',
         '81dc9bdb52d04dc20036dbd8313ed055', 1, 1, 'admin', '2023-08-23', 'admin', '2023-08-23'),
        ("karen", 'Karen', 'Hampanda', 'karen.hampanda@cuanschutz.edu',
         '81dc9bdb52d04dc20036dbd8313ed055', 1, 1, 'admin', '2023-08-23', 'admin', '2023-08-23'),
        ("alain", 'Alain', 'Amstutz', 'alain.amstutz@unibas.ch',
         '81dc9bdb52d04dc20036dbd8313ed055', 1, 1, 'admin', '2023-08-23', 'admin', '2023-08-23'),
        ("madeleine", 'Madeleine', 'Sehrt', 'madeleine.sehrt@cuanschutz.edu',
         '81dc9bdb52d04dc20036dbd8313ed055', 1, 1, 'admin', '2023-08-23', 'admin', '2023-08-23'),
    ]

    cur.executemany("""INSERT INTO app_users (user_username, user_fname, user_lname, user_email,
                                              user_password, user_role, user_status, 
                                              user_createuser, user_createdate, user_lastupdatedate, user_lastupdateuser) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", data)

    con.commit()

    data = [
        ("Zambia", '+260',
         1, 'admin', '2023-08-23', 'admin', '2023-08-23'),
        ("United States", '+1',
         1, 'admin', '2023-08-23', 'admin', '2023-08-23'),
    ]

    cur.executemany("""INSERT INTO app_countries (country_name, country_code, country_status,
                    country_createuser, country_createdate, country_lastupdatedate, country_lastupdateuser) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)""", data)

    con.commit()


    data = [('PrEP FAQs', 'FAQs about prep', 'https://www.unaids.org/sites/default/files/media_asset/UNAIDS_JC2765_en.pdf',
             'https://images.squarespace-cdn.com/content/v1/5fb1d13439928464562b880e/1611720515025-WYDCGIY87FZJGQ2QZU10/PrEP+Medical+Group+West+Melbourne.jpg', 
             1, 'admin', '2023-08-23', 'admin', '2023-08-23'),
            ('Contraception FAQs', 'FAQs about contraception', 'https://apps.who.int/iris/bitstream/handle/10665/181468/9789241549158_eng.pdf',
             'https://images.news18.com/ibnlive/uploads/2023/03/4292134.jpg',
             1, 'admin', '2023-08-23', 'admin', '2023-08-23')]
        

    cur.executemany("""INSERT INTO app_resources (resource_name, resource_description, resource_url, 
                    resource_thumbnailUrl,
                    resource_status, resource_createuser, resource_createdate, resource_lastupdatedate, resource_lastupdateuser) 
                    VALUES (?, ?, ?, 
                            ?,
                            ?, ?, ?, ?, ?)""", data)

    con.commit()

    data = [('Marie Stopes International (MSI)', 'Plot 120 Kudu Road, Kabulonga, Lusaka', '5600', '+260762560733',
             'info@mariestopes.org.zm', 'https://www.msichoices.org/', '+260965005600',
             1, 0, 1, 1, 1, 0,
             29.44, 23.00,
             1, 'admin', '2023-08-23', 'admin', '2023-08-23'),
            ('Planned Parenthood Association of Zambia (PPAZ)', 'Corner of church road and Dushambe Road, Lusaka', None, None,
            'info@ppaz.org.zm', 'https://www.facebook.com/PPAZambia/', '+260211256182',
             1, 1, 1, 1, 1, 0,
             29.44, 23.00,
             1, 'admin', '2023-08-23', 'admin', '2023-08-23'),]

    cur.executemany("""INSERT INTO app_facilities (facility_name, facility_address, facility_tollfree, facility_whatsapp,
                    facility_email, facility_website, facility_phone,
                    facility_contraception, facility_prep,facility_abortion,facility_menstrual, facility_sti,  facility_art,
                    facility_lat, facility_lon,
                    facility_status, facility_createuser, facility_createdate, facility_lastupdatedate, facility_lastupdateuser) 
                    VALUES (?, ?, ?, ?, 
                            ?, ?, ?,
                            ?, ?, ?, ?, ?, ?,
                            ?, ?,
                            ?, ?, ?, ?, ?)""", data)

    con.commit()

    con.close()

    rs = {'succeeded': True, 'items': None,
          'The database data has been initialized': None}

    resp = Response(json.dumps(rs))
    resp.headers['Content-Type'] = 'application/json'

    return resp

@db.route('/initialize/<feature>', methods=['POST'])
def initialize(feature):

    con = sqlite3.connect("twyshe.db")
    cur = con.cursor()

    data = []
    rs ={}

    if feature == 'color':

        data = [("red", '#D32F2F', 1, 'admin', '2023-08-23', 'admin', '2023-08-23'),
                ("pink", '#C2185B', 1, 'admin', '2023-08-23', 'admin', '2023-08-23'),
                ("purple", '#7B1FA2', 1, 'admin', '2023-08-23', 'admin', '2023-08-23'), 
                ("indigo", '#303F9F', 1, 'admin', '2023-08-23', 'admin', '2023-08-23'), 
                ("blue", '#1976D2', 1, 'admin', '2023-08-23', 'admin', '2023-08-23'), 
                ("green", '#388E3C', 1, 'admin', '2023-08-23', 'admin', '2023-08-23'), 
                ("brown", '#388E3C', 1, 'admin', '2023-08-23', 'admin', '2023-08-23'),  ]
        
        cur.executemany("""INSERT INTO app_colors (color_name, color_code, color_status, 
                                              color_createuser, color_createdate, color_lastupdatedate, color_lastupdateuser) 
                    VALUES (?, ?, ?, 
                            ?, ?, ?, ?)""", data)
        
        con.commit()
        
        rs = {'succeeded': False, 'items': None, 'message': f"The data for '{feature}' has been initialized"}

    elif feature == 'resource':
        
        data = [('PrEP FAQs', 'FAQs about prep', 'https://www.unaids.org/sites/default/files/media_asset/UNAIDS_JC2765_en.pdf',
             'https://images.squarespace-cdn.com/content/v1/5fb1d13439928464562b880e/1611720515025-WYDCGIY87FZJGQ2QZU10/PrEP+Medical+Group+West+Melbourne.jpg', 
             1, 'admin', '2023-08-23', 'admin', '2023-08-23'),
            ('Contraception FAQs', 'FAQs about contraception', 'https://apps.who.int/iris/bitstream/handle/10665/181468/9789241549158_eng.pdf',
             'https://images.news18.com/ibnlive/uploads/2023/03/4292134.jpg',
             1, 'admin', '2023-08-23', 'admin', '2023-08-23')]
        

        cur.executemany("""INSERT INTO app_resources (resource_name, resource_description, resource_url, 
                    resource_thumbnailUrl,
                    resource_status, resource_createuser, resource_createdate, resource_lastupdatedate, resource_lastupdateuser) 
                    VALUES (?, ?, ?, 
                            ?,
                            ?, ?, ?, ?, ?)""", data)

        con.commit()

        rs = {'succeeded': False, 'items': None, 'message': f"The data for '{feature}' has been initialized"}

    elif feature == 'user':
        
        data = [
        ("admin", 'Evans', 'Nkole', 'nkoleevans@hotmail.com',
         '81dc9bdb52d04dc20036dbd8313ed055', 1, 1, 'admin', '2023-08-23', 'admin', '2023-08-23'),
        ("karen", 'Karen', 'Hampanda', 'karen.hampanda@cuanschutz.edu',
         '81dc9bdb52d04dc20036dbd8313ed055', 1, 1, 'admin', '2023-08-23', 'admin', '2023-08-23'),
        ("alain", 'Alain', 'Amstutz', 'alain.amstutz@unibas.ch',
         '81dc9bdb52d04dc20036dbd8313ed055', 1, 1, 'admin', '2023-08-23', 'admin', '2023-08-23'),
        ("madeleine", 'Madeleine', 'Sehrt', 'madeleine.sehrt@cuanschutz.edu',
         '81dc9bdb52d04dc20036dbd8313ed055', 1, 1, 'admin', '2023-08-23', 'admin', '2023-08-23'),]

        cur.executemany("""INSERT INTO app_users (user_username, user_fname, user_lname, user_email,
                                              user_password, user_role, user_status, 
                                              user_createuser, user_createdate, user_lastupdatedate, user_lastupdateuser) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", data)

        con.commit()

        rs = {'succeeded': False, 'items': None, 'message': f"The data for '{feature}' has been initialized"}

    elif feature == 'facility':
        
        data = [('Marie Stopes International (MSI)', 'Plot 120 Kudu Road, Kabulonga, Lusaka', '5600', '+260762560733',
             'info@mariestopes.org.zm', 'https://www.msichoices.org/', '+260965005600',
             1, 0, 1, 1, 1, 0,
             29.44, 23.00,
             1, 'admin', '2023-08-23', 'admin', '2023-08-23'),
            ('Planned Parenthood Association of Zambia (PPAZ)', 'Corner of church road and Dushambe Road, Lusaka', None, None,
            'info@ppaz.org.zm', 'https://www.facebook.com/PPAZambia/', '+260211256182',
             1, 1, 1, 1, 1, 0,
             29.44, 23.00,
             1, 'admin', '2023-08-23', 'admin', '2023-08-23'),]

        cur.executemany("""INSERT INTO app_facilities (facility_name, facility_address, facility_tollfree, facility_whatsapp,
                    facility_email, facility_website, facility_phone,
                    facility_contraception, facility_prep,facility_abortion,facility_menstrual, facility_sti,  facility_art,
                    facility_lat, facility_lon,
                    facility_status, facility_createuser, facility_createdate, facility_lastupdatedate, facility_lastupdateuser) 
                    VALUES (?, ?, ?, ?, 
                            ?, ?, ?,
                            ?, ?, ?, ?, ?, ?,
                            ?, ?,
                            ?, ?, ?, ?, ?)""", data)

        con.commit()

        rs = {'succeeded': False, 'items': None, 'message': f"The data for '{feature}' has been initialized"}

    elif feature == 'country':
        
        data = [
        ("Zambia", '+260',
         1, 'admin', '2023-08-23', 'admin', '2023-08-23'),
        ("United States", '+1',
         1, 'admin', '2023-08-23', 'admin', '2023-08-23'),]

        cur.executemany("""INSERT INTO app_countries (country_name, country_code, country_status,
                    country_createuser, country_createdate, country_lastupdatedate, country_lastupdateuser) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)""", data)

        con.commit()

        rs = {'succeeded': False, 'items': None, 'message': f"The data for '{feature}' has been initialized"}
            
    else:
       rs = {'succeeded': False, 'items': None, 'message': f"The specified feature '{feature}' is not valid"}


    con.close()

    resp = Response(json.dumps(rs))
    resp.headers['Content-Type'] = 'application/json'

    return resp


@db.route('/user/list', methods=['GET'])
def userList():

    con = sqlite3.connect("twyshe.db")
    cur = con.cursor()

    res = cur.execute("SELECT * FROM app_users")

    rows = res.fetchall()
    columns = list(map(lambda x: x[0], cur.description))

    items = assist.getList(rows, columns)
    con.close()

    rs = {'succeeded': True, 'items': items, 'message': None}

    resp = Response(json.dumps(rs))
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin']= '*'
    return resp


@db.route('/facility/list', methods=['GET'])
def facilityList():

    con = sqlite3.connect("twyshe.db")
    cur = con.cursor()

    res = cur.execute("SELECT * FROM app_facilities")

    rows = res.fetchall()
    columns = list(map(lambda x: x[0], cur.description))

    items = assist.getList(rows, columns)

    con.close()

    #rs = {'succeeded': True, 'items': items, 'message': None}

    resp = Response(json.dumps(items))
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin']= '*'

    return resp


@db.route('/resource/list', methods=['GET'])
def resourceList():

    con = sqlite3.connect("twyshe.db")
    cur = con.cursor()

    res = cur.execute("SELECT * FROM app_resources")

    rows = res.fetchall()
    columns = list(map(lambda x: x[0], cur.description))

    items = assist.getList(rows, columns)

    con.close()

    rs = {'succeeded': True, 'items': items, 'message': None}

    resp = Response(json.dumps(rs))
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin']= '*'

    return resp


@db.route('/country/list', methods=['GET'])
def countryList():

    con = sqlite3.connect("twyshe.db")
    cur = con.cursor()

    res = cur.execute("SELECT * FROM app_countries")

    rows = res.fetchall()
    columns = list(map(lambda x: x[0], cur.description))

    items = assist.getList(rows, columns)

    con.close()

    rs = {'succeeded': True, 'items': items, 'message': None}

    resp = Response(json.dumps(rs))
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin']= '*'

    return resp

@db.route('/color/list', methods=['GET'])
def colorist():

    con = sqlite3.connect("twyshe.db")
    cur = con.cursor()

    res = cur.execute("SELECT * FROM app_colors")

    rows = res.fetchall()
    columns = list(map(lambda x: x[0], cur.description))

    items = assist.getList(rows, columns)

    con.close()

    rs = {'succeeded': True, 'items': items, 'message': None}

    resp = Response(json.dumps(rs))
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin']= '*'

    return resp

@db.route('/login', methods=['POST'])
def loginUser():
    
    username = request.form.get('username')
    password = request.form.get('password')
  
    con = sqlite3.connect("twyshe.db")
    cur = con.cursor()

    res = cur.execute("SELECT * FROM app_users WHERE user_username=? OR user_email=?", [username, username])

    rows = res.fetchall()

    rs = {}

    if len(rows)==0:
        rs = {'succeeded': False, 'items': None, 'message': f"The specified user '{username}' could not be found"}
    else:
       columns = list(map(lambda x: x[0], cur.description))
       items = assist.getList(rows, columns)

       if items[0]['user_password'] != assist.getMD5(password):
                rs = {'succeeded': False, 'items': items[0]['user_password'], 'message': f"The specified user '{username}' or password is incorrect"}
       else:
                rs = {'succeeded': True, 'items': items, 'message': None}
    
    con.close()

    resp = Response(json.dumps(rs))

    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin']= '*'

    return resp

