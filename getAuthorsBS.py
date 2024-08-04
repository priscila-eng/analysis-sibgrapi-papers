import requests
from bs4 import BeautifulSoup, Comment
from pathlib import Path
import os
import os.path
from os import path
import csv

counter = 1995

def makeDir(dir_name):
    os.makedirs(dir_name)

def makeFile(file_name, content):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(content)

def getAuthors(paper_urls, dir_name, filename_authors, filename_universities):
    lines_authors = [['id', 'id_paper', 'name']]
    lines_university = [['id', 'id_author', 'university']]
    id_author  = 0
    id_university = 0
    for id_paper, paper_url in enumerate(paper_urls):
        id_authors_universities = []
        url = paper_url.replace("\n", "")
        req_paper_page = requests.get(url)
        paper_page = BeautifulSoup(req_paper_page.content, 'html.parser')
        tags_td = paper_page.find_all('td')
        for i, element in enumerate(tags_td):
            j = i + 1
            if(element.text == "Author"):
                tt_content = tags_td[j].find('tt').decode_contents()
                print(id_paper)
                author = tt_content.replace('<br/>', '\n')
                author = author.split('\n')
                name_reorder = ""
                for value in author:
                    partes = value.split(', ')
                    name = partes[1]
                    if partes[0][0].isdigit():
                        lastname = " " + partes[0][2:]
                    else:
                        lastname = " " + partes[0]
                    name_reorder = name + lastname
                    if not os.path.exists(dir_name):
                        makeDir(dir_name)
                    if name:
                        lines_authors.append([id_author, id_paper, name_reorder])
                        id_authors_universities.append(id_author)
                        id_author += 1
                if("http://sibgrapi.sid.inpe.br/sid.inpe.br/sibgrapi/2013/02.18.16.52.29?ibiurl.backgroundlanguage=en" in paper_url):
                    print(name_reorder)
                # if(author[0].isdigit()):
                #     name = ""
                #     lastname = ""
                #     for value in author:
                #         if not value.isdigit():
                #             if value.endswith(","):
                #                 lastname = value
                #             else:
                #                 name += value + " "
                #         else:
                #             name = name + lastname
                            
                #             name = ""
                #             lastname = ""
                #         if value == author[len(author)-1]:
                #             name = name + lastname
                #             if not os.path.exists(dir_name):
                #                 makeDir(dir_name)
                #             if name:
                #                 lines_authors.append([id_author, id_paper, name[:-1]])
                #                 id_authors_universities.append(id_author)
                #                 id_author += 1
                #             name = ""
                #             lastname = ""
                # else:
                #     author = tt_content.split(',')
                #     primeiro_elemento = author.pop(0)
                #     author.append(primeiro_elemento)
                #     name = ""
                #     for value in author:
                #         name += value
                #     lines_authors.append([id_author, id_paper, name[1:]])
                #     id_authors_universities.append(id_author)
                #     id_author += 1
            if(element.text == "Affiliation"):
                tt_content = tags_td[j].find('tt').decode_contents()
                universities = tt_content.replace('<br/>', '\n')
                universities = universities.split('\n')
                for university in universities:
                    if(university[0].isdigit()):
                        pos = int(university[0]) - 1
                        lines_university.append([id_university, id_authors_universities[pos], university[2:]])
                        id_university += 1
                    else:
                        lines_university.append([id_university, id_authors_universities[0], university])
                        id_university += 1
                if not os.path.exists(dir_name):
                   makeDir(dir_name)
            if(element.text == "Empty Fields"):
                fields = tags_td[j].text
                if "affiliation" in fields:
                    for id in id_authors_universities:
                        lines_university.append([id_university, id, "NULL"])
                        id_university += 1
                
    makeFile(filename_authors, lines_authors)
    makeFile(filename_universities, lines_university)

while True:
    filename_paper = f"{counter}_papers.txt"
    dir_name = f"database/{counter}"
    filename_authors = f"{dir_name}/authors.csv"
    filename_university = f"{dir_name}/university.csv"
    if not os.path.isfile(f'{dir_name}/{filename_authors}') or not os.path.isfile(filename_university):
        print(f"processando o ano {counter}")
        try:
            with open(f'papers_links/{filename_paper}', 'r') as f:
                file_content = f.readlines()
                getAuthors(file_content, dir_name, filename_authors, filename_university)
        except IOError:
            print("Quebrou no ano:", counter)
            break
    else:
        print(f"Ano {counter} já processado")
    counter = counter - 1