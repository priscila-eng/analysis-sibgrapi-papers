import os
from sqlite3 import DatabaseError
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import csv
import argostranslate.package
import argostranslate.translate
from unidecode import unidecode
import Levenshtein

from_code = "en"
to_code = "pt"

# Download and install Argos Translate package
argostranslate.package.update_package_index()
available_packages = argostranslate.package.get_available_packages()
package_to_install = next(
    filter(
        lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
    )
)
argostranslate.package.install_from_path(package_to_install.download())

load_dotenv()

def insertUniversity(cursor, id, description, sigla, in_ia):
  if in_ia == "S":
    query = ("INSERT INTO University "
          "(id, description, states_id, IN_IA) "
          "VALUES (%s, %s, (SELECT id FROM States WHERE sigla = %s), 'S')")
  else:
    query = ("INSERT INTO University "
          "(id, description, states_id, IN_IA) "
          "VALUES (%s, %s, (SELECT id FROM States WHERE sigla = %s), 'N')")
          
  data_query = (id, description, sigla)

  cursor.execute(query, data_query)

def getInDatabase(cursor, origem):
  if origem == "pt":
    query = ("select description from University where states_id not in (28) OR states_id is NULL")
  else:
    query = ("select description from University where states_id = 28")

  cursor.execute(query)
  
  return cursor.fetchall()

def temNaLista(lista, text, translator):
  if len(lista) == 0:
    return False
  
  filtrada = [palavra for palavra in lista if palavra.startswith(text[0])]

  if translator != "IN":
    for linha in filtrada:
      clean_text = unidecode(argostranslate.translate.translate(text, from_code, to_code)).upper()
      clean_linha = unidecode(argostranslate.translate.translate(linha, from_code, to_code)).upper()
      if text[1] == linha[1]: 
        if clean_text == clean_linha:
          return True
      elif text[1] < linha[1]:
        return False

  else:
    for linha in filtrada:
      clean_text = unidecode(text).upper()
      clean_linha = unidecode(linha).upper()
      if text[1] == linha[1]: 
        if clean_text == clean_linha:
          return True
      elif text[1] < linha[1]:
        return False
  return False
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
  filename = './universitiesStates.csv'
  file_name = "./universities.csv"
  universities_list = []
  universities_in = []
  id = 1680
  
  return_query = getInDatabase(cursor, 'pt')
  for item in return_query:
    universities_list.append(item[0])

  return_query = getInDatabase(cursor, 'in')
  for item in return_query:
    universities_in.append(item[0])
  
  universities_in.sort()
  universities_list.sort()

  with open(filename, newline='') as csvfile:
    universities = list(csv.DictReader(csvfile))
    aux = "LCG - Laboratório de Computaçāo Gràfica, COPPE - Sistemas/UFRJ, Rio de Janeiro, RJ, Brasil"
    for linha in universities:
      print(id, linha["description"], linha['IA'])
      if linha['estado'] != 'Internacional':
        if unidecode(linha['description']).upper()[0] != unidecode(aux).upper()[0] or aux == "":
          distance = Levenshtein.distance(unidecode(linha['description']).upper(), unidecode(aux).upper())
          if distance > 0 :
            if temNaLista(universities_list, linha['description'], "pt") == False:
              universities_list.append(linha['description'])
              aux = linha['description']
              insertUniversity(cursor, id, linha['description'], linha['sigla'], linha['IA'])
              cnx.commit()
              universities_list.sort()
              id += 1
      else:
        if temNaLista(universities_in, linha['description'], "IN") == False:
          universities_in.append(linha['description'])
          insertUniversity(cursor, id, linha['description'], "IN", linha['IA'])
          cnx.commit()
          universities_in.sort()
          id += 1

   