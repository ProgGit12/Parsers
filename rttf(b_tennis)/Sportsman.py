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

driver = webdriver.Chrome('/Users/macbookpro/Desktop/Project/Parser/Programm/chromdriver/chromedriver', options=options)
# driver.get("https://www.sports.ru/boxing/sportsman/")

link_mass = []
name_mass = []
citizenship_mass = []
birthday_mass = []
weight_mass = []
height_mass = []
discharge_mass = []
place_of_birth_mass = []
hand_mass = []
sex_mass = []
ccilca_sportsman_mass = []



# for i in range(1,301):
driver.get(f"https://rttf.ru/players")
time.sleep(30)

tr = driver.find_elements(by=By.TAG_NAME, value='tr')


for a_link in tr:
    try:
        a = a_link.find_elements(by=By.TAG_NAME, value='a')
        link_mass.append(a[0].get_attribute('href'))
    except IndexError:
        pass

for link in link_mass:
    # print(link)
    driver.get(link)

    section = driver.find_element(by=By.TAG_NAME, value='section')
    span = section.find_elements(by=By.TAG_NAME, value='p')


    birthday = 0
    citizenship = 0
    hand = 0
    discharge = 0
    name = section.find_element(by=By.TAG_NAME, value='h1').text
    for glav in span:
        if re.sub(r"[:]\s.{1,50}", "", glav.text, 1) == "город" or re.sub(r"[:]\s.{1,50}", "", glav.text, 1) == "Страна":
            citizenship = re.sub(r".{1,50}[:]\s", "", glav.text, 1)
        elif re.sub(r"[:]\s.{1,50}", "", glav.text, 1) == "Дата рождения":
            birthday = re.sub(r".{1,50}[:]\s", "", glav.text, 1)
            birthday = re.sub(r"[(].{1,10}[)]", "", birthday, 1)
        elif re.sub(r"[:]\s.{1,50}", "", glav.text, 1) == "Игровая рука":
            hand = re.sub(r".{1,50}[:]\s", "", glav.text, 1)
        elif re.sub(r"[:]\s.{1,50}", "", glav.text, 1) == "Разряд":
            discharge = re.sub(r".{1,50}[:]\s", "", glav.text, 1)

    name_mass.append(name)
    birthday_mass.append(birthday)

    citizenship_mass.append(citizenship)
    hand_mass.append(hand)
    discharge_mass.append(discharge)

    ccilca_sportsman_mass.append(link)

    time.sleep(1)




dfPlayer_Inf = pd.DataFrame({
        'Name': pd.Series(name_mass, dtype='object'),
        'Birthday': pd.Series(birthday_mass),

        'Citizenship': pd.Series(citizenship_mass),
        'Hand': pd.Series(hand_mass),
        'discharge': pd.Series(discharge_mass),

        'Link': pd.Series(ccilca_sportsman_mass),
    })

dfPlayer_Inf.to_csv(r'/Users/macbookpro/Desktop/Project/Parser_data/table(Table_Tennis_rttf2).csv', index=False, sep=';', encoding='utf-8-sig')

driver.close()
driver.quit()
