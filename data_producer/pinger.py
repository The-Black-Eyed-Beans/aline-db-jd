import socket
import time
from logger import Logger

logger = Logger()

def ping(host,port):
    """
    Returns True if host (str) responds to a ping request.
    """
    logger.add("DEBUG","Pinging database @ %s",host)

    # Create network socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Ping target
    result = sock.connect_ex((host,int(port)))

    if result == 0:
        logger.add("DEBUG","Ping pong. Success.")
        return True
    else:
        logger.add("ERROR","Ping poop. No response.")
        return False

def pinger(host,port):
    """
    Returns True if host (str) eventually responds to a ping request.
    Adjust snooze appropriately. Probably better as env. var.
    """
    snooze = 15
    logger.add("DEBUG","Starting ping cycle...")
    for i in range(1,6):
        if ping(host,port) == True:
            logger.add("DEBUG","Exiting ping cycle...")
            return True
        logger.add("DEBUG","Reattempting in %d seconds..",snooze)
        time.sleep(snooze)
    logger.add("ERROR","Pings exhausted. No response.")
    return False

