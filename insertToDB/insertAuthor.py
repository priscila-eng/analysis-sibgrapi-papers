import os
from sqlite3 import DatabaseError
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import csv

from pymysql import NULL

load_dotenv()

def insert(cursor, name, gender):
  query = ("INSERT IGNORE INTO Author "
           "(Name, gender) " 
           "VALUES (%s, %s)")
  data_query = (name, gender)
  
  if gender == NULL:
    query = ("INSERT IGNORE INTO Author "
             "(Name, gender) " 
             "VALUES (%s, %s)")
    data_query = (name, None)

  print(name, gender)
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
  names = []
  with open('names.csv', newline='') as csvfile:
    names = list(csv.DictReader(csvfile))

  while True:
    filename = f'../database/{counter}/authors.csv'
    try:
      with open(filename, newline='') as csvfile:
        content_file = list(csv.DictReader(csvfile))
        for i, linha in enumerate(content_file):
          name_complete = linha['name'].split(' ')
          temNaLista = False
          for linha_nome in names:
            print(name_complete[0], linha_nome['nome'])
            if name_complete[0] == linha_nome['nome']:
              temNaLista = True
              try:
                insert(cursor, linha['name'], linha_nome['genero'])
                cnx.commit()
              except DatabaseError:
                print("Failed to insert %s, %s", linha['name'], linha_nome['genero'])
          if temNaLista == False:
            try:
              insert(cursor, linha['name'], NULL)
              cnx.commit()
            except DatabaseError:
              print("Failed to insert %s, %s", linha['name'], linha_nome['genero'])
      counter = counter - 1
    except IOError:
      print("Quebrou no ano:", counter)
      cursor.close()
      cnx.close()
      break