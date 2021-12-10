import socket
import time
import logging
import datetime

def ping(host,port):
    """
    Returns True if host (str) responds to a ping request.
    """
    logging.debug("%s: Pinging database @ %s" % (datetime.datetime.now(),host))
    

    # Create network socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Ping target
    result = sock.connect_ex((host,int(port)))

    if result == 0:
        logging.debug("%s: Ping pong. Success." % datetime.datetime.now())
        return True
    else:
        logging.error("%s: Ping poop. No response." % datetime.datetime.now())
        return False

def pinger(host,port):
    """
    Returns True if host (str) eventually responds to a ping request.
    Adjust snooze appropriately. Probably better as env. var.
    """
    snooze = 15
    logging.debug("%s: Starting ping cycle..." % datetime.datetime.now())
    for i in range(1,6):
        if ping(host,port) == True: 
            logging.debug("%s: Exiting ping cycle..." % datetime.datetime.now())
            return True
        logging.debug("%s: Reattempting in %i seconds..." % (datetime.datetime.now(),snooze))
        time.sleep(snooze)
    logging.error("%s: Pings exhausted. No response." % datetime.datetime.now())
    return False

