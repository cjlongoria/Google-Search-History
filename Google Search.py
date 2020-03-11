import os
import sqlite3

import dateutil.parser
from bs4 import BeautifulSoup as bs
from tqdm import tqdm

SEARCH_FILE = "C:/Users/curti/OneDrive/Documents/Python Scripts/Google Search History/MyActivity.html"

conn = sqlite3.connect('C:/Users/curti/OneDrive/Documents/Python Scripts/Google Search History/My Life.db')
c = conn.cursor()

def make_table():
    c.execute('CREATE TABLE IF NOT EXISTS words(id INTEGER PRIMARY KEY, unix REAL, word TEXT)')

def build_db():
    stop_words = ['to', 'i', 'I', 'or', ' ', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'a', 'and', 'the', 'of', 'in', 'how', 'is', 'co', 'The',
     'for', 'how', '2019', '2018', 'an', 'on', 'from', 'and', 'with', 'what', 'vs', 'google', 'Google', '']
    with open(SEARCH_FILE, 'r', encoding='utf8') as f:
        soup = bs(f, 'lxml')
        for entry in tqdm(soup.find_all('div', class_='content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1')):
            try:
                if (entry.text.split(" ")[0] == "Searched"):
                    date = entry.br.next_sibling
                    dt = dateutil.parser.parse(date).timestamp()
                    for word in (entry.find('a').text.split(' ')):
                        word = word.replace('"','')
                        word = word.replace(' ','')
                        if word not in stop_words:
                            c.execute('INSERT INTO words (unix, word) VALUES (?, ?)', (dt, word))
            except Exception as e:
                print(str(e))
    print('*********************')
    print('Search database built')
    print('*********************')
    
                
make_table()        
build_db()
conn.commit()
conn.close()

