# Análise de artigos da SIBGRAPI

Projeto desenvolvido como parte de um Trabalho de Conclusão de Curso sobre a produção científica da **SIBGRAPI — Conference on Graphics, Patterns and Images**.

O projeto realiza a coleta, o processamento, o armazenamento e a análise de informações dos artigos publicados na conferência entre **1988 e 2023**. A partir desses dados, busca-se analisar o perfil dos autores, sua distribuição geográfica, a participação por gênero e a evolução dos temas pesquisados ao longo dos anos.

## Objetivos

O projeto tem como principais objetivos:

* coletar informações dos artigos publicados na SIBGRAPI;
* extrair títulos, autores, palavras-chave e instituições;
* organizar os dados em um banco de dados relacional;
* identificar a distribuição geográfica dos autores;
* analisar a participação de autores por gênero;
* observar a evolução dos temas de pesquisa ao longo dos anos;
* gerar gráficos, mapas e nuvens de palavras para representar os resultados.

## Período analisado

A pesquisa considera os artigos publicados entre **1988 e 2023**.

Os dados foram obtidos de diferentes fontes, de acordo com o período de publicação:

* **1988 a 1996:** páginas e documentos disponibilizados no acervo da SIBGRAPI;
* **1997 a 2023:** metadados e publicações disponíveis no IEEE Xplore.

## Tecnologias utilizadas

O projeto foi desenvolvido principalmente em **Python** e utiliza um banco de dados **MySQL**.

Entre as principais tecnologias e bibliotecas utilizadas estão:

* Python;
* MySQL;
* Beautiful Soup;
* Selenium;
* Requests;
* Pandas;
* NumPy;
* Matplotlib;
* Plotly;
* WordCloud;
* MySQL Connector;
* python-dotenv;
* Unidecode;
* Argos Translate;
* Levenshtein.

## Estrutura do projeto

```text
analysis-sibgrapi-papers/
├── database/
├── getData/
├── insertToDB/
├── papers/
├── papers_links/
├── statistcs/
├── .gitignore
├── LICENSE
└── README.md
```

### `database/`

Contém os dados coletados e organizados por ano de publicação, abrangendo o período de 1988 a 2023.

### `getData/`

Contém os scripts responsáveis pela coleta e extração dos dados.

Entre os arquivos disponíveis estão:

```text
getAuthors.py
getAuthorsBS.py
getAuthorsPapers.py
getDataPapers.py
getKeywords.py
getKeywordsBS.py
getTitle.py
getTitleBS.py
scrapper_ieee.py
scrapper_metadata.py
```

Esses scripts realizam tarefas como:

* coleta dos artigos;
* extração dos autores;
* extração dos títulos;
* extração das palavras-chave;
* obtenção de metadados;
* coleta de informações no IEEE Xplore;
* processamento dos dados com Beautiful Soup.

Os arquivos com o sufixo `BS` utilizam rotinas baseadas em **Beautiful Soup**.

### `insertToDB/`

Contém os scripts utilizados para tratar os dados e inserí-los no banco de dados MySQL.

Principais arquivos:

```text
classifyUniversity.py
insertAuthor.py
insertAuthorUniversity.py
insertKeyword.py
insertPaperKeyword.py
insertPaperToAuthor.py
insertTitle.py
insertUniversity.py
```

Essa pasta também contém arquivos CSV auxiliares, incluindo:

```text
all_keywords.csv
authors_ia.csv
estados.csv
firstnames.csv
municipios-uf.csv
names.csv
paises.csv
universities.csv
universitiesStates.csv
universities_ia.csv
```

Esses arquivos são utilizados no processo de:

* classificação dos autores;
* identificação das universidades;
* associação entre universidades e estados;
* padronização de palavras-chave;
* classificação geográfica;
* apoio à identificação de gênero;
* armazenamento de resultados intermediários.

### `papers/`

Armazena os artigos ou arquivos relacionados às publicações coletadas.

