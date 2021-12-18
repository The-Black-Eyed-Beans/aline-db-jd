from os import environ
import requests
from random import randint
from faker import Faker
from faker.providers import internet,date_time,misc
from conn import get_conn
from logger import Logger

logger = Logger(std_out=True)
fake = Faker()
fake.add_provider(internet)
fake.add_provider(date_time)
fake.add_provider(misc)

credentials = {
    "username":environ.get('USER_USERNAME'),
    "password":environ.get('USER_PASSWORD'),
}

conn_attempts = 10

def create_admin():
    admin = {
        "role":environ.get('USER_ROLE'),
        "username":environ.get('USER_USERNAME'),
        "password":environ.get('USER_PASSWORD'),
        "firstName":environ.get('USER_FIRSTNAME'),
        "lastName":environ.get('USER_LASTNAME'),
        "email":environ.get('USER_EMAIL'),
        "phone":environ.get('USER_PHONE'),
    }
    add_admin(admin)

def add_admin(payload):
    # Register a new user
    # Returns {username, password}
    logger.info("Attempting to Register user.")
    url = "http://%s/users/registration" % environ.get('URL_USER')
    r = requests.post(url,json=payload)
    if (r.status_code >= 200 and r.status_code <= 300):
        username = payload['username']
        password = payload['password']
        logger.info("User successfully registered.")
        logger.info("username: %s password: %s",username,password)
        return {username,password}
    logger.error("User failed to be registered!")

def get_token(payload):
    # Returns jwt -> Bearer xyz
    logger.info("Attempting to retieve token.")
    url = "http://%s/login" % environ.get('URL_USER')
    r = requests.post(url,json=payload)
    if (r.status_code >= 200 and r.status_code <= 300):
        token = r.headers['Authorization']
        logger.info("Token: %s", token.split(' ')[1])
        return token
    logger.error("Failed to retrieve token!")
    for i in range(conn_attempts):
        create_admin()
        token = get_token(credentials)
        if token: return token
        return False

def get_random_license():
    return "DL%d" % randint(10000, 99999)

def get_random_social_security():
    return "%d-%d-%d" % (randint(100,999),randint(10,99),randint(1000,9999))

def get_random_routing_num():
    return randint(100000000, 999999999)

def get_random_phone_num():
    return "(%d) %d-%d" % (randint(100, 999),randint(100, 999),randint(1000, 9999))

def get_random_address():
    addr = fake.address().split('\n')
    if len(addr) > 2: get_random_address()
    addr = [addr[0]] + addr[1].split(', ')
    return addr[:2] + addr[-1].split(' ')

def create_applicants(qty):
    logger.info("Attempting to create %d dummy applicants...",qty)
    applicants = []
    for i in range(qty):
        logger.info("Applicant #%d" % i)
        applicants.append(add_applicant())
    return applicants

def create_applications(applicants):
    logger.info("Attempting to create %d dummy applications...",len(applicants))
    ids = list(map(lambda x: x['id'],applicants))
    apps = []
    i = 1
    for id in ids:
        logger.info("Application #%d" % i)
        apps.append(add_application(id))
        i+=1
    return apps

def create_banks(qty):
    logger.info("Attempting to create %d dummy banks...",qty)
    banks = []
    for i in range(qty):
        logger.info("Bank #%d",i)
        banks.append(add_bank())
    return banks

def create_branch(banks):
    logger.info("Attempting to create %d dummy branches...",len(banks))
    branches = []
    for i in range(len(banks)):
        logger.info("Branch #%d",i)
        branches.append(add_branch(banks[i]['id']))
    return branches

def add_null_merchant():
    logger.info("Attempting to insert NULL merchant...")
    conn = get_conn()
    curs = conn.cursor()
    sql = 'INSERT INTO alinedb.merchant VALUES("NONE",null,null,null,"NONE",null,null,null)'
    try:
        curs.execute(sql)
        conn.commit()
        logger.info("Execution complete. Records commited: %s",curs.rowcount)
    except:
        logger.error("Execution failed. This may lead to errors/bugs when populating certain transactions!")

def create_merchants(qty):
    logger.info("Attempting to create %d dummy merchants...",qty)
    merchants = []
    for i in range(qty):
        logger.info("Merchant #%d",i)
        merchants.append(add_merchant())
    return merchants

