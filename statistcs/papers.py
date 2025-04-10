import os
import mysql.connector
from dotenv import load_dotenv
import matplotlib.pyplot as plt

from pymysql import NULL

load_dotenv()

def getAll(cursor):
  
  query = ("SELECT count(*) FROM Paper A WHERE A.id IN (SELECT B.paper_id FROM PaperAuthor B);")
  cursor.execute(query)
  result = cursor.fetchone()
  return result[0]

def getByYear(cursor, year):
  
  query = ("SELECT count(*) FROM Paper A WHERE A.year = %s AND A.id IN (SELECT B.paper_id FROM PaperAuthor B);")
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

cursor = cnx.cursor()


years = [str(year) for year in range(2023, 1987, -1)]

categories = ["Total"] + [str(year) for year in range(2023, 1987, -1)]

quantities = [getAll(cursor)] + [getByYear(cursor, str(year)) for year in years]

# Plotar gráfico de barras
plt.figure(figsize=(10, 6))
bars = plt.bar(categories, quantities, color='skyblue')
plt.xlabel('Total e Anos')
plt.ylabel('Quantidade de Papers')
plt.title('Quantitativo de Papers por Ano')
plt.xticks(rotation=45)
plt.tight_layout()

# Adicionar valores no topo das barras
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 1, int(yval), ha='center', va='bottom')

plt.show()

closeConnection(cursor)