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

def insert(cursor, word):
  query = ("INSERT IGNORE INTO Keyword "
           "(Word) " 
           "VALUES (%s)")
  data_query = (word,)

  print(word)
  cursor.execute(query, data_query)

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
  while True:
    print("Processando o ano:", counter)
    filename = f'../database/{counter}/keywords.csv'
    try:
      with open(filename, newline='') as csvfile:
        content_file = list(csv.DictReader(csvfile))
        for i, linha in enumerate(content_file):
          isEqualIn = False
          if len(palavras_dif) >= 1:
            for word in palavras_dif:
              if isEqualIn == False and isEqual(linha['keyword'], word[1]):
                isEqualIn = True
                all_keywords.append([word[0], linha['keyword']])
            if isEqualIn == False:
              palavras_dif.append([id, linha['keyword']])
              id += 1
          else:
            palavras_dif.append([id, linha['keyword']])
            id += 1
      
      with open('./all_keywords.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(all_keywords)

      with open('./dif_keywords.csv', 'w', newline='') as file2:
        writer = csv.writer(file2)
        writer.writerows(palavras_dif)
      counter = counter - 1
    except IOError:
      print("Quebrou no ano:", counter)
      cursor.close()
      cnx.close()
      break