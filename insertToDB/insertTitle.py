import os
from sqlite3 import DatabaseError
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import csv

load_dotenv()

def insert(cursor, id, title, year):
  query = ("INSERT INTO Paper "
           "(Title, id, Year) " 
           "VALUES (%s, %s, %s)")
  data_query = (title, int(id), year)
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

  last_id = 0
  while True:
    filename = f'../database/{counter}/titles.csv'
    try:
      with open(filename, newline='') as csvfile:
        content_file = list(csv.DictReader(csvfile))

        for i, linha in enumerate(content_file):
          try:
            id_actual = int(linha['id']) + last_id
            print(id_actual, last_id)
            insert(cursor, id_actual, linha['title'], linha['year'])
            cnx.commit()
            if i == len(content_file) - 1:
              last_id = last_id + int(linha['id']) + 1
          except DatabaseError:
            print("Failed to insert %s, %s, %s", linha['id'], linha['title'], linha['year'])
      counter = counter - 1
    except IOError:
      print("Quebrou no ano:", counter)
      cursor.close()
      cnx.close()
      break
  # result = cursor.execute("SELECT * FROM Paper")
  # print(result)