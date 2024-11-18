from selenium import webdriver
from selenium.webdriver.common.by import By
import time

import sqlite3

import random

# Initialize the Selenium WebDriver (e.g., for Chrome)
options = webdriver.ChromeOptions()
options.headless = True  # Run in headless mode if you don't want a visible browser window
driver = webdriver.Chrome(options=options)

URL = {
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

driver.get(URL['problems'] + '/' + row[2])
time.sleep(5)