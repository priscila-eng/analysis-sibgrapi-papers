import mysql.connector
import pandas as pd
import os
import seaborn as sns
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import numpy as np

load_dotenv()

# conexão com o banco
cnx = mysql.connector.connect(
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    database=os.getenv("DATABASE_NAME")
)
cursor = cnx.cursor()

command = input("Digite um comando: ")

# TODO: Trocar universidade para filiação


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
    df = pd.DataFrame(results, columns=["Região", "Estado", "Artigo"])

    # gráfico
    plt.figure(figsize=(20, 10))
    plt.legend(
      loc='upper center',
      bbox_to_anchor=(0.5, -0.1),
      ncol=3,
      frameon=True,
      fontsize=16
    )
    ax = sns.barplot(data=df, x="Estado", y="Artigo", hue="Região")
    plt.xticks(rotation=45, ha='right')

    for container in ax.containers:
        ax.bar_label(container, fmt='%.0f', label_type='edge', padding=3, fontsize=16)

    ax.tick_params(axis='both', labelsize=16)
    ax.set_xlabel("Estado", fontsize=16)
    ax.set_ylabel("Artigo", fontsize=16)
    # plt.title("Número de artigos por estado e região")
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
    plt.figure(figsize=(20, 10))
    plt.legend(
      loc='upper center',
      bbox_to_anchor=(0.5, -0.1),
      ncol=3,
      frameon=True,
      fontsize=16
    )
    sns.lineplot(data=df, x="Year", y="Paper Count", hue="Region", marker="o")
    # plt.title("Distribuição de artigos por região ao longo dos anos")
    plt.ylabel("Número de artigos", fontsize=16)
    plt.xlabel("Ano", fontsize=16)
    plt.tick_params(axis='both', labelsize=16)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
# Separar por regiao    
elif command == "4":
    region = input("Digite a região: ")
    #Centro-Oeste
    if region == "1":
        query = """
                SELECT 
                p.year,
                COUNT(DISTINCT pa.paper_id) AS paper_count
                FROM PaperAuthor pa
                JOIN Paper p ON pa.paper_id = p.id
                JOIN Author a ON pa.author_id = a.id
                JOIN University u ON a.author_university = u.id
                JOIN States s ON u.states_id = s.id
                JOIN Region r ON s.region_id = r.id
                WHERE r.description = "Centro-Oeste"
                GROUP BY p.year, r.description
                ORDER BY p.year, r.description;
                """
    #Mundo
    elif region == "2":
        query = """
                SELECT 
                p.year,
                COUNT(DISTINCT pa.paper_id) AS paper_count
                FROM PaperAuthor pa
                JOIN Paper p ON pa.paper_id = p.id
                JOIN Author a ON pa.author_id = a.id
                JOIN University u ON a.author_university = u.id
                JOIN States s ON u.states_id = s.id
                JOIN Region r ON s.region_id = r.id
                WHERE r.description = "Mundo"
                GROUP BY p.year, r.description
                ORDER BY p.year, r.description;
                """
    # Nordeste
    elif region == "3":
        query = """
                SELECT 
                p.year,
                COUNT(DISTINCT pa.paper_id) AS paper_count
                FROM PaperAuthor pa
                JOIN Paper p ON pa.paper_id = p.id
                JOIN Author a ON pa.author_id = a.id
                JOIN University u ON a.author_university = u.id
                JOIN States s ON u.states_id = s.id
                JOIN Region r ON s.region_id = r.id
                WHERE r.description = "Nordeste"
                GROUP BY p.year, r.description
                ORDER BY p.year, r.description;
                """
    # Sudeste
    elif region == "4":
        query = """
                SELECT 
                p.year,
                COUNT(DISTINCT pa.paper_id) AS paper_count
                FROM PaperAuthor pa
                JOIN Paper p ON pa.paper_id = p.id
                JOIN Author a ON pa.author_id = a.id
                JOIN University u ON a.author_university = u.id
                JOIN States s ON u.states_id = s.id
                JOIN Region r ON s.region_id = r.id
                WHERE r.description = "Sudeste"
                GROUP BY p.year, r.description
                ORDER BY p.year, r.description;
                """
    # Sul
    elif region == "5":
        query = """
                SELECT 
                p.year,
                COUNT(DISTINCT pa.paper_id) AS paper_count
                FROM PaperAuthor pa
                JOIN Paper p ON pa.paper_id = p.id
                JOIN Author a ON pa.author_id = a.id
                JOIN University u ON a.author_university = u.id
                JOIN States s ON u.states_id = s.id
                JOIN Region r ON s.region_id = r.id
                WHERE r.description = "Sul"
                GROUP BY p.year, r.description
                ORDER BY p.year, r.description;
                """
    #Norte
    elif region == "6":
        query = """
                SELECT 
                p.year,
                COUNT(DISTINCT pa.paper_id) AS paper_count
                FROM PaperAuthor pa
                JOIN Paper p ON pa.paper_id = p.id
                JOIN Author a ON pa.author_id = a.id
                JOIN University u ON a.author_university = u.id
                JOIN States s ON u.states_id = s.id
                JOIN Region r ON s.region_id = r.id
                WHERE r.description = "Norte"
                GROUP BY p.year, r.description
                ORDER BY p.year, r.description;
                """
    cursor.execute(query)
    results = cursor.fetchall()
    # dataframe
    df = pd.DataFrame(results, columns=["Year", "Paper Count"])
    df["Year"] = df["Year"].astype(int)

    # Cria a lista completa de anos que você quer no gráfico
    anos_completos = list(range(1988, 2024))  # 1988 até 2023

    # Faz o DataFrame garantir todos os anos (preenchendo com 0 onde faltar)
    df = df.set_index("Year").reindex(anos_completos, fill_value=0).reset_index()

    # gráfico de barras agrupadas
    plt.figure(figsize=(16, 9))
    ax = sns.barplot(data=df, x="Year", y="Paper Count", width=0.6, color='skyblue')
    ax.plot(df["Paper Count"], marker='o', color='blue')

    if region == "1":
        plt.title("Number of Papers per Year in the Central-West Region")
    elif region == "2":
        plt.title("Number of Papers Written by Authors with International Affiliation")
    elif region == "3":
        plt.title("Number of Papers per Year in the Northeast Region")
    elif region == "4":
        plt.title("Number of Papers per Year in the Southeast Region")
    elif region == "5":
        plt.title("Number of Papers per Year in the South Region")
    elif region == "6":
        plt.title("Number of Papers per Year in the North Region")

    plt.ylabel("Number of Papers", fontweight='bold')
    plt.xlabel("Year", fontweight='bold')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
elif command == "5":
    query = """
            WITH UniversityRanking AS (
            SELECT 
                p.year,
                u.description AS university_name,
                COUNT(DISTINCT pa.paper_id) AS paper_count,
                ROW_NUMBER() OVER (PARTITION BY p.year ORDER BY COUNT(DISTINCT pa.paper_id) DESC) AS rank_position
            FROM PaperAuthor pa
            JOIN Paper p ON pa.paper_id = p.id
            JOIN Author a ON pa.author_id = a.id
            JOIN University u ON a.author_university = u.id
            GROUP BY p.year, u.description
            )
            SELECT 
                year,
                university_name,
                paper_count,
                rank_position
            FROM UniversityRanking
            WHERE rank_position <= 20
            ORDER BY year, rank_position;
        """
    cursor.execute(query)
    results = cursor.fetchall()
    df = pd.DataFrame(results, columns=["Year", "University", "Paper Count", "Rank"])
    print(df.sort_values(by=["Year", "Rank"]))
