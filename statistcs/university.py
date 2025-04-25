import mysql.connector
import pandas as pd
import os
import seaborn as sns
from dotenv import load_dotenv
import matplotlib.pyplot as plt

load_dotenv()

# conexão com o banco
cnx = mysql.connector.connect(
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    database=os.getenv("DATABASE_NAME")
)
cursor = cnx.cursor()

command = input("Digite um comando: ")

if command == "1":
    query = """
    SELECT 
    r.description AS region,
    s.description AS state,
    COUNT(u.id) AS university_count
    FROM University u
    JOIN States s ON u.states_id = s.id
    JOIN Region r ON s.region_id = r.id
    GROUP BY r.description, s.description
    ORDER BY r.description, s.description;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    # transforma em DataFrame
    df = pd.DataFrame(results, columns=["Region", "State", "University Count"])

    # gráfico
    plt.figure(figsize=(16, 10))
    ax = sns.barplot(data=df, x="State", y="University Count", hue="Region")
    plt.xticks(rotation=45)
    # Adiciona os valores em cima das barras
    for container in ax.containers:
        ax.bar_label(container, fmt='%.0f', label_type='edge', padding=3)
    plt.title("Number of Universities per State and Region")
    plt.tight_layout()
    plt.show()
elif command == "2":
    query = """
    SELECT 
    r.description AS region,
    s.description AS state,
    COUNT(DISTINCT pa.paper_id) AS paper_count
    FROM PaperAuthor pa
    JOIN Author a ON pa.author_id = a.id
    JOIN University u ON a.author_university = u.id
    JOIN States s ON u.states_id = s.id
    JOIN Region r ON s.region_id = r.id
    GROUP BY r.description, s.description
    ORDER BY r.description, s.description;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    # dataframe
    df = pd.DataFrame(results, columns=["Region", "State", "Paper Count"])

    # gráfico
    plt.figure(figsize=(14, 8))
    ax = sns.barplot(data=df, x="State", y="Paper Count", hue="Region")
    plt.xticks(rotation=45, ha='right')
    for container in ax.containers:
        ax.bar_label(container, fmt='%.0f', label_type='edge', padding=3)
    plt.title("Number of Papers per State and Region")
    plt.tight_layout()
    plt.show()
elif command == "3":
    # executa a query
    query = """
    SELECT 
    p.year,
    r.description AS region,
    s.description AS state,
    COUNT(DISTINCT pa.paper_id) AS paper_count
    FROM PaperAuthor pa
    JOIN Paper p ON pa.paper_id = p.id
    JOIN Author a ON pa.author_id = a.id
    JOIN University u ON a.author_university = u.id
    JOIN States s ON u.states_id = s.id
    JOIN Region r ON s.region_id = r.id
    GROUP BY p.year, r.description, s.description
    ORDER BY p.year, r.description, s.description;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    # dataframe
    df = pd.DataFrame(results, columns=["Year", "Region", "State", "Paper Count"])
    df["Year"] = df["Year"].astype(int)

    # gráfico de linha: crescimento por região
    plt.figure(figsize=(14, 8))
    sns.lineplot(data=df, x="Year", y="Paper Count", hue="Region", marker="o")
    plt.title("Growth of Paper Publications by Region Over the Years")
    plt.ylabel("Number of Papers")
    plt.xlabel("Year")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
elif command == "4":
    # executa a query
    query = """
    SELECT 
    p.year,
    r.description AS region,
    COUNT(DISTINCT pa.paper_id) AS paper_count
    FROM PaperAuthor pa
    JOIN Paper p ON pa.paper_id = p.id
    JOIN Author a ON pa.author_id = a.id
    JOIN University u ON a.author_university = u.id
    JOIN States s ON u.states_id = s.id
    JOIN Region r ON s.region_id = r.id
    GROUP BY p.year, r.description
    ORDER BY p.year, r.description;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    # dataframe
    df = pd.DataFrame(results, columns=["Year", "Region", "Paper Count"])
    df["Year"] = df["Year"].astype(int)

    # gráfico de barras agrupadas
    plt.figure(figsize=(16, 9))
    sns.barplot(data=df, x="Year", y="Paper Count", hue="Region", width=1.1)
    plt.title("Number of Papers per Year by Region")
    plt.ylabel("Number of Papers")
    plt.xlabel("Year")
    plt.xticks(rotation=45)
    plt.legend(title="Region")
    plt.tight_layout()
    plt.show()
