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
    lines = [['id', 'title', 'year']]
    for id_paper, paper_url in enumerate(paper_urls):
        driver.get(paper_url)
        time.sleep(5)
        print("paper", id_paper)
        tags_h1 = driver.find_elements(By.TAG_NAME, "h1")
        for a_element in tags_h1:
            class_name = a_element.get_attribute("class")
            if "document-title" in class_name:
                if not os.path.exists(dir_name):
                    makeDir(dir_name)
                if a_element.text:
                    lines.append([id_paper, a_element.text, counter])
        time.sleep(5)
    makeFile(file_name, lines)

while True:
    filename_paper = f"{counter}_papers.txt"
    dir_name = f"database/{counter}"
    filename_titles = f"{dir_name}/titles.csv"
    if not os.path.isfile(f'{dir_name}/{filename_titles}'):
        try:
            with open(f'papers/{filename_paper}', 'r') as f:
                file_content = f.readlines()
                getKeywords(file_content, dir_name, filename_titles)
        except IOError:
            print("Quebrou no ano:", counter)
            break
    else:
        print(f"Ano {counter} já processado")
    counter = counter - 1