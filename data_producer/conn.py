from os import environ
import logging
import datetime
import mysql.connector
from pinger import ping, pinger

def get_conn():
    host = environ.get('MYSQL_HOST')
    port=environ.get('MYSQL_PORT')

    # ping database before attempting to connect.
    logging.debug("%s: Pinging database @ %s" % (datetime.datetime.now(),host))
    if ping(host,port) == False: 
        # ping failed.
        if pinger(host,port) == False: return
    try: 
        logging.error("%s: Attempting to connect to database..." % datetime.datetime.now())
        db = mysql.connector.connect(
               host=host,
               port=port,
               user=environ.get('MYSQL_USER'),
               password=environ.get('MYSQL_PASSWORD'),
               database=environ.get('MYSQL_DATABASE')
               )
        return db
    except:
        logging.error("%s: Failed to connect to database!" % datetime.datetime.now())
        return

