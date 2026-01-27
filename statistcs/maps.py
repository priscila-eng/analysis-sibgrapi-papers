import os
import mysql.connector
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px
import requests
import plotly.io as pio



load_dotenv()

def getAll(cursor):
  
  query = ("""SELECT 
    s.sigla AS estado,
    COUNT(DISTINCT pa.paper_id) AS Papers
        FROM PaperAuthor pa
        JOIN Paper p ON pa.paper_id = p.id
        JOIN Author a ON pa.author_id = a.id
        JOIN University u ON a.author_university = u.id
        JOIN States s ON u.states_id = s.id
        GROUP BY s.sigla
        ORDER BY Papers DESC;""")
  cursor.execute(query)
  results = cursor.fetchall()
  return results


def closeConnection(cursor):
# Fechar conexão
    cursor.close()

cnx = mysql.connector.connect(
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    database=os.getenv("DATABASE_NAME")
)

cursor = cnx.cursor()

df = pd.DataFrame(getAll(cursor), columns=["estado", "Artigos"])

url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
geojson = requests.get(url).json()

# Criar mapa
fig = px.choropleth(
    df,
    geojson=geojson,
    locations="estado",                # coluna do DataFrame
    featureidkey="properties.sigla",   # chave do GeoJSON
    color="Artigos",               # coluna para colorir
    color_continuous_scale="OrRd",
    title="Mapa do Brasil da quantidade de artigos"
)

pio.renderers.default = "browser"
fig.update_geos(fitbounds="locations", visible=False)
fig.show()


closeConnection(cursor)