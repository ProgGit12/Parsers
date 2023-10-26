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

driver = webdriver.Chrome('/Users/macbookpro/Desktop/Project/Parser/Programm/driver/chromedriver', options=options)
# driver.get("https://www.sports.ru/boxing/sportsman/")
name_mass = []
rating_mass = []
birthday_mass = []
citizenship_mass = []
hand_mass = []
discharge_mass = []
base_mass = []
trim_right_mass = []
trim_left_mass = []
visiting_mass = []

link_mass = []

weight_mass = []
height_mass = []
place_of_birth_mass = []
sex_mass = []
ccilca_sportsman_mass = []


dfPlayer_Inf = pd.DataFrame({
        'Name': pd.Series(name_mass, dtype='object'),
        'Rating': pd.Series(rating_mass, dtype='object'),
        'Birthday': pd.Series(birthday_mass, dtype='object'),
        'Citizenship': pd.Series(citizenship_mass, dtype='object'),
        'Hand': pd.Series(hand_mass, dtype='object'),
        'discharge': pd.Series(discharge_mass, dtype='object'),
        'Base': pd.Series(base_mass, dtype='object'),
        'Trim right': pd.Series(trim_right_mass, dtype='object'),
        'Trim left': pd.Series(trim_left_mass, dtype='object'),
        'Visiting': pd.Series(visiting_mass, dtype='object'),

        'Link': pd.Series(ccilca_sportsman_mass, dtype='object'),
    })



# for i in range(1,301):
driver.get(f"https://rttf.ru/players/")
time.sleep(2)

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
    time.sleep(1)

    section = driver.find_element(by=By.CLASS_NAME, value='player-info')
    span = section.find_elements(by=By.TAG_NAME, value='p')

    name = section.find_element(by=By.TAG_NAME, value='h1').text
    rating = section.find_element(by=By.TAG_NAME, value='dfn').text

    birthday = 0
    citizenship = 0
    hand = 0
    discharge = 0
    base = 0
    trim_right = 0
    trim_left = 0
    visiting = 0

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
        elif re.sub(r"[:]\s.{1,50}", "", glav.text, 1) == "Основание":
            base = re.sub(r".{1,200}:\W.\s", "", glav.text, 1)
        elif re.sub(r"[:]\s.{1,50}", "", glav.text, 1) == "Накладка справа":
            trim_right = re.sub(r".{1,200}:\W.\s", "", glav.text, 1)
        elif re.sub(r"[:]\s.{1,50}", "", glav.text, 1) == "Накладка слева":
            trim_left = re.sub(r".{1,200}:\W.\s", "", glav.text, 1)
        elif re.sub(r"[:]\s.{1,50}", "", glav.text, 1) == "На сайте с":
            visiting = re.sub(r".{1,200}:\W.\s", "", glav.text, 1)

    dfPlayer_Inf.loc[len(dfPlayer_Inf.index)] = [name, rating, birthday, citizenship,
                                                 hand, discharge, base, trim_right,
                                                 trim_left, visiting]
    time.sleep(1)

dfPlayer_Inf.to_csv(r'/Users/macbookpro/Desktop/Project/Parser_data/Table_excel/rttf(tennis)/Sportsman(table-tennis).csv', index=False, sep=';', encoding='utf-8-sig')

driver.close()
driver.quit()
