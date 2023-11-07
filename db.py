import json
import sqlite3
from flask import Blueprint, Response
import assist

db = Blueprint('db', __name__)


@db.route("/db")
def dbr():
    return {'app': 'Database configuration file'}


@db.route('/initialize-db', methods=['POST'])
def initializeDb():

    con = sqlite3.connect(assist.DB_NAME)
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_users (
          user_id INTEGER PRIMARY KEY,
          user_username TEXT,
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
        CREATE TABLE IF NOT EXISTS app_logins (
          login_id INTEGER PRIMARY KEY,
          login_username TEXT,
          login_source TEXT,
          login_date TEXT
        );
        """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_logs (
          log_id INTEGER PRIMARY KEY,
          log_username TEXT, 
          log_title TEXT,
          log_action TEXT,
          log_description TEXT,
          log_exception TEXT,
          log_date TEXT
        );
        """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_audits (
          audit_id INTEGER PRIMARY KEY,
          audit_username TEXT,
          audit_title TEXT,
          audit_action TEXT,
          audit_description TEXT,
          audit_date TEXT
        );
        """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_peer_navigators (
          peer_id INTEGER PRIMARY KEY,
          peer_username TEXT,
          peer_fname TEXT,
          peer_lname TEXT,
          peer_phone TEXT,
          peer_email TEXT,
          peer_password TEXT,
          peer_thumbnailUrl,
          peer_status INTEGER,
          peer_createpeer TEXT,
          peer_createdate TEXT,
          peer_lastupdatedate TEXT,
          peer_lastupdatepeer TEXT
        );
        """)
    

    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_participants (
          participant_id INTEGER PRIMARY KEY,
          participant_fname TEXT,
          participant_lname TEXT,
          participant_dob TEXT,
          participant_phone TEXT,analytic
          participant_email TEXT,
          participant_thumbnailUrl,
          participant_status INTEGER,
          participant_createuser TEXT,
          participant_createdate TEXT,
          participant_lastupdatedate TEXT,
          participant_lastupdateuser TEXT
        );
        """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_followups (
          followup_id INTEGER PRIMARY KEY,
          followup_participant TEXT,
          followup_status INTEGER,
          followup_createuser TEXT,
          followup_createdate TEXT,
          followup_lastupdatedate TEXT,
          followup_lastupdateuser TEXT
        );
        """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_analytics (
          analytic_id INTEGER PRIMARY KEY,
          analytic_type INTEGER,
          analytic_startdate TEXT,
          analytic_enddate TEXT,
          analytic_duration INTEGER,
          analytic_result TEXT,
          analytic_subject TEXT
        );
        """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_facilities (
          facility_id INTEGER PRIMARY KEY,
          facility_name TEXT,
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
    
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_resources (
          resource_id INTEGER PRIMARY KEY,
          resource_name TEXT,
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
        CREATE TABLE IF NOT EXISTS app_countries (
          country_id INTEGER PRIMARY KEY,
          country_name TEXT,
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
        CREATE TABLE IF NOT EXISTS app_notifications (
          notification_id INTEGER PRIMARY KEY,
          notification_type TEXT,
          notification_title TEXT,
          notification_body TEXT,
          notification_description TEXT,
          notification_createuser TEXT,
          notification_createdate TEXT,
          notification_lastupdatedate TEXT,
          notification_lastupdateuser TEXT
        );
        """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_colors (
          color_id INTEGER PRIMARY KEY,
          color_name TEXT,
          color_code,
          color_thumbnailUrl,
          color_status INTEGER,
          color_createuser TEXT,
          color_createdate TEXT,
          color_lastupdatedate TEXT,
          color_lastupdateuser TEXT
        );
        """)



    con.close()

    rs = {'succeeded': True, 'items': None,
          'message': 'The database structure has been initialized'}

    resp = Response(json.dumps(rs))
    resp.headers['Content-Type'] = 'application/json'

    return resp


@db.route('/initialize-data', methods=['POST'])
def initializeData():

    con = sqlite3.connect(assist.DB_NAME)
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
             'https://westwindfoundation.org/wp-content/uploads/2020/05/marie-stopes.jpg',
             1, 'admin', '2023-08-23', 'admin', '2023-08-23'),
            ('Planned Parenthood Association of Zambia (PPAZ)', 'Corner of church road and Dushambe Road, Lusaka', None, None,
            'info@ppaz.org.zm', 'https://www.facebook.com/PPAZambia/', '+260211256182',
             1, 1, 1, 1, 1, 0,
             29.44, 23.00,
             'https://www.ippf.org/sites/default/files/2016-06/zambia_MA_logo.jpg',
             1, 'admin', '2023-08-23', 'admin', '2023-08-23'),]

    cur.executemany("""INSERT INTO app_facilities (facility_name, facility_address, facility_tollfree, facility_whatsapp,
                    facility_email, facility_website, facility_phone,
                    facility_contraception, facility_prep,facility_abortion,facility_menstrual, facility_sti,  facility_art,
                    facility_lat, facility_lon,
                    facility_thumbnailUrl,
                    facility_status, facility_createuser, facility_createdate, facility_lastupdatedate, facility_lastupdateuser) 
                    VALUES (?, ?, ?, ?, 
                            ?, ?, ?,
                            ?, ?, ?, ?, ?, ?,
                            ?, ?,
                            ?,
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

    con = sqlite3.connect(assist.DB_NAME)
    cur = con.cursor()

    data = []
    rs = {}

    if feature == 'color':

        data = [("red", '#D32F2F', 1, 'admin', '2023-08-23', 'admin', '2023-08-23'),
                ("pink", '#C2185B', 1, 'admin',
                 '2023-08-23', 'admin', '2023-08-23'),
                ("purple", '#7B1FA2', 1, 'admin',
                 '2023-08-23', 'admin', '2023-08-23'),
                ("indigo", '#303F9F', 1, 'admin',
                 '2023-08-23', 'admin', '2023-08-23'),
                ("blue", '#1976D2', 1, 'admin',
                 '2023-08-23', 'admin', '2023-08-23'),
                ("green", '#388E3C', 1, 'admin',
                 '2023-08-23', 'admin', '2023-08-23'),
                ("brown", '#388E3C', 1, 'admin', '2023-08-23', 'admin', '2023-08-23'),]

        cur.executemany("""INSERT INTO app_colors (color_name, color_code, color_status, 
                                              color_createuser, color_createdate, color_lastupdatedate, color_lastupdateuser) 
                    VALUES (?, ?, ?, 
                            ?, ?, ?, ?)""", data)

        con.commit()

        rs = {'succeeded': False, 'items': None,
              'message': f"The data for '{feature}' has been initialized"}

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

        rs = {'succeeded': False, 'items': None,
              'message': f"The data for '{feature}' has been initialized"}

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

        rs = {'succeeded': False, 'items': None,
              'message': f"The data for '{feature}' has been initialized"}

    elif feature == 'facility':

        data = [('Marie Stopes International (MSI)', 'Plot 120 Kudu Road, Kabulonga, Lusaka', '5600', '+260762560733',
                 'info@mariestopes.org.zm', 'https://www.msichoices.org/', '+260965005600',
                 1, 0, 1, 1, 1, 0,
                 29.44, 23.00,
                 'https://westwindfoundation.org/wp-content/uploads/2020/05/marie-stopes.jpg',
                 1, 'admin', '2023-08-23', 'admin', '2023-08-23'),
                ('Planned Parenthood Association of Zambia (PPAZ)', 'Corner of church road and Dushambe Road, Lusaka', None, None,
                 'info@ppaz.org.zm', 'https://www.facebook.com/PPAZambia/', '+260211256182',
                 1, 1, 1, 1, 1, 0,
                 29.44, 23.00,
                 'https://www.ippf.org/sites/default/files/2016-06/zambia_MA_logo.jpg',
                 1, 'admin', '2023-08-23', 'admin', '2023-08-23'),]

        cur.executemany("""INSERT INTO app_facilities (facility_name, facility_address, facility_tollfree, facility_whatsapp,
                    facility_email, facility_website, facility_phone,
                    facility_contraception, facility_prep,facility_abortion,facility_menstrual, facility_sti,  facility_art,
                    facility_lat, facility_lon,
                    facility_thumbnailUrl,
                    facility_status, facility_createuser, facility_createdate, facility_lastupdatedate, facility_lastupdateuser) 
                    VALUES (?, ?, ?, ?, 
                            ?, ?, ?,
                            ?, ?, ?, ?, ?, ?,
                            ?, ?,
                            ?,
                            ?, ?, ?, ?, ?)""", data)

        con.commit()

        rs = {'succeeded': False, 'items': None,
              'message': f"The data for '{feature}' has been initialized"}

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

        rs = {'succeeded': False, 'items': None,
              'message': f"The data for '{feature}' has been initialized"}

    else:
        rs = {'succeeded': False, 'items': None,
              'message': f"The specified feature '{feature}' is not valid"}

    con.close()

    resp = Response(json.dumps(rs))
    resp.headers['Content-Type'] = 'application/json'

    return resp