import datetime
import logging
from openpyxl.utils import get_column_letter
from conn import get_conn

def process_data(records):
    logging.debug("%s: Beginning record processing..." % datetime.datetime.now())
    if len(records['bank']) != 0: add_data(records['bank'], 'bank')
    if len(records['branch']) != 0: add_data(records['branch'], 'branch')
    if len(records['applicant']) != 0: add_data(records['applicant'], 'applicant')
    if len(records['member']) != 0: add_data(records['member'], 'member')
    if len(records['user']) != 0: add_data(records['user'], 'user')
    if len(records['application']) != 0: add_data(records['application'], 'application')
    if len(records['merchant']) != 0: add_data(records['merchant'], 'merchant')
    if len(records['account']) != 0: add_data(records['account'], 'account')
    if len(records['transaction']) != 0: add_data(records['transaction'], 'transaction')

def add_data(records,tbl):
    logging.debug("%s: Table - %s" % (datetime.datetime.now(),tbl))
    conn = get_conn()
    curs = conn.cursor()
    vals = ["%s"] * len(records[0])
    sql = "INSERT INTO %s VALUES (%s)" % (tbl, ",".join(vals))
    logging.debug("%s: Executing statement: %s" % (datetime.datetime.now(),sql))
    try:
        curs.executemany(sql,records)
        conn.commit()
        logging.debug("%s: Execution complete. Records commited: %s" % (datetime.datetime.now(),curs.rowcount))
    except:
        logging.error("%s: Execution failed. Skipping table!" % datetime.datetime.now())

def process_table(ws):
    logging.debug("%s: Records found. Processing..." % datetime.datetime.now())
    col_len = len(tuple(ws.columns)) +1
    row_len = len(tuple(ws.rows)) +1
    records = []
    logging.debug("%s: Total records found: %d" % (datetime.datetime.now(),row_len-2))
    for row in range(2, row_len):
        record = []
        for col in range(1, col_len):
            char = get_column_letter(col)
            record.append(ws[char + str(row)].value)
        if len(record) != 0: records.append(tuple(record))
    if len(record) == 0: return []
    logging.debug("%s: Total records parsed: %d" % (datetime.datetime.now(),len(records)))
    return records
