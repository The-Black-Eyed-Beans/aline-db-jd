import mysql.connector
import logging
import datetime
import time

def get_conn():
    try: 
        logging.error("%s: Attempting to connect to database..." % datetime.datetime.now())
        db = mysql.connector.connect(
               host="aline-db",
               port=3306,
               user="root",
               password="123456",
               database="alinedb"
               )
    except:
        logging.error("%s: Failed to connect to database!" % datetime.datetime.now())
        time.sleep(15)
        return get_conn()
    return db

