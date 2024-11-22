from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from bs4 import BeautifulSoup, element

import sqlite3

import random


# Initialize the Selenium WebDriver (e.g., for Chrome)
options = webdriver.ChromeOptions()
options.headless = True  # Run in headless mode if you don't want a visible browser window
driver = webdriver.Chrome(options=options)

URL = {
    'leetcode': f'https://leetcode.com',
    'problemset': f'https://leetcode.com/problemset',
    'problems': f'https://leetcode.com/problems'
}

conn = sqlite3.connect('problems.db')
cursor = conn.cursor()

cursor.execute('SELECT COUNT(*) FROM problems')
row_count = cursor.fetchone()[0]

rand_row_idx = random.randint(0, row_count-1)
cursor.execute('SELECT * FROM problems LIMIT 1 OFFSET ?', (rand_row_idx, ))
row = cursor.fetchone()

driver.get(f'{URL["problems"]}/{row[2]}/solutions')
time.sleep(5)

soup = BeautifulSoup(driver.page_source, 'html.parser')

solutions_divs = soup.find_all('div', class_=['flex', 'w-full', 'flex-col'])
solutions_divs = [div for div in solutions_divs if set(div['class']) == {'flex', 'w-full', 'flex-col'}]
# for i in range(len(solution_divs)): print(solution_divs[i], '\n')

solution_link = solutions_divs[0].find_next('div').find_all('a')[-1].get('href')
# print(solution_link)

driver.get(f'{URL["leetcode"]}{solution_link}')
time.sleep(5)

soup = BeautifulSoup(driver.page_source, 'html.parser')
# print(soup.prettify())
print(soup.find('pre').find('code'))
# for i in soup.find('pre').find('code'): ... # Code to tag converter
