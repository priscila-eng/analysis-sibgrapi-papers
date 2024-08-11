import os
from sqlite3 import DatabaseError
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import csv

from pymysql import NULL

load_dotenv()

def insert(cursor, word):
  query = ("INSERT IGNORE INTO Keyword "
           "(Word) " 
           "VALUES (%s)")
  data_query = (word,)

  print(word)
  cursor.execute(query, data_query)


counter = 2023

try:
  cnx = mysql.connector.connect(
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    database=os.getenv("DATABASE_NAME")
  )
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cursor = cnx.cursor()

  while True:
    filename = f'../database/{counter}/keywords.csv'
    try:
      with open(filename, newline='') as csvfile:
        content_file = list(csv.DictReader(csvfile))
        for i, linha in enumerate(content_file):
          try:
            insert(cursor, linha['keyword'])
            cnx.commit()
          except DatabaseError:
            print("Failed to insert %s", linha['keyword'])
      counter = counter - 1
    except IOError:
      print("Quebrou no ano:", counter)
      cursor.close()
      cnx.close()
      break