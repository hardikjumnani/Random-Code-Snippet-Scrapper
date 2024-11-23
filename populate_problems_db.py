from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from typing import List
import random
import string
import re
import requests
from bs4 import BeautifulSoup, element

import sqlite3

PROBLEM_PAGES = 69

# Initialize the Selenium WebDriver (e.g., for Chrome)
options = webdriver.ChromeOptions()
options.headless = True  # Run in headless mode if you don't want a visible browser window
driver = webdriver.Chrome(options=options)

'''
# Visit the LeetCode URL
url = "https://leetcode.com/problemset/"
driver.get(url)

# Wait for the page to load (tune this time as needed)
time.sleep(5)  # This gives enough time for Cloudflare's challenges to pass
'''

# setup DB
conn = sqlite3.connect('problems.db')
cursor = conn.cursor()

# Create a table
cursor.execute('''
CREATE TABLE IF NOT EXISTS problems (
    srno INT,
    title TEXT,
    rel_href TEXT
)
''')

URL = {
    'problemset': f'https://leetcode.com/problemset', # /?page={5}',
    'problems': f'https://leetcode.com/problems'
}

for i in range(1, PROBLEM_PAGES):
    driver.get(URL['problemset'] + '/?page=' + str(i))
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # print(soup.prettify())

    internet_connected = False
    div_rowgroup: element.ResultSet = soup.find_all('div', role="rowgroup")
    div_problemset: None | element.Tag = None
    for div in div_rowgroup:
        if len(div.find_all('div', role="row")) > 0:
            div_problemset = div
            internet_connected = True

    del div_rowgroup
    if not internet_connected:
        raise Exception('Couldn\'t connect to the servers!')

    for prob_div in div_problemset:
        cells = prob_div.find_all('div')
        
        is_premium_problem = len(cells[1].find_all('svg')) != 0
        if is_premium_problem : continue

        prob_string: str = cells[1].text
        try: prob_no, prob_name = prob_string.split('. ')
        except ValueError: print(prob_string)
        prob_href = prob_name

        # Title -> Href
        for punc in string.punctuation:
            prob_href = prob_href.replace(punc, '')
        
        prob_href = prob_href.replace(' ', '-')
        prob_href = prob_href.lower()

        cursor.execute('INSERT INTO problems (srno, title, rel_href) VALUES (?, ?, ?)', (prob_no, prob_name, prob_href))
    conn.commit()


conn.close()