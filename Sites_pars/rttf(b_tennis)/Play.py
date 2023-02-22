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
from bs4 import BeautifulSoup
import requests
import lxml

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

name_player_mass = []
rating_player_mass = []
date_mass = []
tournament_mass = []
time_match_mass = []
status_mass = []
col_man_mass = []
origin_mass = []
stage_mass = []
enemy_mass = []
rating_enemy_mass = []
result_match_mass = []
time1_mass = []
time2_mass = []
time3_mass = []
ccilca_sportsman_mass = []

link_mass = []

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
    # time.sleep(1)


    page = requests.get(link)
    soup = BeautifulSoup(page.text, "lxml")
    player_results = soup.find('section', class_='player-results')

    # a = player_results.findAllNext("a")
    try:
        a = player_results.find_all(href=re.compile("tournaments"))
    # except:
    #     pass

        for i in a:
            name_player = driver.find_element(by=By.TAG_NAME, value='h1').text
            rating_player = driver.find_element(by=By.TAG_NAME, value='h3').text
            date = re.search(r"\d{2}.\d{2}.\d{4}", i.text)
            tournament = re.sub(r"\d{2}.\d{2}.\d{4}\s\d{2}:\d{2}\s", "", i.text, 1)
            time_match = re.search(r"\d{2}:\d{2}", i.text)
            status = re.sub(r"\d{2}.\d{2}.\d{4}\s\d{2}:\d{2}\s", "", i.text, 1)



            # time.sleep(1)
            # print('asd')
            table = player_results.find('a', attrs={"href": f'{i.get("href")}'}).find_next_sibling("table")
            td = table.find('tbody').findAll('td')
            col_man = player_results.find('a', attrs={"href": f'{i.get("href")}'}).next_sibling.text
            # time.sleep(1)

            origin = td[0].text
            stage = td[1].text
            enemy = td[2].text
            rating_enemy = td[3].text
            result_match = td[4].text
            time1 = td[5].text
            time2 = td[6].text
            time3 = td[7].text

            name_player_mass.append(name_player)
            rating_player_mass.append(rating_player)
            date_mass.append(date.group(0))
            tournament_mass.append(tournament)
            time_match_mass.append(time_match.group(0))
            status_mass.append(status)
            col_man_mass.append(col_man)
            origin_mass.append(origin)
            stage_mass.append(stage)
            # enemy_mass.append(enemy)
            # rating_enemy_mass.append(rating_enemy)
            # result_match_mass.append(result_match)
            # time1_mass.append(time1)
            # time2_mass.append(time2)
            # time3_mass.append(time3)

            ccilca_sportsman_mass.append(link)

    except:
        pass
    # print()
    # time.sleep(1)




dfPlayer_Inf = pd.DataFrame({
        'Name player': pd.Series(name_player_mass, dtype='object'),
        'Rating player': pd.Series(rating_player_mass, dtype='object'),
        'Data': pd.Series(date_mass, dtype='object'),
        'Tournament': pd.Series(tournament_mass, dtype='object'),
        'Time match': pd.Series(time_match_mass, dtype='object'),
        'Status': pd.Series(status_mass, dtype='object'),
        'col_man': pd.Series(col_man_mass, dtype='object'),
        'origin': pd.Series(origin_mass, dtype='object'),
        'enemy': pd.Series(enemy_mass, dtype='object'),
        'rating': pd.Series(rating_enemy_mass, dtype='object'),
        'result_match': pd.Series(result_match_mass, dtype='object'),
        'Time1': pd.Series(time1_mass, dtype='object'),
        'Time2': pd.Series(time2_mass, dtype='object'),
        'Time3': pd.Series(time3_mass, dtype='object'),

        'Link': pd.Series(ccilca_sportsman_mass, dtype='object'),
    })

dfPlayer_Inf.to_csv(r'/Users/macbookpro/Desktop/Project/Parser_data/Table_excel/rttf(tennis)/Play(table-tennis).csv', index=False, sep=';', encoding='utf-8-sig')

driver.close()
driver.quit()
