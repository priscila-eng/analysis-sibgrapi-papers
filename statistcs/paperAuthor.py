import os
import mysql.connector
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import numpy as np

from pymysql import NULL

load_dotenv()

def getAll(cursor):
  
  query = ("SELECT count(*) FROM Paper A WHERE A.id IN (SELECT B.paper_id FROM PaperAuthor B);")
  cursor.execute(query)
  result = cursor.fetchone()
  return result[0]

def getPapersWithWomen(cursor):
  
  query = ("SELECT COUNT(DISTINCT pa.paper_id) AS papers_with_women "
            "FROM PaperAuthor pa "
            "JOIN Author a ON pa.author_id = a.id "
            "WHERE a.gender = 'F'")
  cursor.execute(query)
  result = cursor.fetchone()
  return result[0]

def getPapersWithWomenByYear(cursor, year):
  
  query = ("SELECT COUNT(DISTINCT pa.paper_id) AS papers_with_women "
            "FROM PaperAuthor pa "
            "JOIN Author a ON pa.author_id = a.id "
            "JOIN Paper p ON pa.paper_id = p.id "
            "WHERE a.gender = 'F' AND p.year = %s;")
  query_data = (year,)
  cursor.execute(query, query_data)
  result = cursor.fetchone()
  return result[0]

def getPapersNoneGenderByYear(cursor, year):
  
  query = ("SELECT COUNT(DISTINCT pa.paper_id) AS papers_with_women "
            "FROM PaperAuthor pa "
            "JOIN Author a ON pa.author_id = a.id "
            "JOIN Paper p ON pa.paper_id = p.id "
            "WHERE a.gender is NULL AND p.year = %s;")
  query_data = (year,)
  cursor.execute(query, query_data)
  result = cursor.fetchone()
  return result[0]

def getAllByYear(cursor, year):
  query = ("SELECT count(*) FROM Paper A WHERE A.Year = %s AND A.id IN (SELECT B.paper_id FROM PaperAuthor B);")
  query_data = (year,)
  cursor.execute(query, query_data)
  result = cursor.fetchone()
  return result[0]

def closeConnection(cursor):
# Fechar conexão
    cursor.close()

cnx = mysql.connector.connect(
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    database=os.getenv("DATABASE_NAME")
)

# TODO:fazer gráfico por genero e ano, colocar linha de evolução. Fazer das universidades.
command = input("Digite um comando: ")
years = [str(year) for year in range(2023, 1987, -1)]
cursor = cnx.cursor()

if command == "1":  
  categories = ["Participação de mulheres"]

  quantities = [getAll(cursor), getPapersWithWomen(cursor)]

  # Plotar gráfico de barras
  plt.figure(figsize=(10, 6))
  bars = plt.bar(categories, quantities, color='skyblue')
  plt.xlabel('Papers')
  plt.ylabel('Quantidade')
  plt.title('Quantidade de Papers com participação de mulheres')
  plt.xticks(rotation=45)
  plt.tight_layout()

  # Adicionar valores no topo das barras
  for bar in bars:
      yval = bar.get_height()
      plt.text(bar.get_x() + bar.get_width()/2.0, yval + 1, int(yval), ha='center', va='bottom')

  plt.show()
  
else:
  mens = [getAllByYear(cursor, str(year)) -
          getPapersWithWomenByYear(cursor, str(year)) -
          getPapersNoneGenderByYear(cursor, str(year)) for year in years
        ]
  womens = [getPapersWithWomenByYear(cursor, str(year)) for year in years]
  others = [getPapersNoneGenderByYear(cursor, str(year)) for year in years]

  # Posição no eixo x
  x = np.arange(len(years)) * 2
  largura = 0.6  # Largura de cada barra

  # Cria o gráfico
  fig, ax = plt.subplots()
  barras_homens = ax.bar(x - largura, mens, width=largura, label='Mens', color='skyblue')
  barras_mulheres = ax.bar(x, womens, width=largura, label='Womens', color='#FFD580')
  barras_others = ax.bar(x + largura, others, width=largura, label='Others', color='#A9A9A9')

  # Rótulos e título
  ax.set_xlabel('Ano')
  ax.set_ylabel('Quantidade de papers')
  ax.set_title("Evolution of women's participation")
  ax.set_xticks(x)
  ax.set_xticklabels(years)
  ax.legend()

  plt.tight_layout()
  plt.show()

closeConnection(cursor)