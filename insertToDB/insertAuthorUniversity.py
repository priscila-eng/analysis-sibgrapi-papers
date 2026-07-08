import os
from mysql.connector import Error
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import csv
import argostranslate.package
import argostranslate.translate
from unidecode import unidecode
import Levenshtein

load_dotenv()

def insertUniversityAuthor(cursor, university, author):
  cursor.execute("SELECT id FROM Author WHERE Name = %s", (author, ))
  author_fetch = cursor.fetchone()
  print()
  if author_fetch:

    cursor.execute("SELECT id FROM University WHERE description LIKE %s ORDER BY id LIMIT 1", (university,))
    university_fetch = cursor.fetchone()

    if not university_fetch:
      return False
    
    university_id = university_fetch[0]
    author_id     = author_fetch[0]

    # Agora faz o UPDATE com o ID
    cursor.execute(
        "UPDATE Author SET author_university = %s WHERE id = %s",
        (university_id, author_id)
    )
    return True
  else:
    return False

counter = 2023

cnx = mysql.connector.connect(
  user=os.getenv("DATABASE_USER"),
  password=os.getenv("DATABASE_PASSWORD"),
  database=os.getenv("DATABASE_NAME")
)
cursor = cnx.cursor()
# ------------------------------------------------------------------------------------
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
# ------------------------------------------------------------------------------------
while True:
  k = 0
  university = f'../database/{counter}/university.csv'
  author = f'../database/{counter}/authors.csv'
  try:
    with open(university, newline='') as universitycsv:
      content_file_university = list(csv.DictReader(universitycsv))
      for i, linha in enumerate(content_file_university):
        name_author = " "
        with open(author, newline='') as authorcsv:
          content_file_author = list(csv.DictReader(authorcsv))
          j = 0
          found = False
          while(found is False):
            if content_file_author[j]['id'] == linha['id_author']:
              name_author = content_file_author[j]['name']
              found = True
            else:
              j += 1
        if not insertUniversityAuthor(cursor, linha['university'], name_author):
          text_modified = " ".join([f"%{palavra}%" for palavra in linha['university'].split()])
          if not insertUniversityAuthor(cursor, text_modified, name_author):
            keyword = "University"
            index = linha['university'].find(keyword)
            if index == -1:
              keyword = "Universidade"
              index = linha['university'].find(keyword)
            if index == -1:
              keyword = "UF"
              index = linha['university'].find(keyword)
            if index != -1:
              text_modified = " ".join([f"%{palavra}%" for palavra in linha['university'][index:].split()])
              if not insertUniversityAuthor(cursor, text_modified, name_author):
                text_translate = unidecode(argostranslate.translate.translate(linha['university'], from_code, to_code)).upper()
                text_modified = " ".join([f"%{palavra}%" for palavra in text_translate.split()])
                if not insertUniversityAuthor(cursor, text_modified, name_author):
                  if counter == 2020 and (linha['id_author'] == "21" or linha['id_author'] == "22"):
                    k += 1
                  else:
                    print("TRADUZIR FALHOU FALHOU")
                    print(linha["id_author"], linha["university"], text_translate, text_modified)
                else:
                  k += 1
                  cnx.commit()
              else:
                k += 1
                cnx.commit()
            else:
              text_translate = unidecode(argostranslate.translate.translate(linha['university'], from_code, to_code)).upper()
              text_modified = " ".join([f"%{palavra}%" for palavra in text_translate.split()])
              if not insertUniversityAuthor(cursor, text_modified, name_author):
                print("TRADUZIR FALHOU FALHOU")
                print(linha["id_author"], linha["university"], text_translate, text_modified)
              else:
                k += 1
                cnx.commit()
          else:
            k += 1
            cnx.commit()
        else:
          k += 1
          cnx.commit()
      print(f"Processamento do ano {counter}: {k} atualizações")
      counter -= 1
  except IOError:
      print("Quebrou no ano:", counter)
      cursor.close()  
      cnx.close()
      break 