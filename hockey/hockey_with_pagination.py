import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

data_rows = []
for p in range(1,25):
    url = f"https://www.scrapethissite.com/pages/forms/?page_num={p}"
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Now scraping page {p}.")
    s = bs(response.text, 'html.parser')
    if p == 1:
        columns = [c.get_text(strip=True) for c in s.find_all('th')]
    
    
    table = s.find('table', class_='table').prettify()
    for tr in s.find_all('tr')[1::]:
        row = [x.get_text(strip=True) for x in tr.find_all('td')]
        data_rows.append(row)

    time.sleep(0.2) # Add a wait time to avoid overloading the server

df = pd.DataFrame(data_rows, columns=columns)
print(df.head())
print(df.shape)
