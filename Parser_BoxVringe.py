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
driver = webdriver.Chrome('/Users/macbookpro/Desktop/Project/Parser/Programm/chromdriver/chromedriver')
# driver.get("https://www.sports.ru/boxing/sportsman/")

link_mass = []
name_mass = []
citizenship_mass = []
birthday_mass = []
сountry_mass = []
weight_mass = []
height_mass = []
place_of_birth_mass = []
hand_mass = []
sex_mass = []
ccilca_sportsman_mass = []


# try:
for i in range(1,155):
    driver.get(f"https://vringe.com/dossier/search/?PAGEN_1={i}")
    time.sleep(2)

    img = driver.find_elements(by=By.CLASS_NAME, value='name')

    for mass in img:
        img_mass = mass.find_elements(by=By.TAG_NAME, value='a')
        for link12 in img_mass:
            link_mass.append(link12.get_attribute('href'))

    for link in link_mass:
        driver.get(link)

        divs = driver.find_elements(by=By.CLASS_NAME, value='dprop')

        ##
        birthday_index = 25
        height_index = 25
        сountry_index = 25

        place_of_birth_index = 25
        hand_index = 25

        for glav in divs:
            if glav.find_element(by=By.TAG_NAME, value='span').text == "Дата рождения:":
                birthday_index = divs.index(glav) # th.index(glav) - это индекс элемента в массиве заголовков

            elif glav.find_element(by=By.TAG_NAME, value='span').text == "Рост:":
                height_index = divs.index(glav)

            elif glav.find_element(by=By.TAG_NAME, value='span').text == "Место рождения:":
                place_of_birth_index = divs.index(glav)

            elif glav.find_element(by=By.TAG_NAME, value='span').text == "Страна:":
                сountry_index = divs.index(glav)

            elif glav.find_element(by=By.TAG_NAME, value='span').text == "Боевая стойка:":
                hand_index = divs.index(glav)


        # Это кусок кода, который анализирует данные на сайте


        name = driver.find_element(by=By.TAG_NAME, value='h1').text
        height = '0'

        сountry = '0'
        place_of_birth = '0'
        hand = '0'


        if birthday_index != 25:
            birthday = re.sub(r".{1,20}[:]\s", "", divs[birthday_index].text, 1)
            birthday = re.sub(r"\s[(].{1,23}[)]", "", birthday, 1)
        else:
            birthday = "0"

        if height_index != 25:
            height = re.sub(r".{4,5}\s", "", divs[height_index].text, 1)
            height = re.sub(r"\s.{1,4}", "", height, 1)
        else:
            height = "0"


        if hand_index != 25:
            hand = re.sub(r".{2,20}:\s", "", divs[hand_index].text, 1)
        else:
            hand = "0"

        if сountry_index != 25:
            сountry = re.sub(r".{2,20}:\s", "", divs[сountry_index].text, 1)
        else:
            сountry = "0"


        if place_of_birth_index != 25:
            place_of_birth = re.sub(r".{2,20}:\s", "", divs[place_of_birth_index].text, 1)
        else:
            place_of_birth = "0"



        birthday_mass.append(birthday)
        height_mass.append(height)

        сountry_mass.append(сountry)
        hand_mass.append(hand)
        place_of_birth_mass.append(place_of_birth)

        name_mass.append(name)
        ccilca_sportsman_mass.append(link)

        time.sleep(2)


    link_mass.clear()




    dfPlayer_Inf = pd.DataFrame({
            'Name': pd.Series(name_mass, dtype='object'),
            'Birthday': pd.Series(birthday_mass),
            'Height': pd.Series(height_mass),

            'Country': pd.Series(сountry_mass),
            'Place_of_birth': pd.Series(place_of_birth_mass),
            'Hand': pd.Series(hand_mass),

            'Link': pd.Series(ccilca_sportsman_mass),
        })

    dfPlayer_Inf.to_csv(r'/Users/macbookpro/Desktop/Project/Parser_data/table3.csv', index=False, sep=';', encoding='utf-8-sig')

driver.close()
driver.quit()