def create_transactions(users,merchants):
    logger.info("Attempting to create %d dummy transactions...",len(users))
    transactions = []
    i = 1
    for user in users:
        rand_int = randint(0, len(merchants)-1)
        merchant = merchants[rand_int]
        logger.info("Transaction #%d",i)
        transactions.append(add_transaction(user,merchant))
        i+=1
    return transactions

def create_users(apps):
    logger.info("Attempting to create %d dummy users...",len(apps))
    users_list = []
    i = 1
    for application in apps:
        logger.info("User #%d",i)
        user = add_user(application)
        if (user != None): users_list.append(user)
        i+=1
    return users_list

def add_applicant():
    # Add new applicant
    # Returns {applicant}
    logger.info("Creating dummy applicant.")    
    url = "http://%s/applicants" % environ.get('URL_UNDERWRITER')
    token = get_token(credentials)
    headers = {'Authorization':token,"Content-Type":"application/json"}
    addr = get_random_address()
    gender = "FEMALE"
    if (randint(0,99) % 2 == 0): gender = "MALE"
    payload = {
        "firstName": fake.name().split(' ')[0],
        "lastName": fake.name().split(' ')[1],
        "address":addr[0],
        "city":addr[1],
        "state":fake.state(),
        "zipcode":addr[-1],
        "mailingAddress":addr[0],
        "mailingCity":addr[1],
        "mailingState":addr[-2],
        "mailingZipcode":addr[-1],
        "phone":get_random_phone_num(),
        "driversLicense":get_random_license(),
        "socialSecurity": get_random_social_security(),
        "income":get_random_routing_num(),
        "gender":gender,
        "dateOfBirth": fake.date(),
        "email":fake.email()
    }
    logger.info("Dummy applicant successfully generated.")
    logger.info("Sending data to microservice...")
    r = requests.post(url,headers=headers,json=payload)
    if (r.status_code >= 200 and r.status_code <= 300):
        logger.info("Microservice successfully added applicant to database!")
        return r.json()
    logger.error("Microservice failed to add applicant to database! Reattempting...")
    return add_applicant()

def add_application(id):
    # Add new applicants
    # Returns {applications}
    logger.info("Creating dummy application.")
    url = "http://%s/applications" % environ.get('URL_UNDERWRITER')
    payload = {
        "applicationType":"CHECKING",
        "noApplicants":True,
        "applicantIds": [id]
    }
    token = get_token(credentials)
    headers = {'Authorization':token,"Content-Type":"application/json"}
    for i in range(conn_attempts):
        r = requests.post(url,headers=headers,json=payload)
        if (r.status_code >= 200 and r.status_code <= 300):
            logger.info("Microservice successfully added applications to database!")
            return r.json()
        logger.error("Microservice failed to add applications to database! Reattempting...")

def add_bank():
    # Add new bank
    # Returns {bank}
    logger.info("Creating dummy bank.")
    url = "http://%s/banks" % environ.get('URL_BANK')
    addr = get_random_address()
    payload = {
        "routingNumber":get_random_routing_num(),
        "address":addr[0],
        "city":addr[1],
        "state":addr[2],
        "zipcode":addr[3]
    }
    logger.info("Dummy bank successfully generated.")
    logger.info("Sending data to microservice...")
    token = get_token(credentials)
    headers = {'Authorization':token,"Content-Type":"application/json"}
    r = requests.post(url,headers=headers,json=payload)
    if (r.status_code >= 200 and r.status_code <= 300):
        logger.info("Microservice successfully added bank to database!")
        return r.json()
    logger.error("Microservice failed to add bank to database! Reattempting...")
    return add_bank()

def add_branch(bankId):
    # Add new branch
    # Returns {branch}
    logger.info("Creating dummy branch.")
    url = "http://%s/branches" % environ.get('URL_BANK')
    addr = get_random_address()
    payload = {
        "bankID":bankId,
        "name":"%s Branch"%fake.name().split(' ')[1],
        "phone":get_random_phone_num(),
        "address":addr[0],
        "city":addr[1],
        "state":addr[2],
        "zipcode":addr[3]
    }
    logger.info("Dummy branch successfully generated.")
    logger.info("Sending data to microservice...")
    token = get_token(credentials)
    headers = {'Authorization':token,"Content-Type":"application/json"}
    r = requests.post(url,headers=headers,json=payload)
    if (r.status_code >= 200 and r.status_code <= 300):
        logger.info("Microservice successfully added branch to database!")
        return r.json()
    logger.error("Microservice failed to add branch to database! Reattempting...")
    return add_branch(bankId)

