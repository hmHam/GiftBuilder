
import speech, sound, time
import random
import ui
import numpy as np
import sqlite3
con = sqlite3.connect('eng_words.db')
cur = con.cursor()

# 単語の読み込み
TABLE_NAME = 'TOEFL_2500_BASE'
# TABLE_NAME = 'TOEFL_2500_ADVANCE'
cur.execute('select * from {}'.format(TABLE_NAME))
words = cur.fetchall()
chunk = random.sample(words, 12)
cur.close()

Q_NUM_IDX = 0
ENG_WORD_IDX = 1
JP_WORD_IDX = 2

def next_words(sender):
	label = sender.superview['label1']
	tb = sender.superview['table']
	
	global chunk
	if len(chunk) == 0:
		chunk = random.sample(words, 12)
	label.text = '%d/12' % len(chunk)
	next_q = []
	for _ in range(3):
		w = chunk.pop()
		eng_w = w[ENG_WORD_IDX]
		next_q.append(eng_w)
		jp_w = w[JP_WORD_IDX]
		next_q.append(jp_w[:30])
		next_q.append('' if len(jp_w) < 30 else jp_w[30:])
	del next_q[-1]
	tb.data_source = ui.ListDataSource(next_q)
	
	tb.data_source.font = ('<system>', 12)
	tb.reload_data()

# 音声読み上げ => 音声入力待機
# 音声入力 => 正解判定
# 丸 => 正解音。バツ => 不正解音。
Base = 3
weight = 1.5
weight1 = 1.5

#TODO: interval とx, yの値を取得する範囲を入力する
#      UIを作る

def add():
 '''足し算の処理'''
 x = random.randint(*(2, 100))
 y = random.randint(*(2, 100))
 speech.say("%d plus %d equals?" % (x, y))
 ans = x + y
 time.sleep(weight1 * Base)
 speech.say("%d" % ans)
 return ans
    
def sub():
 '''引き算の処理'''
 x = random.randint(*(2, 100))
 y = random.randint(*(2, 100))
 speech.say("%d minus %d equals?" % (x, y))
 ans = x - y
 time.sleep(weight1 * Base)
 speech.say("%d" % ans)
 return ans

def mul():
 x = random.randint(*(2, 50))
 y = random.randint(*(2, 10))
 xy = [x, y]
 random.shuffle(xy)
 x, y = xy
 speech.say("%d times %d equals?" % (x, y))
 ans = x * y
 time.sleep(Base * weight)
 speech.say("%d" % ans)
 return ans

def div():
 x = random.randint(*(3, 100))
 y = random.randint(*(2, 10))
 speech.say("%d devided by %d equals?" % (x, y))
 ans = (x / y, x % y)
 time.sleep(Base * weight)
 speech.say("%d and the remainder is %d" % (ans[0], ans[1]))
 return ans

method_list = [
 add,
 sub,
 mul,
 div,
]

import time
import sys

# セット数
set_count = 10
# interval = 5
# 問題数
try_times = 10

def main():
 for s in range(set_count):
  for i in range(try_times):
   method = random.choice(method_list)
   method()
   p = 0.05
   n = 10
   n_p = 4
   comp_p = (1 - n_p*p) / (n - n_p)
   interval = np.random.choice(
    np.arange(5, 5+n),
    p=[p]*n_p + [comp_p]*(n - n_p)
   )
   time.sleep(interval)
  
   
if __name__ == '__main__':
 v = ui.load_view()
 v['button1'].action(v['button1'])
 v.present('sheet')
 main()
