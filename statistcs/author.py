import os
import mysql.connector
from dotenv import load_dotenv
import matplotlib.pyplot as plt

from pymysql import NULL

load_dotenv()

def getAll(cursor):
  
  query = ("SELECT count(*) FROM Author ")
  cursor.execute(query)
  result = cursor.fetchone()
  return result[0]

def getFemale(cursor):
  
  query = ("SELECT count(*) FROM Author "
            "WHERE gender = 'F' " )
  cursor.execute(query)
  result = cursor.fetchone()
  return result[0]

def getMale(cursor):
  query = ("SELECT count(*) FROM Author "
            "WHERE gender = 'M' " )

  cursor.execute(query)
  result = cursor.fetchone()
  return result[0]

def getInIA(cursor):
  query = ("SELECT count(*) FROM Author "
            "WHERE IN_IA = 'S' " )
  cursor.execute(query)
  result = cursor.fetchone()
  return result[0]

def getWithOutGender(cursor):
  query = ("SELECT count(*) FROM Author "
            "WHERE gender is NULL " )

  cursor.execute(query)
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

cursor = cnx.cursor()

categorias = ['Total', 'Masculino', 'Feminino', 'Encontrados por IA', 'Sem gênero']

quantidades = [getAll(cursor), 
               getMale(cursor), 
               getFemale(cursor), 
               getInIA(cursor), 
               getWithOutGender(cursor)]

# Plotar gráfico de barras
plt.figure(figsize=(10, 6))
bars = plt.bar(categorias, quantidades, color='skyblue')
plt.xlabel('Categoria')
plt.ylabel('Quantidade de Autores')
plt.title('Quantitativo de Autores por Categoria')
plt.xticks(rotation=45)
plt.tight_layout()

# Adicionar valores no topo das barras
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 1, int(yval), ha='center', va='bottom')

plt.show()

closeConnection()