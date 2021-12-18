from datetime import datetime
from logger import Logger
import util

file_name = "py_inj_%s.log" % datetime.today().strftime('%Y-%m-%d-%H%M%S')
logger = Logger(file_name,std_out=True)
logger.create_file_and_start()
logger.info("Starting python script...")

util.verify_account_sequence()
util.add_null_merchant()

qty = 100
banks = util.create_banks(qty)
branches = util.create_branch(banks)
applicants = util.create_applicants(qty)
applications = util.clean_applications(util.create_applications(applicants))
users = util.create_users(applications)
merchants = util.create_merchants(int(qty/5))
transactions = util.create_transactions(users,merchants)

logger.info("Script completed successfully and is shuting down!")