from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_headers import Headers
from selenium.webdriver import ChromeOptions
import os.path


header = Headers(browser="chrome", os="win", headers=False)
customUserAgent = header.generate()['User-Agent']

options = ChromeOptions()
options.add_argument('--headless')
options.add_argument("--enable-javascript")
options.add_argument(f"user-agent={customUserAgent}")
driver = webdriver.Chrome(options=options)


url_main_page = 'https://ieeexplore.ieee.org/xpl/conhome/1000131/all-proceedings'

driver.get(url_main_page)

time.sleep(5)
tags_a = driver.find_elements(By.TAG_NAME, "a")
links_conf_year = []

for a_element in tags_a:
    if a_element.get_attribute("href"):
        url = a_element.get_attribute("href")
        if url and url.endswith("/proceeding") and url not in links_conf_year:
            links_conf_year.append(url)

counter = 2023
    

for url_conf_year in links_conf_year:
    page = 1
    papers_list = []
    time.sleep(5)
    driver.get(url_conf_year)
    time.sleep(2)

    while True:
        filename = f"{counter}_papers.txt"
        
        if os.path.exists(f'papers/{filename}') and page == 1:
            print("Ano já processado: ", counter)
            break

        buttons_pagination = driver.find_elements(By.TAG_NAME, "button")
        time.sleep(2)

        for button in buttons_pagination:
            if button.text == str(page):
                driver.execute_script("arguments[0].scrollIntoView(true);", button)
                time.sleep(1)
                button.click()
                break
        
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, 'a')))
        papers_links = driver.find_elements(By.TAG_NAME, "a")
        for paper in papers_links:
            paper_url = paper.get_attribute("href")
            if paper_url and paper_url.endswith("/") and "document" in paper_url:
                if paper_url not in papers_list:
                    papers_list.append(paper_url)
                    with open(f"papers/{filename}", 'a') as file:
                        file.write(paper_url + "\n")
        
        time.sleep(5)
        page = page + 1
        path = f'//button[text()="{page}"]'
        next_page_button = driver.find_elements(By.XPATH, path)
        if not next_page_button:
            break
    counter = counter - 1

    
            

