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

driver = webdriver.Chrome('/Users/macbookpro/Desktop/Project/Parser_data/driver/chromedriver', options=options)


name_mass = []
nickname_mass = []
birthday_mass = []
boxrec_id_mass = []
nationality_mass = []
weight_mass = []
height_mass = []
arm_span_mass = []
hand_mass = []
KO_mass = []
place_birth_mass = []
place_of_residence_mass = []

ccilca_sportsman_mass = []
link_mass = []



dfPlayer_Inf = pd.DataFrame({
        'name': pd.Series(name_mass, dtype='object'),
        'nickname': pd.Series(nickname_mass, dtype='object'),
        'Birthday': pd.Series(birthday_mass, dtype='object'),
        'BoxRec ID': pd.Series(boxrec_id_mass, dtype='object'),
        'nationality': pd.Series(nationality_mass, dtype='object'),
        'weight': pd.Series(weight_mass, dtype='object'),
        'height': pd.Series(height_mass, dtype='object'),
        'Arm span': pd.Series(arm_span_mass, dtype='object'),
        'hand': pd.Series(hand_mass, dtype='object'),
        'KO': pd.Series(KO_mass, dtype='object'),
        'Place birth': pd.Series(place_birth_mass, dtype='object'),
        'Place of residence': pd.Series(place_of_residence_mass, dtype='object'),

        'Link': pd.Series(ccilca_sportsman_mass, dtype='object'),
    })



driver.get(f"https://champinon.info/ru/boxing/")
time.sleep(2)

tr = driver.find_elements(by=By.TAG_NAME, value='a')

for s in tr:
    link_mass.append(s.get_attribute("href"))

for link in link_mass:
    # link = href.find_element(by=By.TAG_NAME, value="a").get_attribute("href")
    driver.get(link)

    name = 0
    nickname = 0
    Birthday = 0
    boxrec_id = 0
    nationality = 0
    weight = 0
    height = 0
    arm_span = 0
    hand = 0
    KO = 0
    place_birth = 0
    place_of_residence = 0

    # col-md-8 col-sm-8
    # p = driver.find_element(by=By.CLASS_NAME, value="col-md-8").find_elements(by=By.TAG_NAME, value="p")
    p = driver.find_element(by=By.CLASS_NAME, value="col-md-8")
    # for tr in p:
    #     if tr.find_element(by=By.CLASS_NAME, value="fa").text == "Имя (англ):":
    #         name = tr.text
    #         print()


    # dfPlayer_Inf.loc[len(dfPlayer_Inf.index)] = [name, rating, birthday, citizenship,
    #                                              hand, discharge, base, trim_right,
    #                                              trim_left, visiting]
    time.sleep(1)

driver.close()
driver.quit()
