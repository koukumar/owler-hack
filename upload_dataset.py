import mysql.connector
from mysql.connector import errorcode
import load_farequote

MYSQL_HOST = "cbe"
try:
   cnx = mysql.connector.connect(user='root', password='',
                              host=MYSQL_HOST)
   cursor = cnx.cursor()
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exists")
  else:
    print(err)
  exit()

DB_NAME = 'logbase'

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))

create_database(cursor)

try:
    cnx.database = DB_NAME
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        cnx.database = DB_NAME
    else:
        print(err)

TABLES = {}
TABLES['airfare'] = (
    "CREATE TABLE `airfare` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `ts` TIMESTAMP NOT NULL,"
    "  `airline` varchar(3) NOT NULL,"
    "  `response_time` FLOAT(13,3) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")



for name, ddl in TABLES.items():
    try:
        print("Creating table {}: ".format(name))
        cursor.execute(ddl)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

add_airfare = ("INSERT INTO airfare "
               "(ts, airline, response_time) "
               "VALUES (%s, %s, %s)")

print("reading airfare csv")
rows = load_farequote.load_airline_date()

print("loading data to mysql. #rows: " + str(len(rows)-1))
for row in rows[1:]:
    cursor.execute(add_airfare, row[0:3])

cnx.commit()
cursor.close()
cnx.close()