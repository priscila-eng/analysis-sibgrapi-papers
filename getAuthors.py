from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_headers import Headers
from selenium.webdriver import ChromeOptions
import os.path
import csv

counter = 2023

header = Headers(browser="chrome", os="win", headers=False)
customUserAgent = header.generate()['User-Agent']

options = ChromeOptions()
options.add_argument('--headless')
options.add_argument("--enable-javascript")
options.add_argument(f"user-agent={customUserAgent}")
driver = webdriver.Chrome(options=options)

def makeDir(dir_name):
    os.makedirs(dir_name)

def makeFile(file_name, content):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(content)

def getAuthorsUniversities(paper_urls, dir_name, filename_authors, filename_universities):
    lines_author = [['id', 'id_paper', 'name']]
    lines_university = [['id', 'id_author', 'university']]
    id_author = -1
    id_university = 0
    for id_paper, paper_url in enumerate(paper_urls):
        authors_url = paper_url.rstrip('\n') + "authors#authors"
        driver.get(authors_url)
        time.sleep(5)
        tags_div = driver.find_elements(By.CLASS_NAME, "authors-accordion-container")
        print(authors_url)
        for a_element in tags_div:
            name = a_element.find_element(By.TAG_NAME, "span")
            if not os.path.exists(dir_name):
                makeDir(dir_name)
            if name:
                id_author += 1
                lines_author.append([id_author, id_paper, name.text])
            if a_element.text and a_element != name:
                universities = a_element.text.split("\n")
                for i in range(len(universities)):
                    if i != 0:
                        lines_university.append([id_university, id_author, universities[i]])
                        id_university += 1
        time.sleep(5)
    makeFile(filename_authors, lines_author)
    makeFile(filename_universities, lines_university)

while True:
    filename_paper = f"{counter}_papers.txt"
    dir_name = f"database/{counter}"
    filename_author = f"{dir_name}/authors.csv"
    filename_university = f"{dir_name}/university.csv"
    if not os.path.isfile(filename_author) or not os.path.isfile(filename_university):
        try:
            with open(f'papers/{filename_paper}', 'r') as f:
                file_content = f.readlines()
                getAuthorsUniversities(file_content, dir_name, filename_author, filename_university)
        except IOError:
            print("Quebrou no ano:", counter)
            break
    else:
        print(f"Ano {counter} já processado")
    counter = counter - 1