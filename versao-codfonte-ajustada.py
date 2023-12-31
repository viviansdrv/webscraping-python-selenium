# -*- encoding: utf-8 -*-

import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import json

# Grab content from URL (Pegar conteúdo HTML a partir da URL)
url = "https://www.nba.com/stats/players/traditional"
top10ranking = {}

rankings = {
    '3points': {'field': 'FG3M', 'label': '3PM'},
    'points': {'field': 'PTS', 'label': 'PTS'},
    'assistants': {'field': 'AST', 'label': 'AST'},
    'rebounds': {'field': 'REB', 'label': 'REB'},
    'steals': {'field': 'STL', 'label': 'STL'},
    'blocks': {'field': 'BLK', 'label': 'BLK'},
}


def buildrank(type):

    field = rankings[type]['field']
    label = rankings[type]['label']
    
    driver.find_element(By.XPATH, 
                        f"//div[@class='Crom_container__C45Ti crom-container']//table[@class='Crom_table__p1iZz']//thead//tr[@class='Crom_headers__mzI_m']//th[@field='{field}']").click()


    element = driver.find_element(By.XPATH, 
        "//div[@class='Crom_container__C45Ti crom-container']//table[@class='Crom_table__p1iZz']")
    html_content = element.get_attribute('outerHTML')

    # Parse HTML (Parsear o conteúdo HTML) - BeaultifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find(name='table')

    # Data Structure Conversion (Estruturar conteúdo em um Data Frame) - Pandas
    df_full = pd.read_html(str(table))[0].head(10)
    df = df_full[['Unnamed: 0', 'Player', 'Team', label]]
    df.columns = ['pos', 'player', 'team', 'total']

    # Convert to Dict (Transformar os Dados em um Dicionário de dados próprio)
    return df.to_dict('records')


option = Options()
option.headless = True
driver = webdriver.Firefox(options=option)

driver.get(url)
driver.implicitly_wait(10)  # in seconds

for k in rankings:
    top10ranking[k] = buildrank(k)

driver.quit()

# Dump and Save to JSON file (Converter e salvar em um arquivo JSON)
with open('ranking.json', 'w', encoding='utf-8') as jp:
    js = json.dumps(top10ranking, indent=4)
    jp.write(js)