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

def getKeywords(paper_urls, dir_name, file_name):
    lines = [['id', 'id_paper', 'keyword']]
    id_keyword = 0
    for id_paper, paper_url in enumerate(paper_urls):
        keywords_url = paper_url.rstrip('\n') + "keywords#keywords"
        driver.get(keywords_url)
        time.sleep(5)
        tags_a = driver.find_elements(By.TAG_NAME, "a")
        print(keywords_url)
        for a_element in tags_a:
            if a_element.get_attribute("href") and "newsearch=true" in a_element.get_attribute("href"):
                if not os.path.exists(dir_name):
                    makeDir(dir_name)
                if a_element.text:
                    lines.append([id_keyword, id_paper, a_element.text])
                    id_keyword += 1
        time.sleep(5)
    
    makeFile(file_name, lines)

while True:
    filename_paper = f"{counter}_papers.txt"
    dir_name = f"database/{counter}"
    filename_keywords = f"{dir_name}/keywords.csv"
    if not os.path.isfile(f'{dir_name}/{filename_keywords}'):
        try:
            with open(f'papers/{filename_paper}', 'r') as f:
                file_content = f.readlines()
                getKeywords(file_content, dir_name, filename_keywords)
        except IOError:
            print("Quebrou no ano:", counter)
            break
    else:
        print(f"Ano {counter} já processado")
    counter = counter - 1