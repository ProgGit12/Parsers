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
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Create webdriver
# s = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome()
driver = webdriver.Remote(command_executor='http://localhost:4444')

print("OK")
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

# Create DataFrame
dfPlayer_Inf = pd.DataFrame({
        'Name player': pd.Series(name_player_mass, dtype='object'),
        'Rating player': pd.Series(rating_player_mass, dtype='object'),
        'Data': pd.Series(date_mass, dtype='object'),
        'Tournament': pd.Series(tournament_mass, dtype='object'),
        'Time match': pd.Series(time_match_mass, dtype='object'),
        'Status': pd.Series(status_mass, dtype='object'),
        'Col man': pd.Series(col_man_mass, dtype='object'),
        'Stage': pd.Series(stage_mass, dtype='string'),
        'Number enemy': pd.Series(number_enemy_mass, dtype='object'),
        'Origin': pd.Series(origin_mass, dtype='object'),
        'Enemy': pd.Series(enemy_mass, dtype='object'),
        'Rating enemy': pd.Series(rating_enemy_mass, dtype='object'),
        'Result match': pd.Series(result_match_mass, dtype='int'),
        'Time1': pd.Series(time1_mass, dtype='object'),
        'Time2': pd.Series(time2_mass, dtype='object'),

        'Link': pd.Series(ccilca_sportsman_mass, dtype='object'),
})


driver.get(f"https://chrome.google.com/webstore/detail/miblocker-ad-block/jbolpidmijgjfkcpndcngibedciomlhd/related?hl=ru")
time.sleep(10)


for link in range(1, 5):
    # Open website
    driver.get(f'https://rttf.ru/players/{link}')
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.5)

    # Include BeautifulSoup4 and parse all tournaments
    soup = BeautifulSoup(requests.get(f'https://rttf.ru/players/{link}').text, "lxml")
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
            number_enemy = 0  # numerators enemy

            # Information about tournament from tag <a>
            time_match = re.search(r"\d{2}:\d{2}", i.text)[0]
            name_player = driver.find_element(by=By.TAG_NAME, value='h1').text
            rating_player = driver.find_element(by=By.CLASS_NAME, value='player-info').find_element(by=By.TAG_NAME, value='h3').find_element(by=By.TAG_NAME, value='dfn').text
            date = re.search(r"\d{2}.\d{2}.\d{4}", i.text)[0]
            tournament = re.sub(r"\d{2}.\d{2}.\d{4}\s\d{2}:\d{2}\s|\d{2}.\d{2}.\d{4}\s", "", i.text, 1)
            status = re.sub(r"\d{2}.\d{2}.\d{4}\s\d{2}:\d{2}\s|\d{2}.\d{2}.\d{4}\s", "", i.text, 1)
            status = re.sub(r"\s.{1,200}", "", status, 1)
            col_man = player_results.find('a', attrs={"href": f'{i.get("href")}'}).next_sibling.text

            # Information with table
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
                number_enemy += 1

                # Append in DataFrame
                dfPlayer_Inf.loc[len(dfPlayer_Inf.index)] = [name_player, rating_player, date, tournament, time_match, status, col_man, stage, number_enemy, origin, enemy, rating_enemy, result_match, time1, time2, link]
    except:
        pass

dfPlayer_Inf.to_csv(r'/app/Play(table-tennis).csv', index=False, sep=';', encoding='utf-8-sig')

driver.close()
driver.quit()
