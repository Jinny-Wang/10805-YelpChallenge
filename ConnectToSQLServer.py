## 10-805 Machine Learning with Large Dataset  Final Project
## Yelp Challenge
## Code snippet :  Connecting to remote sql server using python
## Date : Oct. 22nd 2017
## Name : Jingyu Wang

## Assumption : Please install mysql connector on your macs

import mysql.connector
from mysql.connector import errorcode
import datetime


# step 1 : connect to the remote MySQL server
try:
  cnx = mysql.connector.connect(user='Admin10805', password='10805fall2017',
                              host='yelp2.csfuygoxtob2.us-east-2.rds.amazonaws.com',
                              database='yelp_db')
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
# else:
#   cnx.close()



# step 2 : query the data
cursor = cnx.cursor()
query = ("SELECT id FROM business WHERE state = %s")

state = "CA"
cursor.execute(query,(state,)) ## note !! pass  (state,) to create a tuple of strings!!
results = cursor.fetchall()
for row in results:
    print row
