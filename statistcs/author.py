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


categorias = ['Male', 'Female', 'Unknown gender']

quantidades = [getMale(cursor), 
               getFemale(cursor),
               getWithOutGender(cursor)]

total = getAll(cursor)

# Plotar gráfico de barrasGênero
plt.figure(figsize=(10, 6))
bars = plt.bar(categorias, quantidades, color='skyblue')
plt.xlabel('Gender', fontweight='bold')
plt.ylabel('Number of authors', fontweight='bold')
plt.title('Distribution of authors by gender')
plt.xticks(rotation=0)
plt.tight_layout()

# Adicionar valores no topo das barras
for bar, qt in zip(bars, quantidades):
  percent = (qt / total) * 100
  yval = bar.get_height()
  plt.text(bar.get_x() + bar.get_width()/2.0, yval + 1, f"{percent:.1f}%", ha='center', va='bottom')

plt.show()

closeConnection(cursor)