Por conter documentos provenientes de fontes externas, é necessário observar as condições de acesso e uso definidas pelos respectivos provedores.

### `papers_links/`

Armazena links utilizadas para localizar os artigos publicados na conferência.

### `statistcs/`

Contém os scripts responsáveis pelas consultas, análises estatísticas e visualizações dos dados.

Principais arquivos:

```text
author.py
author_pie.py
generate_wordcloud.py
keywords.py
maps.py
paperAuthor.py
paperAuthor_feira.py
papers.py
university.py
```

Entre as análises produzidas estão:

* quantidade de autores por gênero;
* participação feminina ao longo dos anos;
* quantidade de artigos publicados;
* distribuição por universidade;
* distribuição por estado e região;
* mapas geográficos;
* palavras-chave mais frequentes;
* nuvens de palavras;
* evolução dos principais temas de pesquisa.

## Modelo de dados

O banco de dados foi estruturado para representar artigos, autores, palavras-chave, universidades e localizações geográficas.

As principais entidades são:

* `Author`;
* `Paper`;
* `PaperAuthor`;
* `Keyword`;
* `PaperKeyword`;
* `University`;
* `States`;
* `Region`.

Uma estrutura simplificada dos relacionamentos é apresentada abaixo:

```text
Author N:N Paper
Paper N:N Keyword
Author N:1 University
University N:1 States
States N:1 Region
```

As tabelas associativas `PaperAuthor` e `PaperKeyword` representam, respectivamente, os relacionamentos muitos-para-muitos entre autores e artigos e entre artigos e palavras-chave.

## Metodologia

O fluxo geral do projeto é dividido nas seguintes etapas:

```text
Coleta dos artigos
        ↓
Extração dos metadados
        ↓
Limpeza e padronização
        ↓
Inserção no banco de dados
        ↓
Consultas e análises
        ↓
Geração de gráficos, mapas e nuvens de palavras
```

### 1. Coleta

Os scripts da pasta `getData` acessam as fontes disponíveis e coletam informações relacionadas aos artigos.

### 2. Extração

São extraídas informações como:

* título do artigo;
* ano de publicação;
* nomes dos autores;
* palavras-chave;
* instituições;
* referências;
* links e metadados.

### 3. Limpeza e padronização

Os dados coletados passam por procedimentos de:

* remoção de espaços e quebras de linha;
* normalização de caracteres;
* padronização de letras maiúsculas e minúsculas;
* tradução de palavras-chave;
* comparação de nomes semelhantes;
* tratamento de autores com nomes abreviados;
* remoção ou controle de registros duplicados;
* associação de universidades aos estados e regiões.

### 4. Armazenamento

Após o tratamento, os dados são inseridos em um banco de dados MySQL.

### 5. Análise

As consultas ao banco permitem gerar informações sobre:

* diversidade dos autores;
* participação por gênero;
* evolução das publicações;
* localização das instituições;
* frequência de palavras-chave;
* transformação dos temas estudados ao longo do tempo.

## Pré-requisitos

Para executar o projeto, recomenda-se utilizar:

* Python 3.10 ou superior;
* MySQL Server;
* MySQL Workbench, opcionalmente;
* Google Chrome ou Chromium;
* ChromeDriver compatível com a versão do navegador.

## Instalação

Clone o repositório:

```bash
git clone https://github.com/priscila-eng/analysis-sibgrapi-papers.git
```

Entre na pasta do projeto:

```bash
cd analysis-sibgrapi-papers
```

Instale as principais dependências:

```bash
pip install requests beautifulsoup4 selenium pandas numpy matplotlib plotly
pip install mysql-connector-python python-dotenv unidecode
pip install python-Levenshtein wordcloud argostranslate
```

Como o projeto ainda não possui um arquivo `requirements.txt` consolidado, pode ser necessário instalar dependências adicionais de acordo com o script executado.

## Configuração do banco de dados

Crie um banco de dados MySQL para armazenar as informações do projeto.

