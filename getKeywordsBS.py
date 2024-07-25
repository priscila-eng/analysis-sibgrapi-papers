import requests
from bs4 import BeautifulSoup, Comment
from pathlib import Path
import os
import os.path
from os import path
import csv

counter = 1996

def makeDir(dir_name):
    os.makedirs(dir_name)

def makeFile(file_name, content):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(content)

def getAuthors(paper_urls, dir_name, file_name):
    lines = [['id', 'id_paper', 'keyword']]
    id_keyword = 0
    for id_paper, paper_url in enumerate(paper_urls):
        url = paper_url.replace("\n", "")
        req_paper_page = requests.get(url)
        paper_page = BeautifulSoup(req_paper_page.content, 'html.parser')
        tags_td = paper_page.find_all('td')
        for i, element in enumerate(tags_td):
            if(element.text == "Keywords"):
                j = i + 1
                tt_content = tags_td[j].find('tt').decode_contents()
                keywords = tt_content.replace('<br/>', '\n')
                keywords = keywords.split('\n')
                print("KEYWORDS\n", keywords)
                for key in keywords:
                    if not os.path.exists(dir_name):
                        makeDir(dir_name)
                    lines.append([id_keyword, id_paper, key.strip()])
                    id_keyword += 1
                            
                
    makeFile(file_name, lines)

while True:
    filename_paper = f"{counter}_papers.txt"
    dir_name = f"database/{counter}"
    filename_authors = f"{dir_name}/keywords.csv"
    if not os.path.isfile(f'{dir_name}/{filename_authors}'):
        try:
            with open(f'papers_links/{filename_paper}', 'r') as f:
                file_content = f.readlines()
                getAuthors(file_content, dir_name, filename_authors)
        except IOError:
            print("Quebrou no ano:", counter)
            break
    else:
        print(f"Ano {counter} já processado")
    counter = counter - 1