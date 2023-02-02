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
weight_mass = []
height_mass = []
ccilca_sportsman_mass = []



for i in range(1,30):
    driver.get(f"https://www.sports.ru/boxing/sportsman/?page={i}")
    time.sleep(2)

    a = driver.find_elements(by=By.CLASS_NAME, value='name')
    for a_link in a:
        link_mass.append(a_link.get_attribute('href'))

    for link in link_mass:

        driver.get(link)

        td = driver.find_elements(by=By.TAG_NAME, value='td')
        th = driver.find_elements(by=By.TAG_NAME, value='th')

        ##
        birthday_index = 25
        citizenship_index = 25
        height_index = 25
        weight_index = 25

        for glav in th:
            if (glav.text == "Родился") or (glav.text == "Родилась"):
                birthday_index = th.index(glav) # th.index(glav) - это индекс элемента в массиве заголовков

            elif glav.text == "Гражданство":
                citizenship_index = th.index(glav)

            elif glav.text == "Рост и вес":
                height_index = th.index(glav)
                weight_index = th.index(glav)

            elif glav.text == "Рост":
                height_index = th.index(glav)

            elif glav.text == "Вес":
                weight_index = th.index(glav)
        # Это кусок кода, который анализирует данные на сайте


        name = driver.find_element(by=By.CLASS_NAME, value='titleH1').text
        height = ''
        weight = ''




        if birthday_index != 25:
            birthday = re.sub(r"\s[|]\s.{1,10}", "", td[birthday_index].text, 1)
        else:
            birthday = ""
            pass

        if citizenship_index != 25:
            citizenship = td[citizenship_index].text
        else:
            citizenship = ""
            pass


        if height_index != 25:
            if th[height_index].text == "Рост и вес":
                # print('OK!')
                height = re.sub(r"[|].{1,10}", "", td[height_index].text, 1)
                weight = re.sub(r".{1,10}[|]", "", td[height_index].text, 1)
            else:
                pass

            if th[height_index].text == "Рост":
                height = td[height_index].text
            else:
                pass

        if weight_index != 25:
            if th[weight_index].text == "Вес":
                weight = td[weight_index].text
            else:
                pass



        name_mass.append(name)
        birthday_mass.append(birthday)
        citizenship_mass.append(citizenship)
        weight_mass.append(weight)
        height_mass.append(height)
        ccilca_sportsman_mass.append(link)

    link_mass.clear()




dfPlayer_Inf = pd.DataFrame({
        'Name': pd.Series(name_mass, dtype='object'),
        'Birthday': pd.Series(birthday_mass),
        'Citizenship': pd.Series(citizenship_mass),
        'Weight': pd.Series(weight_mass),
        'Height': pd.Series(height_mass),
        'Link': pd.Series(ccilca_sportsman_mass),
    })

dfPlayer_Inf.to_csv(r'/Users/macbookpro/Desktop/Project/Parser_data/table(Box_Sports.ru).csv', index=False, sep=';', encoding='utf-8-sig')

driver.close()
driver.quit()

