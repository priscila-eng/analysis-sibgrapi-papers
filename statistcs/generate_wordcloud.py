import os
import mysql.connector
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from wordcloud import WordCloud

load_dotenv()

cnx = mysql.connector.connect(
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    database=os.getenv("DATABASE_NAME")
)

cursor = cnx.cursor()

periodos = {
    1: (1988, 1994),
    2: (1995, 2001),
    3: (2002, 2009),
    4: (2010, 2016),
    5: (2017, 2023)
}

print("Escolha o período:")
for chave, (inicio, fim) in periodos.items():
    print(f"{chave} - {inicio} a {fim}")

opcao = int(input("\nDigite a opção desejada: "))

if opcao not in periodos:
    print("Período inválido!")
    exit()

inicio, fim = periodos[opcao]

query = """
SELECT
    LOWER(k.Word) AS keyword,
    COUNT(*) AS freq
FROM PaperKeyword pk
JOIN Paper p ON pk.paper_id = p.id
JOIN Keyword k ON pk.keyword_id = k.id
WHERE p.year BETWEEN %s AND %s
GROUP BY LOWER(k.Word)
ORDER BY freq DESC;
"""

cursor.execute(query, (inicio, fim))
resultados = cursor.fetchall()

frequencias = {
    palavra.title(): freq
    for palavra, freq in resultados
}

wc = WordCloud(
    width=1800,
    height=1000,
    background_color="white",
    colormap="viridis",
    max_words=100,
    random_state=42,
    collocations=False
).generate_from_frequencies(frequencias)

plt.figure(figsize=(12, 7))
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.title(f"Período {inicio} a {fim}", fontsize=20)

plt.show()

cursor.close()
cnx.close()