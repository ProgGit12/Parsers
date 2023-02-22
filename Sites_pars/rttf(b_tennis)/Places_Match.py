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
# options = Options()
# options.add_experimental_option(
#     'prefs',
#     {
#         'profile.managed_default_content_settings.javascript': 2,
#         'profile.managed_default_content_settings.images': 2,
#         'profile.managed_default_content_settings.mixed_script': 2,
#     }
# )

driver = webdriver.Chrome('/Users/macbookpro/Desktop/Project/Parser_data/chromdriver/chromedriver')

link_mass = []
address_mass = []
club_mass = []
status_mass = []
official_site_club_mass = []
shir_dolg_mass = []
working_hours_mass = []
contact_mass = []
representative_on_site_mass = []
number_of_tables_mass = []

ccilca_club_mass = []


driver.get(f"https://rttf.ru/halls/?title=")
time.sleep(2)

tr = driver.find_elements(by=By.TAG_NAME, value='article')


for s in tr:
    try:
        a = s.find_element(by=By.TAG_NAME, value='a')
        link_mass.append(a.get_attribute('href'))
    except:
        pass

for link in link_mass:
    driver.get(link)

    section = driver.find_element(by=By.CLASS_NAME, value='hall-info')
    p = section.find_elements(by=By.TAG_NAME, value='p')
    name = section.find_element(by=By.TAG_NAME, value='h1').text
    date = 0
    address = 0
    club = 0
    shir_dolg = 0
    official_site_club = 0
    working_hours = 0
    contact = 0
    representative_on_site = 0
    number_of_tables = 0


    for glav in p:
        if re.sub(r"[:]\s.{1,300}", "", glav.text, 1) == "Адрес":
            address = re.sub(r".{1,300}[:]\s", "", glav.text, 1)
        elif re.sub(r"[:]\s.{1,300}", "", glav.text, 1) == "Официальный сайт":
            official_site_club = re.sub(r".{1,300}[:]\s", "", glav.text, 1)
        elif re.sub(r"[:]\s.{1,300}", "", glav.text, 1) == "Время работы":
            working_hours = re.sub(r".{1,300}[:]\s", "", glav.text, 1)
        elif re.sub(r"[:]\s.{1,300}", "", glav.text, 1) == "Контакты":
            contact = re.sub(r".{1,300}[:]\s", "", glav.text, 1)
        elif re.sub(r"[:]\s.{1,300}", "", glav.text, 1) == "Представитель на сайте":
            representative_on_site = re.sub(r".{1,300}[:]\s", "", glav.text, 1)
        elif re.sub(r"[:]\s.{1,300}", "", glav.text, 1) == "Кол-во столов":
            number_of_tables = re.sub(r".{1,300}[:]\s", "", glav.text, 1)

    # driver.get('https://yandex.ru/maps/2/saint-petersburg/?ll=30.315635%2C59.938951&z=11')
    # time.sleep(4)
    # input = driver.find_element(by=By.CLASS_NAME, value='input__control').send_keys(f"{address}\n")
    # time.sleep(4)
    # try:
    #     shir_dolg = driver.find_element(by=By.CLASS_NAME, value='toponym-card-title-view__coords-badge').text
    # except:
    #     pass


    address_mass.append(address)
    club_mass.append(name)
    official_site_club_mass.append(official_site_club)
    working_hours_mass.append(working_hours)
    contact_mass.append(contact)
    representative_on_site_mass.append(representative_on_site)
    number_of_tables_mass.append(number_of_tables)

    ccilca_club_mass.append(link)
    time.sleep(1)


dfPlayer_Inf = pd.DataFrame({
        'Name': pd.Series(club_mass, dtype='object'),
        'Site club': pd.Series(official_site_club_mass, dtype='object'),
        'Address': pd.Series(address_mass, dtype='object'),
        'Working hours': pd.Series(working_hours_mass, dtype='object'),
        'Contact': pd.Series(contact_mass, dtype='object'),
        'Representative on site': pd.Series(representative_on_site_mass, dtype='object'),
        'Number of tables': pd.Series(number_of_tables_mass, dtype='object'),


        'Link': pd.Series(ccilca_club_mass, dtype='object'),
    })

dfPlayer_Inf.to_csv(r'/Users/macbookpro/Desktop/Project/Parser_data/Table_excel/rttf(tennis)/Places_Match(table-tennis).csv', index=False, sep=';', encoding='utf-8-sig')

driver.close()
driver.quit()
