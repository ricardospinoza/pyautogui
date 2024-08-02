import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import openpyxl

# Configuração do Selenium para usar o Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Executa o Chrome em modo headless (sem interface gráfica)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Inicialização do WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# URL da página principal do CoinMarketCap
url = "https://coinmarketcap.com/"

# Acessando a página
driver.get(url)

# Definindo uma função para rolar e esperar
def scroll_and_wait(scroll_pause_time):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Rolar a página gradualmente para carregar todos os elementos
scroll_pause_time = 2  # Tempo de espera entre os scrolls
increment = 1000  # Pixels para rolar a cada incremento

while True:
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(0, last_height, increment):
        driver.execute_script(f"window.scrollBy(0, {increment});")
        time.sleep(scroll_pause_time)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break

# Obtendo o conteúdo HTML da página
html = driver.page_source
driver.quit()

# Analisando o conteúdo da página com BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Criando uma lista para armazenar os dados
data = []

# Encontrando todos os elementos de ranking e símbolo
rank_elements = soup.select('p[class$="jBOvmG"]')
symbol_elements = soup.select('p[class$="coin-item-symbol"]')

# Iterando sobre os elementos encontrados
for rank, symbol in zip(rank_elements, symbol_elements):
    data.append([rank.text.strip(), symbol.text.strip()])
    time.sleep(0.1)  # Adicionando uma pequena espera para processar os dados

# Verificando se há dados extraídos
if data:
    # Criando um DataFrame com os dados
    df = pd.DataFrame(data, columns=['Rank', 'Symbol'])

    # Nome do arquivo Excel
    file_name = 'coinmarketcap_rankings.xlsx'

    # Nome da aba baseado na data atual
    sheet_name = datetime.now().strftime('%Y-%m-%d')

    # Verificando se o arquivo Excel já existe
    if os.path.exists(file_name):
        # Abrindo o arquivo existente e sobrescrevendo a aba
        with pd.ExcelWriter(file_name, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    else:
        # Criando um novo arquivo Excel
        with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"Dados salvos na aba '{sheet_name}' do arquivo '{file_name}'")
else:
    print("Nenhum dado foi extraído da tabela de criptomoedas.")
