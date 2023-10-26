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

# Здесь создаю браузер
driver = webdriver.Chrome('/Users/macbookpro/Desktop/Project/Parser/Programm/driver/chromedriver')

link_mass = []
name_mass = []
citizenship_mass = []
birthday_mass = []
place_of_birth_mass = []
ccilca_sportsman_mass = []
buttons_mass = []



driver.get(f"https://rusboxing.ru/professional-boxing/boxers")
time.sleep(4)

navigation = driver.find_element(by=By.XPATH, value='/html/body/div/div[2]/div/div[2]/div[2]/div/section[2]/div/div[2]/div[2]/div').find_elements(by=By.TAG_NAME, value='div')

for buttons in navigation:
    buttons_mass.append(buttons)

for click_navigations in buttons_mass:
    click_navigations.click()
    time.sleep(1)
    tags_a = driver.find_element(by=By.CLASS_NAME, value='boxers__content').find_elements(by=By.TAG_NAME, value='a')

    for s in tags_a:
        link_mass.append(s.get_attribute('href'))

    for link in link_mass:
        driver.get(link)
        time.sleep(2)
        try:
            li = driver.find_element(by=By.CLASS_NAME, value='boxer-card__info').find_elements(by=By.TAG_NAME, value='li')

            name = 0
            birthday = 0
            place_of_birth = 0
            citizenship = 0

            for glav in li:
                if re.sub(r":\n.{1,200}", "", glav.text, 1) == "Имя":
                    name = re.sub(r".{1,200}:\W", "", glav.text, 1)
                elif re.sub(r":\n.{1,200}", "", glav.text, 1) == "Отчество":
                    surname = re.sub(r".{1,200}:\W", "", glav.text, 1)
                    name = f"{name} {surname}"
                elif re.sub(r":\n.{1,200}", "", glav.text, 1) == "День рождения":
                    birthday = re.sub(r".{1,200}:\W", "", glav.text, 1)
                elif re.sub(r":\n.{1,200}", "", glav.text, 1) == "Место рождения":
                    place_of_birth = re.sub(r".{1,200}:\W", "", glav.text, 1)
                elif re.sub(r":\n.{1,200}", "", glav.text, 1) == "Гражданство":
                    citizenship = re.sub(r".{1,200}:\W", "", glav.text, 1)


            name_mass.append(name)
            birthday_mass.append(birthday)
            place_of_birth_mass.append(place_of_birth)
            citizenship_mass.append(citizenship)

            ccilca_sportsman_mass.append(link)

            time.sleep(1)
        except:
            pass
        print()



dfPlayer_Inf = pd.DataFrame({
        'Name': pd.Series(name_mass, dtype='object'),
        'Birthday': pd.Series(birthday_mass),
        'Place_of_Birth': pd.Series(place_of_birth_mass),
        'citizenship': pd.Series(citizenship_mass),

        'Link': pd.Series(ccilca_sportsman_mass),
    })

dfPlayer_Inf.to_csv(r'/Users/macbookpro/Desktop/Project/Parser_data/Table_excel/Rusboxing(box)/Sportsman(box).csv', index=False, sep=';', encoding='utf-8-sig')

driver.close()
driver.quit()
