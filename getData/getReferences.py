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

def getReferences(paper_urls, dir_name, file_name):
    lines = [['id', 'id_paper', 'reference']]
    id_reference = 0
    for id_paper, paper_url in enumerate(paper_urls):
        references_url = paper_url.rstrip('\n') + "references#references"
        driver.get(references_url)
        time.sleep(5)
        tags_div = driver.find_elements(By.TAG_NAME, "div")
        for a_element in tags_div:
            class_ref = a_element.get_attribute("class")
            if class_ref and "reference-container" in class_ref:
                if not os.path.exists(dir_name):
                    makeDir(dir_name)
                if a_element.text:
                    reference = a_element.text.split("\n")
                    lines.append([id_reference, id_paper, reference[1]])
                    id_reference += 1
        time.sleep(5)
    
    makeFile(file_name, lines)

while True:
    filename_paper = f"{counter}_papers.txt"
    dir_name = f"database/{counter}"
    filename_references = f"{dir_name}/references.csv"
    if not os.path.isfile(f'{dir_name}/{filename_references}'):
        try:
            with open(f'papers/{filename_paper}', 'r') as f:
                file_content = f.readlines()
                getReferences(file_content, dir_name, filename_references)
        except IOError:
            print("Quebrou no ano:", counter)
            break
    else:
        print(f"Ano {counter} já processado")
    print(f"{counter} terminou de processar")
    counter = counter - 1