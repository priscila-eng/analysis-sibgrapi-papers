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

total = getAll(cursor)

years = [str(year) for year in range(1988, 2024)]

categories = [str(year) for year in range(1988, 2024)]

quantities = [getByYear(cursor, str(year)) for year in years]

# Plotar gráfico de barras
fig, ax = plt.subplots(figsize=(16,9))
bars = ax.bar(categories, quantities, color='skyblue')

x = [bar.get_x() + bar.get_width() / 2 for bar in bars]
y = [bar.get_height() for bar in bars]

plt.xlabel('Year', fontweight='bold')
plt.ylabel('Number of papers', fontweight='bold')
plt.title('Paper distribution over the years')
plt.xticks(rotation=45)
plt.tight_layout()

# Adicionar valores no topo das barras
for bar, qt in zip(bars, quantities):
  percent = (qt / total) * 100
  yval = bar.get_height()
  plt.text(bar.get_x() + bar.get_width()/2.0, yval + 1, f"{percent:.1f}%", ha='center', va='bottom', fontweight='bold')

ax.plot(x, y, color='red', marker='o', linestyle='-')

plt.show()

closeConnection(cursor)