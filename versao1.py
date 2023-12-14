import time
import requests
import pandas as pd 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import json

# 5 -  Converter e salvar em um arquivo JSON

# 1 -  Pegar conteúdo HTML a partir da URL
#url = "https://stats.nba.com/players/traditional/?PerMode=Totals&Season=2019-20&SeasonType=Regular%20Season&sort=PLAYER_NAME&dir=-1"
url = "https://www.nba.com/stats/players/traditional"

option = Options()
option.headless = True #essa opção faz rodar tudo em background
#driver = webdriver.Firefox(options=option)   # sem ativar o headless
driver = webdriver.Firefox()
driver.get(url)

time.sleep(20)

driver.find_element(By.XPATH, "//div[@class='Crom_container__C45Ti crom-container']//table[@class='Crom_table__p1iZz']//thead//tr[@class='Crom_headers__mzI_m']//th[@field='PTS']").click()
driver.find_element(By.XPATH, "//div[@class='Crom_container__C45Ti crom-container']//table[@class='Crom_table__p1iZz']//thead//tr[@class='Crom_headers__mzI_m']//th[@field='PTS']").click() #colocar em ordem decresc.
#driver.quit()

element = driver.find_element(By.XPATH, "//div[@class='Crom_container__C45Ti crom-container']//table[@class='Crom_table__p1iZz']")
html_content = element.get_attribute('outerHTML')

print(html_content)

# 2 -  Parsear o conteúdo HTML - BeaultifulSoup # 
soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find(name='table')


# 3 -  Estruturar o conteúdo em um Data Frame - Pandas
df_full = pd.read_html( str(table))[0].head(10) #limitar a 10. array começa do 0
print(df_full)

#df = df_full[['Unnamed: 0', 'PLAYER', 'TEAM', 'PTS']]
df = df_full[['Unnamed: 0', 'Player', 'Team', 'PTS']] # nesse caso, pegou o nome entre <th> </th>
df.columns = ['pos', 'nome', 'time', 'total']

print(df) 

# 4 -  Transformasr os Dados em um dicionário de dados próprio
top10ranking = {}
top10ranking['points'] = df.to_dict('records') # criacao chave points

print(top10ranking['points'])

js = json.dumps(top10ranking)
fp = open('ranking.json', 'w')
fp.write(js)
fp.close()