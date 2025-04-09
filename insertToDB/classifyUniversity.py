import os
from sqlite3 import DatabaseError
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import csv
import re

from pymysql import NULL
from unidecode import unidecode
import Levenshtein

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
  estados = []
  municipios = []
  paises = []
  with open('estados.csv', newline='') as csvfile:
    estados = list(csv.DictReader(csvfile))
  
  with open('municipios-uf.csv', newline='') as csvfile:
    municipios = list(csv.DictReader(csvfile))
  
  with open('paises.csv', newline='') as csvfile:
    paises = list(csv.DictReader(csvfile))

  file_name = f"./universitiesStates.csv"
  lines = []
  while True:
    print("Processando o ano:", counter)
    filename = f'../database/{counter}/university.csv'
    try:
      with open(filename, newline='') as csvfile:
        content_file = list(csv.DictReader(csvfile))
        for i, linha in enumerate(content_file):
          temNaLista = False
          if(linha['university'] == 'NULL'):
            temNaLista = True
            lines.append(['NULL', 'Affiliation', None, None])
          if temNaLista == False:
            for linha_estados in estados:
              if linha_estados['SIGLA'] == 'DF':
                if 'Brasília' in linha['university'] or 'Bras??lia' in linha['university'] or 'CNPq' in linha['university']:
                  temNaLista = True
                  lines.append([linha['university'], linha_estados['NOME'], linha_estados['SIGLA'], linha_estados['REGIAO']])

              if temNaLista == False and re.search(fr"\b{linha_estados['SIGLA'].upper()}\b", linha['university'].upper()):
                temNaLista = True
                lines.append([linha['university'], linha_estados['NOME'], linha_estados['SIGLA'], linha_estados['REGIAO']])

              if temNaLista == False and re.search(fr"\b{unidecode(linha_estados['NOME'])}\b", unidecode(linha['university'])):
                temNaLista = True
                lines.append([linha['university'], linha_estados['NOME'], linha_estados['SIGLA'], linha_estados['REGIAO']])

            if temNaLista == False:
              for linhaMunicipios in municipios:
                if temNaLista == False and re.search(fr"\b{unidecode(linhaMunicipios['MUNICIPIO']).upper()}\b", unidecode(linha['university']).upper()):
                  result = [d for d in estados if linhaMunicipios['UF'] in d.values()]
                  lines.append([linha['university'], result[0]['NOME'], result[0]['SIGLA'], result[0]['REGIAO']])
                  temNaLista = True
            
            if temNaLista == False:
              if ('Fluminense' in linha['university'] or 
                  'PUC-Rio' in linha['university'] or
                  'IMPA' in linha['university'] or
                  'COPPE' in linha['university'] or
                  'Instituto Nacional de Matemática Pura e Aplicada' in linha['university'] or
                  re.search(fr"\b{unidecode('UERJ').upper()}\b", unidecode(linha['university']).upper()) or
                  'Instituto de Matemática Pura e Aplicada' in linha['university'] or
                  'IME' in linha['university']):
                temNaLista = True
                lines.append([linha['university'], 'Rio de Janeiro', 'RJ', 'Sudeste'])

              if ('unico - idTech' in linha['university'] or 
                  'Federal University of ABC' in linha['university'] or 
                  'Universidade Federal do ABC' in linha['university'] or
                  'USP' in linha['university'] or
                  'Embrapa Instrumentação' in linha['university'] or
                  'UNICAMP' in linha['university'] or
                  'INPE' in linha['university'] or
                  'ITA' in linha['university'] or
                  'National Institute for Space Research' in linha['university'] or
                  re.search(fr"\b{unidecode('FEEC').upper()}\b", unidecode(linha['university']).upper())):
                temNaLista = True
                lines.append([linha['university'], 'São Paulo', 'SP', 'Sudeste'])

              if ('FURG' in linha['university'] or
                  'UFRGS' in linha['university'] or
                  'UNISINOS' in linha['university'].upper() or
                  'UNIPAMPA' in linha['university'] or
                  'Sao Lepoldo' in linha['university']):
                temNaLista = True
                lines.append([linha['university'], 'Rio Grande do Sul', 'RS', 'Sul'])

              if ('Triângulo Mineiro' in linha['university'] or 
                  'Universidade Federal de Minas' in linha['university'] or
                  'PUC Minas' in linha['university'] or
                  '(VIPLAB)' in linha['university'] or
                  re.search(fr"\b{unidecode('UFMG').upper()}\b", unidecode(linha['university']).upper()) or
                  'Jos do Rosrio Vellano University' in linha['university'] or
                  'ICEB UFOP' in linha['university'] or
                  re.search(fr"\b{unidecode('CDTN').upper()}\b", unidecode(linha['university']).upper())):
                temNaLista = True
                lines.append([linha['university'], 'Minas Gerais', 'MG', 'Sudeste'])

              if ('Paranaense' in linha['university'] or
                  'Institutos Lactec' in linha['university'] or
                  re.search(fr"\b{unidecode('UEM').upper()}\b", unidecode(linha['university']).upper())):
                temNaLista = True
                lines.append([linha['university'], 'Paraná', 'PR', 'Sul'])

              if ('Instituto Federal do Espírito' in linha['university']):
                temNaLista = True
                lines.append([linha['university'], 'Espírito Santo', 'ES', 'Sudeste'])

              if (re.search(fr"\b{unidecode('UFBA').upper()}\b", unidecode(linha['university']).upper())):
                temNaLista = True
                lines.append([linha['university'], 'Bahia', 'BA', 'Nordeste'])
              
              if (re.search(fr"\b{unidecode('UFFS').upper()}\b", unidecode(linha['university']).upper())):
                temNaLista = True
                lines.append([linha['university'], 'Santa Catarina', 'SC', 'Sul'])
              
              if (re.search(fr"\b{unidecode('UFAL').upper()}\b", unidecode(linha['university']).upper())):
                temNaLista = True
                lines.append([linha['university'], 'Alagoas', 'AL', 'Nordeste'])
              
              if ('Faculdade de Ciência e Tecnologia-FCT' in linha['university']):
                temNaLista = True
                lines.append([linha['university'], 'Goiás', 'GO', 'Centro-Oeste'])
            
              if (re.search(fr"\b{unidecode('UFPE').upper()}\b", unidecode(linha['university']).upper())):
                temNaLista = True
                lines.append([linha['university'], 'Pernambuco', 'PE', 'Nordeste'])
              
              if (re.search(fr"\b{unidecode('UFPB').upper()}\b", unidecode(linha['university']).upper())):
                temNaLista = True
                lines.append([linha['university'], 'Paraíba', 'PB', 'Nordeste'])
          
            if temNaLista == False:
              for pais in paises:
                if temNaLista == False and unidecode(pais['Nome']).upper() in unidecode(linha['university']).upper():
                  temNaLista = True
                  lines.append([linha['university'], 'Internacional', None, None])
            
            if temNaLista == False:
              if ('Chicago' in linha['university'] or
                  'New York' in linha['university'] or
                  'Massachusetts' in linha['university'] or
                  'Japan' in linha['university'] or
                  'USA' in linha['university'] or
                  'Switzerland' in linha['university'] or
                  'Italy' in linha['university'] or
                  'United Kingdom' in linha['university'] or
                  'Taiwan' in linha['university'] or
                  'Netherlands' in linha['university'] or
                  'Germany' in linha['university'] or
                  'France' in linha['university'] or
                  'Paris' in linha['university'] or
                  'Spain' in linha['university'] or
                  'Norway' in linha['university'] or
                  'London' in linha['university'] or
                  'Uruguay' in linha['university'] or
                  'Groningen' in linha['university'] or
                  'Asuncion' in linha['university'] or
                  'Czech' in linha['university'] or
                  'Turkey' in linha['university'] or
                  'Guildford' in linha['university'] or
                  'Ireland' in linha['university'] or
                  'Bourgogne' in linha['university'] or
                  'Calgary' in linha['university'] or
                  ', UK' in linha['university'] or
                  'Antwerp' in linha['university'] or
                  'Korea' in linha['university'] or
                  'Poland' in linha['university'] or
                  'Dentistry' in linha['university'] or
                  'Belgium' in linha['university'] or
                  'Brown University' in linha['university'] or
                  'Egypt' in linha['university'] or
                  'Coimbra' in linha['university'] or
                  'Paraguay' in linha['university'] or
                  'Toronto' in linha['university'] or
                  'Denmark' in linha['university'] or
                  'Sweden' in linha['university'] or
                  'Singapore' in linha['university'] or
                  'United States' in linha['university'] or
                  'Instituto Tecnologico Informatica'.upper() in unidecode(linha['university']).upper() or
                  'Buenos Aires' in linha['university'] or
                  'Greece' in linha['university'] or
                  'Amsterdam' in linha['university'] or
                  'Waterloo' in linha['university'] or
                  'Louvain' in linha['university'] or
                  re.search(fr"\b{unidecode('ESIEE').upper()}\b", unidecode(linha['university']).upper()) or
                  'York' in linha['university'] or
                  'Hiroshima' in linha['university'] or
                  'Edinburgh' in linha['university'] or
                  'University of Berne' in linha['university'] or
                  'Lisboa' in linha['university'] or
                  'Arizona State' in linha['university'] or
                  'Universidad de Tarapacá' in linha['university'] or
                  'Kent at Canterbury' in linha['university'] or
                  'University of Southampton' in linha['university'] or
                  'Manchester' in linha['university'] or
                  'Pennsylvania' in linha['university'] or
                  re.search(fr"\b{unidecode('EID').upper()}\b", unidecode(linha['university']).upper())):
                temNaLista = True
                lines.append([linha['university'], 'Internacional', None, None])
            
            if temNaLista == False:
              lines.append([linha['university'], None, None, None])

            with open(file_name, 'w', newline='') as file:
              writer = csv.writer(file)
              writer.writerows(lines)
      counter = counter - 1
    except IOError:
      print("Quebrou no ano:", counter)
      cursor.close()
      cnx.close()
      break