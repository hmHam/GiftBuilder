'''英単語用のdbに追加する。
'''
import sqlite3
import pandas as pd

DB_NAME = 'eng_words.db'
TABLE_NAME = 'TOEFL_2500_BASE'

DATA_FILE_NAME = 'words.csv'
con = sqlite3.connect(DB_NAME)
cur = con.cursor()

df = pd.read_csv(DATA_FILE_NAME).dropna(how='all')
for i, row in df.iterrows():
    cur.execute(
        f"insert into {TABLE_NAME}(Q_NUM, ENG_WORD, JP_WORD) values(?, ?, ?)",
        (row['q_num'], row['eng_word'], row['jp_word'])
    )
con.commit()
cur.close()