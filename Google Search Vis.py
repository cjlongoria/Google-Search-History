import sqlite3
from collections import Counter
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style
from tqdm import tqdm

style.use('ggplot')

IMG_DIR = "C:/Users/curti/OneDrive/Documents/Python Scripts/Google Search History"
IMG_FOLDER ="SavedGraphs"
conn = sqlite3.connect('C:/Users/curti/OneDrive/Documents/Python Scripts/Google Search History/My Life.db')
c = conn.cursor()

DAY = 86400
WEEK = 7 * DAY
MONTH = 30 * DAY
HALFYEAR = 180 * DAY
WINDOW = 3 * MONTH
SLIDE = 1 * DAY


def build_timeframe():
    c.execute('SELECT MAX(unix) FROM WORDS')
    max = c.fetchall()[0][0]

    c.execute('SELECT MIN(unix) FROM WORDS')
    min = c.fetchall()[0][0]
    
    START = min
    END = min + WINDOW

    counter = 0
    while END < max:
        print(f'Image: {counter}')
        c.execute(f'SELECT word FROM words WHERE unix > {START} AND unix < {END}')
        data = c.fetchall()
        
        words = [words[0] for words in data]
        word_counter = Counter(words)
        common_words = [word[0] for word in word_counter.most_common(10)]
        common_words_count = [word[1] for word in word_counter.most_common(10)]

        y_pos = np.arange(len(common_words))
        plt.figure(figsize=(12,7))
        plt.bar(y_pos, common_words_count, align='center', alpha=.5)
        plt.xticks(y_pos, common_words)
        plt.ylabel('Count')
        plt.title(f'{datetime.fromtimestamp(END).day}-{datetime.fromtimestamp(END).strftime("%b")}-{datetime.fromtimestamp(END).year}   (3 Previous Months)')
        plt.savefig(f'{IMG_DIR}/{IMG_FOLDER}/{counter}.png')
        #plt.show()
        plt.close()

        counter +=1
        START += SLIDE
        END += SLIDE
    print('*******************')
    print('All visuals created')
    print('*******************')

def count_entries():
    c.execute('SELECT COUNT(*) FROM WORDS')
    count = c.fetchall()[0][0]
    print(f'Total entries:  {count}')

build_timeframe()
conn.commit()
conn.close()
