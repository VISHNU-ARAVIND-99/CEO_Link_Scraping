from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import pandas as pd
import spacy


def ceo_scraping(company_name):
    name = "Nil"
    driver.get("https://www.google.com/")
    time.sleep(1)
    search1 = driver.find_element(By.XPATH, '//*[@id="APjFqb"]')
    # Virgin Media O2 + Executive Team + CEO + Chief Executive Officer + Name
    if "University" not in company_name and "College" not in company_name:
        search1.send_keys(f'{company_name} + Global CEO + Chief Executive Officer + Name')
    else:
        search1.send_keys(f'{company_name} + President + Name')
    time.sleep(1)
    search1.send_keys(Keys.RETURN)


    time.sleep(3)

    source = BeautifulSoup(driver.page_source, "html.parser")
    # try:
    #     inf = source.find_all('div', class_='Z0LcW AZCkJd d2J77b t2b5Cf')
    #     name = inf[0].text
    #
    # except:
    try:
        info = source.find_all('div', class_='Z0LcW t2b5Cf')
        name = info[0].text
    except:
        try:
            fo = source.find_all('div', class_='wDYxhc NFQFxe viOShc LKPcQc')
            name = fo[0].text
        except:
            info1 = source.find_all('div', class_='VwiC3b yXK7lf lVm3ye r025kc hJNv6b Hdw6tb')

            npl = spacy.load("en_core_web_sm")
            doc = npl(info1[0].text)
            person_names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
            try:
                name = person_names[0]

            except:
                try:
                    person_names = [ent.text for ent in doc.ents]
                    name = person_names[0]
                except:
                    pass
    print(name)
    return [company_name, name]


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
    list_of_list.append(ceo_scraping(company_name=k))
    out += 1
    print(out)

df = pd.DataFrame(list_of_list)
df.to_excel('ceo_name_scraping_out.xlsx', index=False)
