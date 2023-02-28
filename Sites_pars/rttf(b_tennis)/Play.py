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
import sys

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

dfPlayer_Inf = pd.DataFrame({
        'Name player': pd.Series(name_player_mass, dtype='object'),
        'Rating player': pd.Series(rating_player_mass, dtype='object'),
        'Data': pd.Series(date_mass, dtype='object'),
        'Tournament': pd.Series(tournament_mass, dtype='object'),
        'Time match': pd.Series(time_match_mass, dtype='object'),
        'Status': pd.Series(status_mass, dtype='object'),
        'Col man': pd.Series(col_man_mass, dtype='object'),
        'Origin': pd.Series(origin_mass, dtype='object'),
        'Enemy': pd.Series(enemy_mass, dtype='object'),
        'Rating enemy': pd.Series(rating_enemy_mass, dtype='object'),
        'Result match': pd.Series(result_match_mass, dtype='object'),
        'Time1': pd.Series(time1_mass, dtype='object'),
        'Time2': pd.Series(time2_mass, dtype='object'),

        'Link': pd.Series(ccilca_sportsman_mass, dtype='object'),
})


driver.get(f"https://rttf.ru/players/")
time.sleep(10)


tr = driver.find_elements(by=By.TAG_NAME, value='tr')

for a_link in tr:
    try:
        a = a_link.find_elements(by=By.TAG_NAME, value='a')
        link_mass.append(a[0].get_attribute('href'))
    except IndexError:
        pass

print(len(link_mass))
print(link_mass[-1])
print()
for link in link_mass:
    driver.get(link)
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)



    page = requests.get(link)
    soup = BeautifulSoup(page.text, "lxml")
    player_results = soup.find('section', class_='player-results')

    try:
        a = player_results.find_all(href=re.compile("tournaments"))


        name_player = 0
        rating_player = 0
        date = 0
        tournament = 0
        time_match = 0
        status = 0
        col_man = 0
        origin = 0
        stage = 0
        enemy = 0
        rating_enemy = 0
        result_match = 0
        time1 = 0
        time2 = 0

        for i in a:

            if re.search(r"\d{2}:\d{2}", i.text) != None:
                time_match = re.search(r"\d{2}:\d{2}", i.text)[0]
            else:
                time_match = 0

            name_player = driver.find_element(by=By.TAG_NAME, value='h1').text
            rating_player = driver.find_element(by=By.CLASS_NAME, value='player-info').find_element(by=By.TAG_NAME, value='h3').find_element(by=By.TAG_NAME, value='dfn').text
            date = re.search(r"\d{2}.\d{2}.\d{4}", i.text)[0]
            tournament = re.sub(r"\d{2}.\d{2}.\d{4}\s\d{2}:\d{2}\s|\d{2}.\d{2}.\d{4}\s", "", i.text, 1)
            status = re.sub(r"\d{2}.\d{2}.\d{4}\s\d{2}:\d{2}\s|\d{2}.\d{2}.\d{4}\s", "", i.text, 1)
            col_man = player_results.find('a', attrs={"href": f'{i.get("href")}'}).next_sibling.text


            table = player_results.find('a', attrs={"href": f'{i.get("href")}'}).find_next_sibling("table")
            tr = table.find('tbody').find('tr')
            while tr != None:
                td = tr.findAll('td')

                origin = td[0].text
                stage = td[1].text
                enemy = td[2].text
                rating_enemy = td[3].text
                result_match = td[4].text
                time1 = td[5].text
                time2 = td[6].text

                tr = tr.next_sibling
                dfPlayer_Inf.loc[len(dfPlayer_Inf.index)] = [name_player, rating_player, date, tournament, time_match, status, col_man, origin, enemy, rating_enemy, result_match, time1, time2, link]
    except:
        print(link)
        e = sys.exc_info()[1]
        print(e.args[0])
        pass


dfPlayer_Inf.to_csv(r'/Users/macbookpro/Desktop/Project/Parser_data/Table_excel/rttf(tennis)/Play(table-tennis).csv', index=False, sep=';', encoding='utf-8-sig')

driver.close()
driver.quit()
