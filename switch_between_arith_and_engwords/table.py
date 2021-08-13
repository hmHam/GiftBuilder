'''英単語用のdbのスキーマを定義する
'''

import sqlite3

con = sqlite3.connect('eng_words.db')
cur = con.cursor()

cur.execute('''
CREATE TABLE TOEFL_2500_BASE (
    Q_NUM INTEGER NOT NULL PRIMARY KEY,
    ENG_WORD TEXT,
    JP_WORD TEXT,
    ENG_EXAMPLE TEXT DEFAULT '',
    JP_EXAMPLE TEXT DEFAULT ''
);''')

cur.close()