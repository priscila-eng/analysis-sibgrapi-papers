import os
from sqlite3 import DatabaseError
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import csv
from unidecode import unidecode

from mysql.connector import Error

from pymysql import NULL

load_dotenv()

def insert(cursor, word, title, year):

  title_space = title.rstrip()

  query = ("INSERT INTO PaperKeyword (keyword_id, paper_id)"
           "SELECT k.id, p.id "
           "FROM Keyword k "
           "JOIN Paper p ON p.title like %s " 
           "AND p.year like %s"
           "WHERE k.word like %s ")
  data_query = (title_space, year, word)

  cursor.execute(query, data_query)

  if cursor.rowcount == 0:
    query = ("INSERT INTO PaperKeyword (keyword_id, paper_id)"
           "SELECT k.id, p.id "
           "FROM Keyword k "
           "JOIN Paper p ON p.title like %s " 
           "AND p.year like %s"
           "WHERE k.word like %s ")
    
    data_query = (title_space, year, f"%{word}%")

    cursor.execute(query, data_query)

    if cursor.rowcount == 0:
      query = ("INSERT INTO PaperKeyword (keyword_id, paper_id) "
              "SELECT k.id, p.id "
              "FROM Keyword k "
              "JOIN Paper p ON p.title LIKE %s "
              "AND p.year LIKE %s "
              "WHERE %s LIKE CONCAT('%', k.word, '%')"
            )
      data_query = (title_space, year, word)
      cursor.execute(query, data_query)
      if cursor.rowcount == 0:
        log_list.append([title_space, word, year, cursor.rowcount])



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
  
  log_list = []
  while True:
    print("Processando o ano: ", counter)
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
                aux1 = unidecode(linha['keyword']).upper()
                if aux1 not in temNaLista:
                  insert(cursor, aux1, linha_title['title'], linha_title['year'])
                  cnx.commit()
                  temNaLista.append(aux1)
              except DatabaseError:
                print("Failed to insert %s, %s", linha['name'], linha_title['title'])
              except Error:
                if errorcode.ER_DUP_ENTRY:
                  if len(log_list) > 0:
                    log_list.pop()
          ult_id = linha['id_paper']
#          if len(temNaLista) == 0:
#            print("Não encontrou relação keyword e paper: title: %s, keyword: %s" % (linha_title['title'], aux1))

      with open('./log_paper_keywords.csv', 'w', newline='') as file2:
        writer = csv.writer(file2)
        writer.writerows(log_list)

      counter = counter - 1
    except IOError:

      print("Quebrou no ano:", counter)
      cursor.close()
      cnx.close()
      break