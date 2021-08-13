'''英単語用のdbを見る
'''
import sqlite3
import pandas as pd

DB_NAME = 'eng_words.db'
TABLE_NAME = 'TOEFL_2500_BASE'

con = sqlite3.connect(DB_NAME)
cur = con.cursor()
cur.execute(f'select * from {TABLE_NAME}')
print(cur.fetchall())
cur.close()