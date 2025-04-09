import os
from sqlite3 import DatabaseError
import Levenshtein
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import csv

from pymysql import NULL
from unidecode import unidecode

# geral -> estatísticas - BAR PLOT: qtos autores, qtos papers BR e IN, evolução ao longo do tempo

load_dotenv()

def insert(cursor, name, gender, ia):
  query = ("INSERT IGNORE INTO Author "
           "(Name, gender, IN_IA) " 
           "VALUES (%s, %s, %s)")
  data_query = (name, gender, ia)
  
  if gender == NULL:
    query = ("INSERT IGNORE INTO Author "
             "(Name, gender, IN_IA) " 
             "VALUES (%s, %s, %s)")
    data_query = (name, None, ia)

  cursor.execute(query, data_query)

def isEqual(text1, text2):
  unidecode(text1)

  distance = Levenshtein.distance(text1.upper(), text2.upper())

  if distance < 2:
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

  last_id = 0
  names = []
  names2 = []
  with open('names.csv', newline='') as csvfile:
    names = list(csv.DictReader(csvfile))

  with open('firstnames.csv', newline='') as csvfile:
    names2 = list(csv.DictReader(csvfile))

  file_name = f"./authors_ia.csv"
  lines = []
  lines.append(['Name', 'gender', 'IA'])
  while True:
    filename = f'../database/{counter}/authors.csv'
    print("Processando o ano: ", counter)
    try:
      with open(filename, newline='') as csvfile:
        content_file = list(csv.DictReader(csvfile))
        for i, linha in enumerate(content_file):
          name_complete = linha['name'].split(' ')
          temNaLista = False
          for linha_nome in names:
            if isEqual(name_complete[0], linha_nome['nome']):
              temNaLista = True
              try:
                insert(cursor, linha['name'], linha_nome['sexo'], 'N')
                cnx.commit()
              except DatabaseError:
                print("Failed to insert %s, %s", linha['name'], linha_nome['sexo'])
            else:
              if len(name_complete) > 1:
                if temNaLista == False and isEqual(name_complete[1], linha_nome['nome']):
                  temNaLista = True
                  try:
                    insert(cursor, linha['name'], linha_nome['sexo'], 'N')
                    cnx.commit()
                  except DatabaseError:
                    print("Failed to insert %s, %s", linha['name'], linha_nome['sexo'])
          if temNaLista == False:
            for linha_nome2 in names2:
              if temNaLista == False and isEqual(name_complete[0], linha_nome2['name']):
                temNaLista = True
                try:
                  insert(cursor, linha['name'], linha_nome2['gender'], 'N')
                  cnx.commit()
                except DatabaseError:
                  print("Failed to insert %s, %s", linha['name'], linha_nome2['gender'])
          tem_ia = False
          if temNaLista == False:
            with open('authors_ia.csv', newline='') as csvfile_ia:
              authors_ia = list(csv.DictReader(csvfile_ia))
              for linha_ia in authors_ia:
                if linha['name'] == linha_ia['Name']:
                  try:
                    insert(cursor, linha['name'], linha_ia['gender'], 'S')
                    cnx.commit()
                    tem_ia = True
                  except DatabaseError:
                    print("Failed to insert %s, %s", linha['name'], linha_nome2['gender'])
              if tem_ia == False:
                try:
                  insert(cursor, linha['name'], NULL, 'S')
                  cnx.commit()
                except DatabaseError:
                  print("Failed to insert %s, %s", linha['name'], linha_nome2['gender'])
              else:
                tem_ia = False
          
      counter = counter - 1
    except IOError:
      print("Quebrou no ano:", counter)
      cursor.close()  
      cnx.close()
      break