from os import listdir
from os.path import isfile, join
from datetime import datetime
import logging
from openpyxl import load_workbook
from helpers import process_data, process_table

logging.basicConfig(filename='data_dump.log', level=logging.DEBUG)
logging.debug('%s: Starting flat file import.' % datetime.now())
logging.debug('%s: Building environment...' % datetime.now())


"""
SETTING DEBUG ENV
"""
# environ['MYSQL_HOST'] = 'localhost'
# environ['MYSQL_PORT'] = '3309'
# environ['MYSQL_USER'] = 'root'
# environ['MYSQL_PASSWORD'] = '123456'
# environ['MYSQL_DATABASE'] = 'alinedb'

read_files = []
mypath = "."
fileList = [f for f in listdir(mypath) if isfile(join(mypath, f)) and (f.endswith(".xls") or f.endswith(".xlsx"))]

for file_ in fileList:
    record_list = {}
    if file_ in read_files:
        logging.error("%s: File: %s has already been processed. Skipping file." % (datetime.now(),file_))
        continue
    logging.debug('%s: Loading file: %s' % (datetime.now(),file_))
    try:
        wb = load_workbook(file_)
        logging.debug("%s: File successfully loaded." % datetime.now())
        logging.debug("%s: Sheets found!" % datetime.now())
        logging.debug("%s: %s" % (datetime.now(),wb.sheetnames))
    except:
        logging.error("%s: Error ocurred in loading file. Aborting file." % datetime.now())
        continue
    for sheet in wb.sheetnames:
        logging.debug("%s: Checking workbook for %s." % (datetime.now(),sheet))
        ws = wb[sheet]
        ws_len = len(ws['A'])
        if ws_len <= 1:
            logging.debug("%s: 0 records found. Skipping table." % datetime.now())
            record_list[sheet] = []
            continue
        records = process_table(ws)
        record_list[sheet] = records
    read_files.append(file_)
    process_data(record_list)
    logging.debug("%s: File processing complete!" % datetime.now())
print("log @ data_dump.log")
