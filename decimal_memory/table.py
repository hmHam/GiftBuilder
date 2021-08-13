import sqlite3

def create_table(cur):
    cur.execute('''
    CREATE TABLE RESULT (
        DATE TEXT,
        DURATION_MINUTE INTEGER,
        DURATION_SECOND INTEGER,
        SCORE INTEGER
    );''')


def fetchall(cur):
    cur.execute('select * from RESULT')


def record_result(cur, date, duration_minute, duration_second, score):
    cur.execute(
        'insert into result(date, duration_minute, duration_second, score) values(?, ?, ?, ?)',
        (date, duration_minute, duration_second, score)
    )

if __name__ == '__main__':
    con = sqlite3.connect('history.db')
    cur = con.cursor()
    create_table(cur)
    cur.close()