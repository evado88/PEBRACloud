import json
import sqlite3
from flask import Blueprint, Response, request
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
        CREATE TABLE IF NOT EXISTS app_peer_uploads (
          upload_id INTEGER PRIMARY KEY,
          upload_username TEXT NULL,
          upload_status INTEGER NULL,
          upload_date TEXT NULL
        );
        """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_users (
          user_id INTEGER PRIMARY KEY,
          user_username TEXT NULL,
          user_fname TEXT NULL,
          user_lname TEXT NULL,
          user_phone TEXT NULL,
          user_email TEXT NULL,
          user_password TEXT NULL,
          user_role INTEGER NULL,
          user_thumbnailUrl NULL,
          user_status INTEGER NULL,
          user_createuser TEXT NULL,
          user_createdate TEXT NULL,
          user_lastupdatedate TEXT NULL,
          user_lastupdateuser TEXT NULL
        );
        """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_logins (
          login_id INTEGER PRIMARY KEY,
          login_username TEXT NULL,
          login_source TEXT NULL,
          login_date TEXT NULL
        );
        """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_logs (
          log_id INTEGER PRIMARY KEY,
          log_username TEXT NULL, 
          log_title TEXT NULL,
          log_action TEXT NULL,
          log_description TEXT NULL,
          log_exception TEXT NULL,
          log_date TEXT NULL
        );
        """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_audits (
          audit_id INTEGER PRIMARY KEY,
          audit_username TEXT NULL,
          audit_title TEXT NULL,
          audit_action TEXT NULL,
          audit_description TEXT NULL,
          audit_date TEXT NULL
        );
        """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_peer_navigators (
          id INTEGER PRIMARY KEY,
          status INTEGER NULL,
          parent INTEGER NULL,    
          username TEXT NULL,
          upload INTEGER NULL,
          phone_number TEXT NULL,    
          first_name TEXT NULL,
          last_name TEXT NULL,
          phone_number_upload_required TEXT NULL,
          is_active INTEGER NULL,
          deactivated_date TEXT NULL,
          created_date TEXT NULL
        );
        """)
    

    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_participants (
          id INTEGER PRIMARY KEY, -- utility
          status INTEGER NULL,
          parent INTEGER NULL,    
          username TEXT NULL,  
          upload INTEGER NULL,
          enrollment_date TEXT NULL,
          study_number TEXT NULL, --personal
          names TEXT NULL,
          birthday TEXT NULL,
          downloaded_messenger INTEGER NULL,  --messenger
          no_download_messenger_reason INTEGER NULL,
          no_download_messenger_reason_specify TEXT NULL,
          phone_number TEXT NULL, --contact
          own_phone INTEGER NULL,
          residency INTEGER NULL,
          prefered_contact_method INTEGER NULL,
          contact_frequency INTEGER NULL,
          history_modern_contraception_use INTEGER NULL, -- history contraception
          history_contraception_male_condom BIT NULL,
          history_contraception_female_condom BIT NULL,
          history_contraception_implant BIT NULL,
          history_contraception_injection BIT NULL,
          history_contraception_iud BIT NULL,
          history_contraception_ius BIT NULL,
          history_contraception_pills BIT NULL,
          history_contraception_other BIT NULL,
          history_contraception_other_specify TEXT NULL,
          history_contraception_satisfaction INTEGER NULL,
          history_contraception_satisfaction_reason TEXT NULL,
          history_contraception_stop_reason TEXT NULL,
          history_contraception_no_use_reason TEXT NULL,
          history_hiv_know_status INTEGER NULL, -- history hiv
          history_hiv_last_test TEXT NULL, 
          history_hiv_used_prep INTEGER NULL,
          history_hiv_prep_last_refil TEXT NULL, 
          history_hiv_prep_last_refil_source INTEGER NULL,
          history_hiv_prep_last_refil_source_specify TEXT NULL, 
          history_hiv_prep_problems TEXT NULL,
          history_hiv_prep_questions TEXT NULL,
          history_hiv_taking_art INTEGER NULL,
          history_hiv_last_refil TEXT NULL, 
          history_hiv_last_refil_source INTEGER NULL,
          history_hiv_last_refil_source_specify TEXT NULL, 
          history_hiv_art_problems TEXT NULL,
          history_hiv_art_questions TEXT NULL,
          history_hiv_desired_support_reminders_appointments BIT NULL,
          history_hiv_desired_support_reminders_checkins BIT NULL,
          history_hiv_desired_support_refil_accompany BIT NULL,
          history_hiv_desired_support_refil_pn_accompany BIT NULL,
          history_hiv_desired_support_other BIT NULL,
          history_hiv_desired_support_other_specify TEXT NULL,
          history_hiv_prep_desired_support_reminders_appointments BIT NULL,
          history_hiv_prep_desired_support_reminders_adherence BIT NULL,
          history_hiv_prep_desired_support_refil_pn_accompany BIT NULL,
          history_hiv_prep_desired_support_pn_hiv_kit BIT NULL,
          history_hiv_prep_desired_support_other BIT NULL,
          history_hiv_prep_desired_support_other_specify TEXT NULL,
          history_hiv_prep_stop_reason TEXT NULL,
          srh_contraception_interest INTEGER NULL, -- srh contraception
          srh_contraception_no_interest_reason TEXT NULL,
          srh_contraception_interest_male_condom BIT NULL, 
          srh_contraception_interest_female_condom BIT NULL, 
          srh_contraception_interest_implant BIT NULL, 
          srh_contraception_interest_injection BIT NULL, 
          srh_contraception_interest_iud BIT NULL, 
          srh_contraception_interest_ius BIT NULL, 
          srh_contraception_interest_pills BIT NULL, 
          srh_contraception_interest_other BIT NULL, 
          srh_contraception_interest_other_specify TEXT NULL,
          srh_contraception_method_in_mind INTEGER NULL,
          srh_contraception_information_methods INTEGER NULL,
          srh_contraception_find_schedule_facility INTEGER NULL,
          srh_contraception_find_schedule_facility_yes_date TEXT NULL,
          srh_contraception_find_schedule_facility_yes_pn_accompany INTEGER NULL,
          srh_contraception_find_schedule_facility_no_date INTEGER NULL,
          srh_contraception_find_schedule_facility_no_pick INTEGER NULL,
          srh_contraception_find_schedule_facility_selected TEXT NULL,
          srh_contraception_find_schedule_facility_other TEXT NULL,
          srh_contraception_information_app INTEGER NULL,
          srh_contraception_information_app_sent BIT NULL,
          srh_contraception_learn_methods INTEGER NULL,
          srh_prep_interest INTEGER NULL, -- srh prep
          srh_prep_no_interest_reason TEXT NULL, 
          srh_prep_information_app INTEGER NULL, 
          srh_prep_information_app_sent BIT NULL, 
          srh_prep_find_schedule_facility INTEGER NULL, 
          srh_prep_find_schedule_facility_yes_date TEXT NULL, 
          srh_prep_find_schedule_facility_yes_pn_accompany INTEGER NULL, 
          srh_prep_find_schedule_facility_no_date INTEGER NULL, 
          srh_prep_find_schedule_facility_no_pick INTEGER NULL, 
          srh_prep_find_schedule_facility_selected TEXT NULL, 
          srh_prep_find_schedule_facility_other TEXT NULL, 
          srh_prep_information_read INTEGER NULL,
          next_date TEXT NULL
        );
        """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_followups (
          id INTEGER PRIMARY KEY,
          status INTEGER NULL,
          parent INTEGER NULL,    
          username TEXT NULL,
          upload INTEGER NULL,
          created_date TEXT NULL,
          next_date TEXT NULL,
          art_number TEXT NULL,
          srh_contraception_started INTEGER NULL, -- srh contraception
          srh_contraception_started_method INTEGER NULL, 
          srh_contraception_started_problems INTEGER NULL, 
          srh_contraception_started_side_effects TEXT NULL, 
          srh_contraception_started_other TEXT NULL, 
          srh_contraception_interest INTEGER NULL, 
          srh_contraception_no_interest_reason INTEGER NULL,
          srh_contraception_interest_male_condom BIT NULL, 
          srh_contraception_interest_female_condom BIT NULL, 
          srh_contraception_interest_implant BIT NULL, 
          srh_contraception_interest_injection BIT NULL, 
          srh_contraception_interest_iud BIT NULL, 
          srh_contraception_interest_ius BIT NULL, 
          srh_contraception_interest_pills BIT NULL, 
          srh_contraception_interest_other BIT NULL, 
          srh_contraception_interest_other_specify TEXT NULL,
          srh_contraception_method_in_mind INTEGER NULL,
          srh_contraception_information_methods INTEGER NULL,
          srh_contraception_find_schedule_facility INTEGER NULL,
          srh_contraception_find_schedule_facility_yes_date TEXT NULL,
          srh_contraception_find_schedule_facility_yes_pn_accompany INTEGER NULL,
          srh_contraception_find_schedule_facility_no_date INTEGER NULL,
          srh_contraception_find_schedule_facility_no_pick INTEGER NULL,
          srh_contraception_find_schedule_facility_selected TEXT NULL,
          srh_contraception_find_schedule_facility_other INTEGER NULL,
          srh_contraception_information_app INTEGER NULL,
          srh_contraception_information_app_sent BIT NULL,
          srh_contraception_learn_methods INTEGER NULL,
          srh_prep_started INTEGER NULL, -- srh prep
          srh_prep_started_problems INTEGER NULL, 
          srh_prep_started_side_effects TEXT NULL, 
          srh_prep_started_other TEXT NULL, 
          srh_prep_interest INTEGER NULL, 
          srh_prep_no_interest_reason TEXT NULL, 
          srh_prep_information_app INTEGER NULL, 
          srh_prep_information_app_sent BIT NULL, 
          srh_prep_find_schedule_facility INTEGER NULL, 
          srh_prep_find_schedule_facility_yes_date TEXT NULL, 
          srh_prep_find_schedule_facility_yes_pn_accompany INTEGER NULL, 
          srh_prep_find_schedule_facility_no_date TEXT NULL, 
          srh_prep_find_schedule_facility_no_pick INTEGER NULL, 
          srh_prep_find_schedule_facility_selected TEXT NULL, 
          srh_prep_find_schedule_facility_other TEXT NULL, 
          srh_prep_information_read INTEGER NULL
        );
        """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_analytics (
          id INTEGER PRIMARY KEY,
          status INTEGER NULL,
          username TEXT NULL,
          upload INTEGER NULL,
          type INTEGER NULL,
          start_date TEXT NULL,
          end_date TEXT NULL,
          duration INTEGER NULL,
          result TEXT NULL,
          subject TEXT NULL,
          created_date TEXT NULL
        );
        """)
    
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_sent_resources (
          id INTEGER PRIMARY KEY,
          resource INTEGER NULL,
          user TEXT NULL,
          participant TEXT NULL,
          created_date TEXT NULL,
          status INTEGER NULL,
          date TEXT NULL
        );
        """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_facilities (
          facility_id INTEGER PRIMARY KEY,
          facility_name TEXT NULL,
          facility_address TEXT NULL,
          facility_tollfree TEXT NULL,
          facility_whatsapp TEXT NULL,
          facility_email TEXT NULL,
          facility_website TEXT NULL,
          facility_phone TEXT NULL,
          facility_contraception BIT NULL,
          facility_prep BIT NULL,
          facility_abortion BIT NULL,
          facility_menstrual BIT NULL,
          facility_sti BIT NULL,
          facility_art BIT NULL,
          facility_lat REAL NULL,
          facility_lon REAL NULL,
          facility_thumbnailUrl NULL,
          facility_status INTEGER NULL,
          facility_createuser TEXT NULL,
          facility_createdate TEXT NULL,
          facility_lastupdatedate TEXT NULL,
          facility_lastupdateuser TEXT NULL
        );
        """)
    
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_resources (
          resource_id INTEGER PRIMARY KEY,
          resource_name TEXT NULL,
          resource_description TEXT NULL,
          resource_url TEXT NULL,
          resource_thumbnailUrl TEXT NULL,
          resource_status INTEGER NULL,
          resource_createuser TEXT NULL,
          resource_createdate TEXT NULL,
          resource_lastupdatedate TEXT NULL,
          resource_lastupdateuser TEXT NULL
        );
        """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_countries (
          country_id INTEGER PRIMARY KEY,
          country_name TEXT NULL,
          country_code TEXT NULL,
          country_thumbnailUrl TEXT NULL,
          country_status INTEGER NULL,
          country_createuser TEXT NULL,
          country_createdate TEXT NULL,
          country_lastupdatedate TEXT NULL,
          country_lastupdateuser TEXT NULL
        );
        """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_notifications (
          notification_id INTEGER PRIMARY KEY,
          notification_type TEXT NULL,
          notification_title TEXT NULL,
          notification_body TEXT NULL,
          notification_description TEXT NULL,
          notification_createuser TEXT NULL,
          notification_createdate TEXT NULL,
          notification_lastupdatedate TEXT NULL,
          notification_lastupdateuser TEXT NULL
        );
        """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_colors (
          color_id INTEGER PRIMARY KEY,
          color_name TEXT NULL,
          color_code TEXT NULL,
          color_thumbnailUrl TEXT NULL,
          color_status INTEGER NULL,
          color_createuser TEXT NULL,
          color_createdate TEXT NULL,
          color_lastupdatedate TEXT NULL,
          color_lastupdateuser TEXT NULL
        );
        """)



    con.close()

    rs = {'succeeded': True, 'items': None,
          'message': 'The database structure has been initialized'}

    resp = Response(json.dumps(rs))
    resp.headers['Content-Type'] = 'application/json'

    return resp


@db.route('/drop-db-table', methods=['POST'])
def dropDatabaseTable():

    table = request.form.get ('table')

    if table is None:
         rs = {'succeeded': False, 'items': None, 'message': f"Please specify the {table} to drop from the database"}
    else:
         con = sqlite3.connect(assist.DB_NAME)

         cur = con.cursor()
    
         if table == 'all':
             
             items = ['app_participants', 'app_followups', 'app_peer_navigators', 'app_analytics', 'app_peer_uploads']
             
             for item in items:
               cur.execute(f"DROP TABLE {item}")
         else:
             cur.execute(f"DROP TABLE {table}")
        
         con.close()

         rs = {'succeeded': True, 'items': None,
              'message': f"The specified table '{table}' has been dropped"}

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