from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from bs4 import BeautifulSoup, element

import sqlite3

CODE_IN_DB = False

# Initialize the Selenium WebDriver (e.g., for Chrome)
options = webdriver.ChromeOptions()
options.headless = True  # Run in headless mode if you don't want a visible browser window
driver = webdriver.Chrome(options=options)

with sqlite3.connect('problems.db') as conn:
    cursor = conn.cursor()
    cursor.execute('SELECT * from problems')
    problem_list = cursor.fetchall()

conn = sqlite3.connect('solutions.db')
cursor = conn.cursor()

# Create a table
create_table = '''
CREATE TABLE IF NOT EXISTS solutions (
    srno INT,
    prob_srno INT,
    coder_href TEXT,
    rel_href TEXT,
    code_language TEXT,
    code_length TEXT,
    code TEXT
)
''' if CODE_IN_DB else ''' CREATE TABLE IF NOT EXISTS solutions (
    srno INT,
    prob_srno INT,
    coder_href TEXT,
    rel_href TEXT,
    code_language TEXT,
    code_length TEXT
)
'''
cursor.execute()

URL = {
    'leetcode': f'https://leetcode.com',
    'problemset': f'https://leetcode.com/problemset',
    'problems': f'https://leetcode.com/problems'
}

solu_srno = 1
prob_srno = 1
for prob in problem_list[:]:
    # print('\nNew Problem', prob)
    prob_no, prob_title, prob_href = prob
    driver.get(f'{URL["problems"]}/{prob_href}/solutions')
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    solutions_divs = soup.find_all('div', class_=['flex', 'w-full', 'flex-col'])
    try: solutions_divs = [div for div in solutions_divs if set(div['class']) == {'flex', 'w-full', 'flex-col'}][0].find_all('div', recursive=False)
    except: continue

    for solu in solutions_divs:
        # print('\nok', solu)
        if 'group/ads' in solu['class']: continue
        try:
            coder_href, _, solu_href = map(lambda a: a.get('href'), solu.find_all('a'))

            # print(f'{URL["leetcode"]}{solu_href}')
            driver.get(f'{URL["leetcode"]}{solu_href}')
            time.sleep(5)

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            max_ = 0
            solu_code = None
            for code in soup.find_all('code'):
                if len(code.text) > max_:
                    solu_code = code
                    max_ = len(code.text)
            
            solu_code_language = solu_code['class'][0].replace('language-', '')
            solu_code_length = max_
            solu_code = solu_code.text
        except: continue
        else:
            if CODE_IN_DB: cursor.execute('INSERT INTO solutions \
                                  (srno, prob_srno, coder_href, rel_href, code_language, code_length, code) \
                                  VALUES (?, ?, ?, ?, ?, ?, ?)',
                                  (solu_srno, prob_srno, prob_href, coder_href, solu_href, solu_code_language, solu_code)
                                  )
            else: cursor.execute('INSERT INTO solutions \
                                  (srno, prob_srno, coder_href, rel_href, code_language, code_length) \
                                  VALUES (?, ?, ?, ?, ?, ?)',
                                  (solu_srno, prob_srno, prob_href, coder_href, solu_href, solu_code_language)
                                  )
            conn.commit()

            solu_srno += 1

    
    prob_srno += 1

conn.close()