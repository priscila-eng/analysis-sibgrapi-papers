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
            "WHERE IN_IA = 'S'" )
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


categorias = ['Masculino', 'Feminino', 'Gênero desconhecido']

quantidades = [getMale(cursor), 
               getFemale(cursor),
               getWithOutGender(cursor)]

total = getAll(cursor)

cores = ["#1E90FF", "#DC143C", "#808080"]

# Plotar gráfico de barrasGênero
plt.figure(figsize=(10, 10))

percentuais = [q / total * 100 for q in quantidades]

bars = plt.pie(quantidades, 
               labels=categorias, 
               colors=cores, 
               autopct='%1.1f%%', 
              #  startangle=, 
               wedgeprops={'edgecolor': 'white'}, 
                # pctdistance=1,
                labeldistance=1,
               textprops={'fontsize': 16})
labels_legenda = [
    f"{l}\n{p:.1f}%" for l, p in zip(categorias, percentuais)
]

# plt.legend(
#     labels_legenda,
#     loc='center left',
#     bbox_to_anchor=(1, 0.5),
#     frameon=False
# )

# plt.xlabel('Gênero', fontweight='bold')
# plt.ylabel('Número de autores', fontweight='bold')
# plt.title('Distribuição de autores por gênero')
plt.xticks(rotation=0)
plt.tight_layout()

# Adicionar valores no topo das barras
# for bar, qt in zip(bars, quantidades):
#   percent = (qt / total) * 100
#   yval = bar.get_height()
#   plt.text(bar.get_x() + bar.get_width()/2.0, yval + 1, f"{percent:.1f}%", ha='center', va='bottom')

plt.show()

closeConnection(cursor)