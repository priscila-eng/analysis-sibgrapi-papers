import os
import re
from sqlite3 import DatabaseError
import Levenshtein
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import csv

from pymysql import NULL
from unidecode import unidecode

load_dotenv()

def insert(cursor, id, word):
  query = ("INSERT INTO Keyword "
           "(id, Word) " 
           "VALUES (%s, %s)")
  data_query = (id, word)
  cursor.execute(query, data_query)
  print("Qtde de linhas inseridas: ", cursor.rowcount)

def isEqual(text1, text2):
  
  aux1 = unidecode(text1).upper()
  aux2 = unidecode(text2).upper()
  distance = Levenshtein.distance(aux1, aux2)

  if distance < 2:
    return True
  else:
    if len(aux1) > len(aux2):
      if re.search(fr"\b{aux2}\b", aux1):
        return True
    elif len(aux2) > len(aux1):
      if re.search(fr"\b{aux1}\b", aux2):
        return True

  return False


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

  palavras_dif = []
  all_keywords = []
  id = 0
  filename = f'./dif_keywords.csv'
  print("Processando o arquivo:", filename)
  with open(filename, newline='') as csvfile:
    content_file = list(csv.DictReader(csvfile))
    for i, linha in enumerate(content_file):
      print("Inserindo palavra ", linha['keyword'])
      try:
        insert(cursor, linha["id"], linha['keyword'])
        cnx.commit()
      except DatabaseError:
        print("Failed to insert %s", linha['keyword'])