def add_merchant():
    # Add new merchant
    # Returns {merchant}
    logger.info("Creating dummy merchant.")
    name = fake.name().split(' ')[0]
    rand_int = randint(1, 999)
    merchant_name = "%s%d LLC" % (name,rand_int)
    code = "%s%d" % (merchant_name[:4],rand_int)
    payload = {
        "code":code,
        "name":merchant_name,
    }
    logger.info("Dummy merchant successfully generated.")
    return payload

def add_user(applicant):
    # Add new user 
    # Returns {user}
    logger.info("Creating dummy user.")
    url = "http://%s/users/registration"  % environ.get('URL_USER')
    username = "%s%s%d" % (applicant['firstName'],applicant['lastName'][-2:],randint(10,99999))
    payload = {
        "role":"member",
        "username": username,
        "password": 'Abc123456*',
        "membershipId": applicant['membershipId'],
        "lastFourOfSSN": applicant['socialSecurity'][7:]
    }
    logger.info("Dummy user successfully generated.")
    logger.info("Sending data to microservice...")
    token = get_token(credentials)
    headers = {'Authorization':token,"Content-Type":"application/json"}
    for i in range(conn_attempts):
        r = requests.post(url,headers=headers,json=payload)
        if (r.status_code >= 200 and r.status_code <= 300):
            logger.info("Microservice successfully added user to database!")
            data = r.json()
            # add accountNumber to User obj
            data['accountNumber'] = applicant['accountNumber']
            return data
        logger.error("Microservice failed to add user to database! Reattempting...")
    logger.error("Microservice failed. Attempts exhausted!")

def add_transaction(user,merchant):
    # Add new transaction
    # Returns {transaction}
    logger.info("Creating dummy transaction.")
    url = "http://%s/transactions" % environ.get('URL_TRANSACTIONS')
    Faker.seed(0)
    payload = {
        "type":"DEPOSIT",
        "accountNumber":user['accountNumber'],
        "amount":get_random_routing_num(),
        "merchantCode":merchant['code'],
        "merchantName":merchant['name'],
        "description": fake.text(max_nb_chars=15),
        "method":"ATM",
        "hold":False
    }
    logger.info("Dummy transaction successfully generated.")
    logger.info("Sending data to microservice...")
    token = get_token(credentials)
    headers = {'Authorization':token,"Content-Type":"application/json"}
    for i in range(conn_attempts):
        r = requests.post(url,headers=headers,json=payload)
        if (r.status_code >= 200 and r.status_code <= 300):
            logger.info("Microservice successfully added transaction to database!")
            return r.json()
        logger.error("Microservice failed to add transaction to database! Reattempting...")
    logger.error("Microservice failed. Attempts exhausted!")
    
def clean_applications(apps):
    logger.info("Starting application spin cycle (removing denied accounts).")
    applications_list = []
    for application in apps:
        logger.info("Checking application status...")
        if (application != None and application['membersCreated']): 
            logger.info("Application approved. Adding to list...")
            application['applicants'][0]['membershipId'] = int(application['createdMembers'][0]['membershipId'])
            application['applicants'][0]['accountNumber'] = application['createdAccounts'][0]['accountNumber']
            applications_list.append(application['applicants'][0])
            logger.info("Application successfully added to list...")
        else: logger.debug("Application denied. Skipping...")
    return applications_list

def set_account_sequence():
    logger.info("Attempting to add new record to table...")
    tbl = "account_sequence"
    conn = get_conn()
    curs = conn.cursor()
    sql = "INSERT INTO %s.%s VALUES (%d)" % (environ.get('MYSQL_DATABASE'),tbl,1)

    try:
        curs.execute(sql)
        conn.commit()
        logger.info("Execution complete. Records commited: %s",curs.rowcount)
    except:
        logger.error("Execution failed. This will cause an error when populating accounts!")

def verify_account_sequence():
    logger.info("Retrieving last record in account_sequence...")
    conn = get_conn()
    curs = conn.cursor()
    curs.execute(("SELECT * FROM %s" % "account_sequence"))
    r = curs.fetchall()
    if (len(r) == 0): 
        logger.debug("No record found!")
        set_account_sequence()
        return
    logger.info("Record found. Continuing to next process...")