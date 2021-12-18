import logging
from datetime import datetime

class Logger:
    def __init__(self,file_name=None,std_out=False):
        self.file_name = file_name
        self.std_out = std_out
    
    def create_file_and_start(self):
        logging.basicConfig(filename=self.file_name, level=logging.DEBUG)

    def debug(self,message,*args):
        if len(args) != 0: message = message % args
        message =  "%s: %s" % (datetime.now(), message)
        logging.debug(message)
        if (self.std_out): print(message)

    def info(self,message,*args):
        if len(args) != 0: message = message % args
        message =  "%s: %s" % (datetime.now(), message)
        logging.info(message)
        if (self.std_out): print(message)

    def error(self,message,*args):
        if len(args) != 0: message = message % args
        message =  "%s: %s" % (datetime.now(), message)
        logging.error(message)
        if (self.std_out): print(message)

    def warning(self,message,*args):
        if len(args) != 0: message = message % args
        message =  "%s: %s" % (datetime.now(), message)
        logging.warning(message)
        if (self.std_out): print(message)

    def disable(self,message,*args):
        if len(args) != 0: message = message % args
        message =  "%s: %s" % (datetime.now(), message)
        logging.disable(message)
        if (self.std_out): print(message)

    def add(self,flag,message,*args):
        if len(args) != 0: message = message % args
        cc_message =  "%s: %s" % (datetime.now(), message)
        if flag == 'DEBUG': logging.debug(cc_message)
        if flag == 'INFO': logging.info(cc_message)
        if flag == 'ERROR': logging.error(cc_message)
        if flag == 'WARNING': logging.warning(cc_message)
        if flag == 'DISABLE': logging.disable(cc_message)
        print(cc_message)