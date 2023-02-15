from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.chrome.options import Options
import time
import re
import pandas as pd
import numpy as np

# Здесь создаю браузер и перехожу на сайт
options = Options()
# options.add_experimental_option(
#     'prefs',
#     {
#         'profile.managed_default_content_settings.javascript': 2,
#         'profile.managed_default_content_settings.images': 2,
#         'profile.managed_default_content_settings.mixed_script': 2,
#     }
# )

driver = webdriver.Chrome('/Users/macbookpro/Desktop/Project/Parser_data/chromedriver/chromedriver', options=options)

link_mass = []
name_mass = []
address_mass = []
date_mass = []
weight_mass = []
height_mass = []
discharge_mass = []
place_of_birth_mass = []
club_mass = []

ccilca_sportsman_mass = []



# for i in range(1,301):
# driver.get(f"https://rttf.ru/players")
driver.get(f"https://rttf.ru/tournaments/?date_from=&date_to=14.02.2023&rats=all&rat_from=0&rat_to=1600&title=&search=")
time.sleep(2)

a = driver.find_elements(by=By.CLASS_NAME, value='ladder')


for s in a:
    link_mass.append(s.get_attribute('href'))


for link in link_mass:
    driver.get(link)

    section = driver.find_element(by=By.CLASS_NAME, value='tour-desc')
    p = section.find_elements(by=By.TAG_NAME, value='p')

    date = 0
    address = 0
    club = 0
    status = 0
    name = driver.find_element(by=By.TAG_NAME, value='h1').text


    for glav in p:
        if re.sub(r"[:]\s.{1,300}", "", glav.text, 1) == "Дата":
            date = re.sub(r".{1,300}[:]\s", "", glav.text, 1)
        elif re.sub(r"[:]\s.{1,300}", "", glav.text, 1) == "Клуб":
            club = re.sub(r".{1,300}[:]\s", "", glav.text, 1)
        elif re.sub(r"[:]\s.{1,300}", "", glav.text, 1) == "Адрес":
            address = re.sub(r".{1,300}[:]\s", "", glav.text, 1)


    name_mass.append(name)
    date_mass.append(date)

    address_mass.append(address)
    club_mass.append(club)

    ccilca_sportsman_mass.append(link)

    time.sleep(1)


    print()

dfPlayer_Inf = pd.DataFrame({
        'Name': pd.Series(name_mass, dtype='object'),
        'Date': pd.Series(date_mass),

        'Address': pd.Series(address_mass),
        'Club': pd.Series(club_mass),

        'Link': pd.Series(ccilca_sportsman_mass),
    })

dfPlayer_Inf.to_csv(r'/Users/macbookpro/Desktop/Project/Parser_data/Table_excel/rttf(tennis)/Places_Match(table-tennis).csv', index=False, sep=';', encoding='utf-8-sig')

driver.close()
driver.quit()
