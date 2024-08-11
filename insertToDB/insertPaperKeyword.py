import os
from sqlite3 import DatabaseError
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import csv

from pymysql import NULL

load_dotenv()

def insert(cursor, word, title, year):
  query = ("INSERT INTO PaperKeyword (keyword_id, paper_id)"
           "SELECT k.id, p.id "
           "FROM Keyword k "
           "JOIN Paper p ON p.title = %s " 
           "AND p.year = %s"
           "WHERE k.word = %s ")
  data_query = (title, year, word)

  print(title, word, year)
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
    filename_keywords = f'../database/{counter}/keywords.csv'
    filename_papers = f'../database/{counter}/titles.csv'
    try:
      titles = []
      temNaLista = []
      ult_id = "0"
      with open(filename_papers, newline='') as csvfile:
        titles = list(csv.DictReader(csvfile))
      with open(filename_keywords, newline='') as csvfile:
        content_file = list(csv.DictReader(csvfile))
        for i, linha in enumerate(content_file):
          if linha['id_paper'] != ult_id:
            temNaLista = []
          for linha_title in titles:
            if linha['id_paper'] == linha_title['id']:
              try:
                print(temNaLista)
                if linha['keyword'].upper() not in temNaLista:
                  insert(cursor, linha['keyword'], linha_title['title'], linha_title['year'])
                  cnx.commit()
                  temNaLista.append(linha['keyword'].upper())
              except DatabaseError:
                print("Failed to insert %s, %s", linha['name'], linha_title['title'])
          ult_id = linha['id_paper']
          if len(temNaLista) == 0:
            print("Não encontrou relação keyword e paper: title: %s, keyword: %s" % linha_title['title'], linha['keyword'])
      counter = counter - 1
    except IOError:
      print("Quebrou no ano:", counter)
      cursor.close()
      cnx.close()
      break