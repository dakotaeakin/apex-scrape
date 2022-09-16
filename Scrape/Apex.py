from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains as AS
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import json


# Login to site
userData = open("userLogin.json")
userData = json.load(userData)

username = userData["user"]["username"]
password = userData["user"]["password"]
account = userData["user"]["account"]

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
driver.implicitly_wait(5)
driver.get('https://public-apps.apexclearing.com/session/#/login/')
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="init_username"]')))
driver.find_element_by_xpath('//*[@id="init_username"]').send_keys("deakin96")
driver.find_element_by_xpath('/html/body/div/div/div/main/div/div/div[2]/div/form/button').click()
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]')))
driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
driver.find_element_by_xpath('/html/body/div/div/div/main/div/div/div[4]/div[1]/form/button').click()
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="account"]')))
driver.find_element_by_xpath('//*[@id="account"]').send_keys(account)

# Navigate for data pull

driver.find_element_by_xpath('//*[@id="app-menu"]/form/div[2]/button').click()
wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/nav[2]/ul[1]/li[2]/a')))


try:
    driver.find_element_by_xpath('/html/body/div[2]/div/nav[2]/ul[1]/div/div[2]/div[1]/div/a[4]').click()
except:
    driver.find_element_by_xpath('/html/body/div[2]/div/nav[2]/ul[1]/li[2]/a').click()
    try:
        driver.find_element_by_xpath('/html/body/div[2]/div/nav[2]/ul[1]/div/div[2]/div[1]/div/a[4]').click()  # Still throws error ocaisionally
    except:
        driver.find_element_by_xpath('/html/body/div[2]/div/nav[2]/ul[1]/li[2]/a').click()
        driver.find_element_by_xpath('/html/body/div[2]/div/nav[2]/ul[1]/div/div[2]/div[1]/div/a[4]').click()  # Still throws error ocaisionally

# Filter data for scrape

start_date = '01/01/2020'
end_date = '12/31/2020'

driver.implicitly_wait(5)
driver.find_element_by_xpath('//*[@id="startDate"]').clear()
driver.find_element_by_xpath('//*[@id="startDate"]').send_keys(start_date)
driver.find_element_by_xpath('//*[@id="endDate"]').clear()
driver.find_element_by_xpath('//*[@id="endDate"]').send_keys(end_date)
driver.find_element_by_xpath('//*[@id="app-menu"]/form/div[6]/button').click()
wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'ui-grid-icon-menu')))
driver.find_element_by_class_name('ui-grid-icon-menu').click()
driver.find_element_by_xpath('//*[@id="menuitem-31"]/button').click()
driver.find_element_by_xpath('//*[@id="menuitem-33"]/button').click()

# Scrape data


def scroll_position_bottom():

    scroll = driver.execute_script("return document.querySelector('.ui-grid-viewport.ng-isolate-scope').scrollHeight")
    client = driver.execute_script("return document.querySelector('.ui-grid-viewport.ng-isolate-scope').clientHeight")
    scroll_bottom = scroll - client
    # print(scroll, client)
    return scroll_bottom


data = []
while driver.execute_script("return document.querySelector('.ui-grid-viewport.ng-isolate-scope').scrollTop") < scroll_position_bottom():
    html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    soup = BeautifulSoup(html, "html.parser")
    soup.select('div', class_='ui-grid-cell-contents ng-binding ng-scope')
    for div in soup.select('div.ui-grid-cell-contents.ng-binding.ng-scope'):
        data.append([div.text.strip()])
    driver.execute_script("return document.querySelector('.ui-grid-viewport.ng-isolate-scope').scrollBy(0, 600)")

pd.set_option("display.max_rows", None, "display.max_columns", None)
df_ = pd.DataFrame(data, columns=['First'])
df = pd.DataFrame(df_.values.reshape(-1, 11), columns=['Type', 'Trade Date', 'Settle Date', 'Symbol', 'Description',
                                                       'Trade Action', 'Qty', 'Price', 'Fees', 'Commision', 'Net Amount'])

conn = sqlite3.connect('raw_data.db')
c = conn.cursor()
# c.execute('''
# CREATE TABLE raw_data ("Type", "Trade Date", "Settle Date", "Symbol", "Description", "Trade Action", "Qty", "Price", "Fees", "Commision", "Net Amount")
#         ''')
# conn.commit()

df.to_sql('raw_data', conn, if_exists='append', index=False)
conn.close()

# c.execute('''
# SELECT * FROM raw_data
#           ''')

# for row in c.fetchall():
#     print(row)
