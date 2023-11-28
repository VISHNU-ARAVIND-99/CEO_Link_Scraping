from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import pandas as pd


def craft_scraping(company_name):
    driver.get("https://www.google.com/")
    time.sleep(1)
    driver.maximize_window()
    time.sleep(1)
    search1 = driver.find_element(By.XPATH, '//*[@id="APjFqb"]')
    search1.send_keys(f'{company_name} + Executive Team + Leadership Team + CEO')
    time.sleep(1)
    search1.send_keys(Keys.RETURN)


    time.sleep(3)

    source = BeautifulSoup(driver.page_source, "html.parser")
    info1 = source.find_all('div', class_='kb0PBd cvP2Ce jGGQ5e')

    links = [company_name]
    count = 0
    for div in info1:
        # Find all <a> tags within the current <div> element
        a_tags = div.find_all('a')

        # Extract and append the href attribute from each <a> tag to the links list
        links.extend([a.get('href') for a in a_tags if a.get('href')])
        count += 1
        if count >= 5:
            break
    return links


options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

list_of_list = []
with open('company.txt', 'r') as file:
    links = file.readlines()
name_list = [x.strip() for x in links]

list_of_list = []
out = 0
for k in name_list:
    list_of_list.append(craft_scraping(company_name=k))
    out += 1
    print(out)

df = pd.DataFrame(list_of_list)
df.to_excel('ceo_Link_Scraping.xlsx', index=False)
