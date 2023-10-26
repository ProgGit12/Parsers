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

driver = webdriver.Chrome('C:/Parser-main/driver/chromedriver.exe', options=options)
PrintDf = np.arange(10, 100000, 500)
name_player_mass = []
rating_player_mass = []
date_mass = []
tournament_mass = []
time_match_mass = []
status_mass = []
col_man_mass = []
origin_mass = []
stage_mass = []
number_enemy_mass = []
enemy_mass = []
rating_enemy_mass = []
result_match_mass = []
time1_mass = []
time2_mass = []
time3_mass = []
ccilca_sportsman_mass = []

link_mass = []
mass_errors = []
mass_errors_link = []

dfPlayer_Inf = pd.DataFrame({
        'Name player': pd.Series(name_player_mass, dtype='object'),
        'Rating player': pd.Series(rating_player_mass, dtype='int64'),
        'Data': pd.Series(date_mass, dtype='datetime64[ns]'),
        'Tournament': pd.Series(tournament_mass, dtype='object'),
        'Time match': pd.Series(time_match_mass, dtype='datetime64[ns]'),
        'Status': pd.Series(status_mass, dtype='object'),
        'Col man': pd.Series(col_man_mass, dtype='int64'),
        'Stage': pd.Series(stage_mass, dtype='string'),
        'Number enemy': pd.Series(number_enemy_mass, dtype='int64'),
        'Origin': pd.Series(origin_mass, dtype='object'),
        'Enemy': pd.Series(enemy_mass, dtype='object'),
        'Rating enemy': pd.Series(rating_enemy_mass, dtype='int64'),
        'Result match': pd.Series(result_match_mass, dtype='object'),
        'Time1': pd.Series(time1_mass, dtype='float64'),
        'Time2': pd.Series(time2_mass, dtype='float64'),

        'Link': pd.Series(ccilca_sportsman_mass, dtype='object'),
})

# https://rttf.ru/players/314473
# continue
for link in range(1, 100000):
    t0 = time.time()
# for link in range(0, 3):/
    driver.get(f'https://rttf.ru/players/{link}')
    A = 0
    try:
        driver.find_element(by=By.CLASS_NAME, value='page404')
    except:
        A = 1
    if A != 1:
        # print(link, ' А!=1, Запускаем continue')
        continue
    # print(link, ' А=1, Запускаем обработчик')
    time.sleep(0.2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.2)
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # time.sleep(3)

    page = requests.get(f'https://rttf.ru/players/{link}')
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
        stage = 0
        number_enemy = 0
        origin = 0
        enemy = 0
        rating_enemy = 0
        result_match = 0
        time1 = 0
        time2 = 0

        for i in a:
            number_enemy = 0
            if re.search(r"\d{2}:\d{2}", i.text) != None:
                time_match = re.search(r"\d{2}:\d{2}", i.text)[0]
            else:
                time_match = 0

            name_player = driver.find_element(by=By.TAG_NAME, value='h1').text
            rating_player = driver.find_element(by=By.CLASS_NAME, value='player-info').find_element(by=By.TAG_NAME, value='h3').find_element(by=By.TAG_NAME, value='dfn').text
            date = re.search(r"\d{2}.\d{2}.\d{4}", i.text)[0]
            tournament = re.sub(r"\d{2}.\d{2}.\d{4}\s\d{2}:\d{2}\s|\d{2}.\d{2}.\d{4}\s", "", i.text, 1)
            # tournament = re.sub(r".{1,200}\s", "", tournament, 1)
            status = re.sub(r"\d{2}.\d{2}.\d{4}\s\d{2}:\d{2}\s|\d{2}.\d{2}.\d{4}\s", "", i.text, 1)
            status = re.sub(r"\s.{1,200}", "", status, 1)
            col_man = player_results.find('a', attrs={"href": f'{i.get("href")}'}).next_sibling.text


            table = player_results.find('a', attrs={"href": f'{i.get("href")}'}).find_next_sibling("table")
            tr = table.find('tbody').find('tr')
            while tr != None:
                number_enemy += 1

                td = tr.findAll('td')

                origin = td[0].text
                stage = td[1].text
                enemy = td[2].text
                rating_enemy = td[3].text
                result_match = td[4].text
                time1 = td[5].text
                time2 = td[6].text

                tr = tr.next_sibling
                Line = [name_player, rating_player, date, tournament, time_match, status, col_man, stage, number_enemy, origin,
                 enemy, rating_enemy, result_match, time1, time2, f'https://rttf.ru/players/{link}']
                dfPlayer_Inf.loc[len(dfPlayer_Inf.index)] = Line
                # print(Line)
                if link in PrintDf:
                    dfPlayer_Inf.to_csv(r'C:/Parser-main/Table_excel/rttf(tennis)/Play(table-tennis).csv', index=False,
                                        sep=';', encoding='utf-8-sig')

                    # [name_player, rating_player, date, tournament, time_match, status, col_man, stage, number_enemy, origin, enemy, rating_enemy, result_match, time1, time2, f'https://rttf.ru/players/{link}']
    except:
        # print(link)
        e = sys.exc_info()[1]
        mass_errors_link.append(f'https://rttf.ru/players/{link}')
        mass_errors.append(e.args[0])
        pass
    t1 = time.time()
    print('t=', t1-t0)
dfPlayer_Inf.to_csv(r'C:/Parser-main/Table_excel/rttf(tennis)/Play(table-tennis).csv', index=False, sep=';', encoding='utf-8-sig')

driver.close()
driver.quit()
