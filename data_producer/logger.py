import logging
from datetime import datetime

class Logger:
    def __init__(self,file_name=None):
        self.file_name = file_name
    
    def start_logger(self):
        logging.basicConfig(filename=self.file_name, level=logging.DEBUG)

    def add(self,flag,message,*args):
        if len(args) != 0: message = message % args
        cc_message =  "%s: %s" % (datetime.now(), message)
        if flag == 'DEBUG': logging.debug(cc_message)
        if flag == 'INFO': logging.info(cc_message)
        if flag == 'ERROR': logging.error(cc_message)
        if flag == 'WARNING': logging.warning(cc_message)
        if flag == 'DISABLE': logging.disable(cc_message)
        print(cc_message)