Exemplo:

```sql
CREATE DATABASE sibgrapi;
```

Na raiz do projeto, crie um arquivo `.env` com as credenciais do banco:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=sibgrapi
```

O arquivo `.env` está incluído no `.gitignore` e não deve ser enviado ao repositório.

## Execução

A execução depende da etapa que se deseja reproduzir.

### Coleta dos dados

Os scripts de coleta estão na pasta `getData`.

Exemplo:

```bash
python getData/scrapper_metadata.py
```

Para coletar informações do IEEE:

```bash
python getData/scrapper_ieee.py
```

Para extrair autores:

```bash
python getData/getAuthors.py
```

Para extrair palavras-chave:

```bash
python getData/getKeywords.py
```

Antes de executar os coletores, verifique:

* os caminhos utilizados nos scripts;
* a disponibilidade das páginas consultadas;
* a versão do ChromeDriver;
* as permissões de acesso ao IEEE Xplore;
* as políticas de uso e de coleta das fontes consultadas.

### Inserção no banco

Após a coleta e o tratamento dos dados, execute os scripts da pasta `insertToDB`.

Uma possível ordem de execução é:

```bash
python insertToDB/insertTitle.py
python insertToDB/insertAuthor.py
python insertToDB/insertUniversity.py
python insertToDB/insertAuthorUniversity.py
python insertToDB/insertPaperToAuthor.py
python insertToDB/insertKeyword.py
python insertToDB/insertPaperKeyword.py
```

A ordem pode precisar ser adaptada às chaves estrangeiras e às dependências existentes no banco de dados.

### Geração das análises

Os scripts de análise estão na pasta `statistcs`.

Exemplos:

```bash
python statistcs/author.py
python statistcs/author_pie.py
python statistcs/papers.py
python statistcs/university.py
python statistcs/keywords.py
python statistcs/maps.py
python statistcs/generate_wordcloud.py
```

Os arquivos podem gerar gráficos diretamente na tela ou salvar imagens, dependendo da configuração presente no código.

## Principais análises

O projeto permite investigar diferentes aspectos da produção científica da SIBGRAPI.

### Participação por gênero

Análise da quantidade e da proporção de autores classificados como:

* mulheres;
* homens;
* desconhecidos ou não identificados.

A classificação representa uma estimativa construída a partir das fontes e métodos adotados na pesquisa. Ela não deve ser interpretada como autodeclaração de identidade de gênero.

### Distribuição geográfica

Análise da participação de autores e instituições por:

* universidade;
* estado;
* região brasileira;
* país, quando aplicável.

### Evolução temporal

Análise das mudanças ocorridas entre 1988 e 2023, incluindo:

* quantidade de artigos;
* quantidade de autores;
* participação por gênero;
* distribuição geográfica;
* temas mais frequentes.

### Evolução temática

As palavras-chave são utilizadas para identificar os temas predominantes em diferentes períodos da conferência.

Entre as visualizações utilizadas estão:

* tabelas de frequência;
* gráficos por ano;
* rankings de palavras-chave;
* nuvens de palavras.

## Aspectos éticos

Os dados utilizados no projeto são provenientes de publicações científicas e de informações profissionais publicamente disponíveis.

A análise de gênero possui finalidade exclusivamente acadêmica e estatística. A classificação não representa autodeclaração dos autores e pode conter imprecisões.

Os resultados devem ser apresentados de forma agregada, evitando conclusões individuais ou inferências indevidas sobre pessoas específicas.

## Referências e fontes de dados

* SIBGRAPI — Conference on Graphics, Patterns and Images;
* Sociedade Brasileira de Computação;
* IEEE Xplore;
* páginas institucionais e bases públicas utilizadas na verificação e complementação dos dados.

---

Este repositório possui finalidade acadêmica e foi desenvolvido como parte de uma pesquisa sobre diversidade, distribuição geográfica e evolução temática da produção científica da SIBGRAPI.
