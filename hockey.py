# A demonstration of web scraping

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

url = "https://www.scrapethissite.com/pages/forms/"
response = requests.get(url)
if response.status_code == 200:
    print("Successfully talked to the website.")

s = bs(response.text, 'html.parser')
table = s.find('table', class_='table').prettify()
# print(table)

columns = [c.get_text(strip=True) for c in s.find_all('th')]
# print(columns)

rows = []
for tr in s.find_all('tr'):
    row = [x.get_text(strip=True) for x in tr.find_all('td')]
    rows.append(row)

df = pd.DataFrame(rows, columns=columns)

print(df.head())
print(df.shape)
