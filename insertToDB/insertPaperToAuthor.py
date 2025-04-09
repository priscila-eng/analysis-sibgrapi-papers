import os
from sqlite3 import DatabaseError
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import csv

from pymysql import NULL

load_dotenv()

def insert(cursor, name, title, year):
  query = ("INSERT INTO PaperAuthor (author_id, paper_id)"
           "SELECT a.id, p.id "
           "FROM Author a "
           "JOIN Paper p ON p.title = %s " 
           "AND p.year = %s"
           "WHERE a.name = %s ")  
  data_query = (title, year, name)

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
    print("Processando o ano:", counter)
    filename_authors_duplicate = f'../database/{counter}/author_without_duplicate.csv'
    filename_papers = f'../database/{counter}/titles.csv'
    if os.path.isfile(filename_authors_duplicate):
      filename_authors = filename_authors_duplicate
    else:
      filename_authors = f'../database/{counter}/authors.csv'
    try:
      titles = []
      with open(filename_papers, newline='') as csv_paper:
        titles = list(csv.DictReader(csv_paper))
      with open(filename_authors, newline='') as csv_author:
        content_file = list(csv.DictReader(csv_author))
        for i, linha in enumerate(content_file):
          temNaLista = False
          for linha_title in titles:
            if linha['id_paper'] == linha_title['id']:
              temNaLista = True
              if counter <= 1996:
                title_without_space = linha_title['title'][:-1]
              else:
                title_without_space = linha_title['title']
              try:
                insert(cursor, linha['name'], title_without_space, linha_title['year'])
                cnx.commit()
              except DatabaseError:
                print("Failed to insert %s, %s", linha['name'], linha_title['title'])
          if temNaLista == False:
            print("Não encontrou relação author e paper: title: %s, author: %s" % linha_title['title'], linha['name'])
      counter = counter - 1
    except IOError:
      print("Quebrou no ano:", counter)
      cursor.close()
      cnx.close()
      break