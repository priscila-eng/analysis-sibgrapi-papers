import os
import mysql.connector
from dotenv import load_dotenv
import pandas as pd

from pymysql import NULL

load_dotenv()

def getRanking(cursor):
  query = ("""
            WITH KeywordRanking AS (
                SELECT 
                    p.year,
                    k.Word AS keyword,
                    COUNT(*) AS keyword_count,
                    ROW_NUMBER() OVER (PARTITION BY p.year ORDER BY COUNT(*) DESC) AS rank_position
                FROM PaperKeyword pk
                JOIN Paper p ON pk.paper_id = p.id
                JOIN Keyword k ON pk.keyword_id = k.id
                GROUP BY p.year, k.Word
            )
            SELECT 
                year,
                keyword,
                keyword_count,
                rank_position
            FROM KeywordRanking
            WHERE rank_position <= 10
            ORDER BY year, rank_position;
           """)
  cursor.execute(query)
  result = cursor.fetchall()
  return result

def closeConnection(cursor):
# Fechar conexão
    cursor.close()

cnx = mysql.connector.connect(
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    database=os.getenv("DATABASE_NAME")
)

cursor = cnx.cursor()

df = pd.DataFrame(getRanking(cursor), columns=["Year", "Keyword", "Keyword Count", "Rank"])

df["Keyword"] = df["Keyword"].str.lower().str.title()

df.to_csv("top_keywords_by_year.csv", index=False, encoding='utf-8')
closeConnection(cursor)