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
options.add_experimental_option(
    'prefs',
    {
        'profile.managed_default_content_settings.javascript': 2,
        'profile.managed_default_content_settings.images': 2,
        'profile.managed_default_content_settings.mixed_script': 2,
    }
)

driver = webdriver.Chrome('/Users/macbookpro/Desktop/Project/Parser/Programm/chromdriver/chromedriver', options=options)
# driver.get("https://www.sports.ru/boxing/sportsman/")

link_mass = []
name_mass = []
citizenship_mass = []
birthday_mass = []
weight_mass = []
height_mass = []
place_of_birth_mass = []
hand_mass = []
sex_mass = []
ccilca_sportsman_mass = []



for i in range(1,25):
    driver.get(f"https://www.liveresult.ru/tennis/players/p{i}")
    time.sleep(3)

    a = driver.find_elements(by=By.CLASS_NAME, value='card-media-left')

    for a_link in a:
        # print(a_link.get_attribute('href'))
        link_mass.append(a_link.get_attribute('href'))

    for link in link_mass:
        # print(link)
        driver.get(link)

        td_glavnoe = driver.find_elements(by=By.CLASS_NAME, value='col-7')
        th_glavnoe = driver.find_elements(by=By.CLASS_NAME, value='col-5')

        td_dop = driver.find_elements(by=By.CLASS_NAME, value='col-8')
        th_dop = driver.find_elements(by=By.CLASS_NAME, value='col-4')
        # dt = driver.find_elements(by=By.CLASS_NAME, value='col-5')
        # th = driver.find_elements(by=By.CLASS_NAME, value='col-7')

        ##
        birthday_index = 25
        height_index = 25
        weight_index = 25

        citizenship_index = 25
        place_of_birth_index = 25
        hand_index = 25
        sex_index = 25

        for glav in th_glavnoe:
            if glav.text == "Дата рождения":
                birthday_index = th_glavnoe.index(glav) # th.index(glav) - это индекс элемента в массиве заголовков

            elif glav.text == "Вес":
                weight_index = th_glavnoe.index(glav)

            elif glav.text == "Рост":
                height_index = th_glavnoe.index(glav)


        for dop in th_dop:
            if dop.text == "Гражданство":
                citizenship_index = th_dop.index(dop) # th.index(glav) - это индекс элемента в массиве заголовков

            elif dop.text == "Место рождения":
                place_of_birth_index = th_dop.index(dop)

            elif dop.text == "Рука":
                hand_index = th_dop.index(dop)

            elif dop.text == "Пол":
                sex_index = th_dop.index(dop)



        # Это кусок кода, который анализирует данные на сайте


        name = re.sub(r"[(].{1,23}[)]", "", driver.find_element(by=By.CLASS_NAME, value='h3').text, 1)
        height = ''
        weight = ''

        citizenship = ''
        place_of_birth = ''
        hand = ''

        if birthday_index != 25:
            birthday = re.sub(r"\s[(].{1,23}[)]", "", td_glavnoe[birthday_index].text, 1)

        if height_index != 25:
            height = re.sub(r"\s.{1,5}", "", td_glavnoe[height_index].text, 1)

        if weight_index != 25:
            weight = re.sub(r"\s.{1,5}", "", td_glavnoe[weight_index].text, 1)



        if citizenship_index != 25:
            citizenship = td_dop[citizenship_index].text

        if place_of_birth_index != 25:
            place_of_birth = td_dop[place_of_birth_index].text

        if hand_index != 25:
            hand = td_dop[hand_index].text

        if sex_index != 25:
            sex = td_dop[sex_index].text



        name_mass.append(name)
        birthday_mass.append(birthday)
        weight_mass.append(weight)
        height_mass.append(height)

        citizenship_mass.append(citizenship)
        place_of_birth_mass.append(place_of_birth)
        hand_mass.append(hand)
        sex_mass.append(sex)

        ccilca_sportsman_mass.append(link)

        time.sleep(1)

    link_mass.clear()




dfPlayer_Inf = pd.DataFrame({
        'Name': pd.Series(name_mass, dtype='object'),
        'Birthday': pd.Series(birthday_mass),
        'Weight': pd.Series(weight_mass),
        'Height': pd.Series(height_mass),

        'Citizenship': pd.Series(citizenship_mass),
        'Place_of_birth': pd.Series(place_of_birth_mass),
        'Hand': pd.Series(hand_mass),
        'Sex': pd.Series(sex_mass),

        'Link': pd.Series(ccilca_sportsman_mass),
    })

dfPlayer_Inf.to_csv(r'/Users/macbookpro/Desktop/Project/Parser_data/table2.csv', index=False, sep=';', encoding='utf-8-sig')

driver.close()
driver.quit()
