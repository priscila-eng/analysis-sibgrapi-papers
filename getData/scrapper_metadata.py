import requests
from bs4 import BeautifulSoup, Comment
from pathlib import Path
import os
import os.path
from os import path

# mudar user agent para mozilla

url_main_page = 'http://sibgrapi.sid.inpe.br/col/sid.inpe.br/banon/2001/03.30.15.38.24/doc/mirror.cgi/About?languagebutton=en&languagerep1=sid.inpe.br/banon/2001/05.04.15.05&languagerep2=dpi.inpe.br/banon/1999/05.03.22.11&firstlanguagerep=sid.inpe.br/banon/2001/05.04.15.05&submissionformrep=dpi.inpe.br/banon-pc2@80/2006/08.30.19.42&returnbutton=yes'

req_main_page = requests.get(url_main_page)

counter = 1996

main_page = BeautifulSoup(req_main_page.content, 'html.parser')
tags_a = main_page.find_all('a')

links_conf_year = []
links_conf_year_body = []
links_page_paper_frame = []
links_page_paper_goto = []
links_page_paper = []
links_page_paper_header = []
links_page_paper_frame_header = []
links_page_paper_metadata = []


while True:
    for a_element in tags_a:
        if a_element.get("href") and str(counter) in a_element.text:
            url = a_element.get("href")
            links_conf_year.append(url)
            break

    if counter == 1988:
        break

    counter = counter - 1

for url_conf_year in links_conf_year:
    req_conf_page = requests.get(url_conf_year)
    conf_page = BeautifulSoup(req_conf_page.content, 'html.parser')
    tags_frame = conf_page.find_all('frame')
    for i in tags_frame:
        if not '/Header?' in i['src']:
            links_conf_year_body.append(i['src'])

for url in links_conf_year_body:
    req_conf_page_body = requests.get(url)
    conf_page = BeautifulSoup(req_conf_page_body.content, 'html.parser')
    tags_a = conf_page.find_all('a')
    for i in tags_a:
        link = 'http://sibgrapi.sid.inpe.br/rep/' + i['href'][5:] + '&ibiurl.clientinformation.citingitem=sid.inpe.br/sibgrapi/2013/04.05.14.47&linktype=relative'
        links_page_paper_frame.append(link)

counter = 1996
# Aqui tem o link da página de cada ano, com a lista de papers
for link in links_page_paper_frame:
    req_page_paper_frame = requests.get(link)
    page_paper_frame = BeautifulSoup(req_page_paper_frame.content, 'html.parser')
    tags_frame = page_paper_frame.find_all('frame')
    for i in tags_frame:
        if not '/Header?' in i['src']:
            links_page_paper_goto.append(i['src'])

# Aqui tem um dicionario com os links de todos os papers de cada ano            
for link in links_page_paper_goto:
    links = []
    req_page_paper_goto = requests.get(link)
    page_paper = BeautifulSoup(req_page_paper_goto.content, 'html.parser')
    tags_a_goto = page_paper.find_all('a')

    for i in tags_a_goto:
        if i.has_attr('href') and i['href'].startswith('goto/') and i['href'].endswith('flag=0'):
            url = 'http://sibgrapi.sid.inpe.br/rep/' + i['href'][5:]
            links.append(url)
    links_page_paper.append({counter: links})
    counter = counter - 1

header = {
    'User-Agent': 'Mozilla/5.0'
}
print("COMECOU")
counter = 1996
for dicts in links_page_paper:
    links = []
    for link in dicts[counter]:
        req_page_paper = requests.get(link, headers=header)
        page_paper = BeautifulSoup(req_page_paper.content, 'html.parser')
        tag_script = page_paper.find('script')
        text = tag_script.get_text()
        inicio = text.find("http://")
        fim = text.find(".html")
        if inicio == -1 or fim == -1:
            links.append(link)
        else:
            links.append(text[inicio:fim + 5])
    links_page_paper_header.append({counter: links})
    counter = counter - 1

# javascript -> frame header -> metadata

print("COMECOU")
counter = 1996
for dicts in links_page_paper_header:
    links = []
    for link in dicts[counter]:
        req_page_paper = requests.get(link, headers=header)
        page_paper = BeautifulSoup(req_page_paper.content, 'html.parser')
        tags_frame = page_paper.find_all('frame')
        for tag in tags_frame:
            if tag['name'] == "header":
                url = tag['src']
                url = url.replace(':80', '')
                # print(url)
                url = url.replace('©right', '&copyright')
                url = url.replace('¶meterlist', '&parameterlist')
                url = url.replace('¤trep', '&currentrep')
                links.append(url)
    links_page_paper_frame_header.append({counter: links})
    counter = counter - 1

counter = 1996
for dicts in links_page_paper_frame_header:
    links = []
    for link in dicts[counter]:
        temMetadata = False
        req_page_paper = requests.get(link, headers=header)
        page_paper = BeautifulSoup(req_page_paper.content, 'html.parser')
        tags_a = page_paper.find_all('a')
        for tag in tags_a:
            if tag.get_text() == "Metadata":
                temMetadata = True
                links.append(tag['href'])
        if not temMetadata:
            print("Não achou metadata para o link", link)

    filename = f"{counter}_papers.txt"
    
    if os.path.exists(f'papers/{filename}'):
        print("Ano já processado: ", counter)
        break
    
    for link in links:
        with open(f'papers/{filename}', 'a') as file:
            file.write(link + "\n")
    # links_page_paper_metadata.append({counter: links})
    counter = counter - 1

