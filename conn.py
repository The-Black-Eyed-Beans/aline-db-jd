import mysql.connector
import logging
import datetime

def get_conn():
    try: 
        db = mysql.connector.connect(
               host="localhost",
               port=3309,
               user="root",
               password="123456",
               database="alinedb"
               )
    except:
        logging.error("%s: Failed to connect to database!" % datetime.datetime.now())
        return None
    return db

