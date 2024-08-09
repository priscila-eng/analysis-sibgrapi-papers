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

def getTitle(paper_urls, dir_name, file_name):
    lines = [['id', 'title', 'year']]
    for id_paper, paper_url in enumerate(paper_urls):
        url = paper_url.replace("\n", "")
        req_paper_page = requests.get(url)
        paper_page = BeautifulSoup(req_paper_page.content, 'html.parser')
        tags_td = paper_page.find_all('td')
        print("paper", id_paper)
        # print("tags_td", tags_td)
        # print("content", paper_page)
        for i, element in enumerate(tags_td):
            # print("element ", element)
            if(element.text == "Title"):
                j = i + 1
                title = tags_td[j].text
                if not os.path.exists(dir_name):
                   makeDir(dir_name)
                if title:
                   lines.append([id_paper, title, counter])
    makeFile(file_name, lines)

while True:
    filename_paper = f"{counter}_papers.txt"
    dir_name = f"database/{counter}"
    filename_titles = f"{dir_name}/titles.csv"
    if not os.path.isfile(f'{dir_name}/{filename_titles}'):
        try:
            with open(f'papers_links/{filename_paper}', 'r') as f:
                file_content = f.readlines()
                getTitle(file_content, dir_name, filename_titles)
        except IOError:
            print("Quebrou no ano:", counter)
            break
    else:
        print(f"Ano {counter} já processado")
    counter = counter - 1