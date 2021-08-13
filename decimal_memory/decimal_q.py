import random
import os
from decimal import Decimal, ROUND_HALF_UP
import shutil
from operator import add, sub, mul
from datetime import datetime

import numpy as np
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
 
def make_question():
    registerFont(TTFont('GenShinGothic',
                        'GenShinGothic-Light.ttf'))
    
    directory = datetime.today().strftime('%Y-%m-%d')
    os.makedirs(directory, exist_ok=True)
    file = os.path.join(directory, 'question.pdf') # 出力ファイル名を設定
    
    paper = canvas.Canvas(file)             # 白紙のキャンバスを用意
    paper.saveState()                       # 初期化
    paper.setFont('GenShinGothic', 24)      # フォントを設定
    
    # 横wと縦hの用紙サイズを設定
    w = 210 * mm
    h = 297 * mm
    
    paper.setPageSize((w, h))  # 用紙のサイズをセット
    paper.setFont('GenShinGothic', 12) # フォントを設定

    # 問題作成
    nonce = np.random.randint(101)

    q_array = np.random.rand(25, 8) + 0.01
    q_array = q_array.tolist()

    div = lambda a, b : a / b
    op_list = [add, sub, mul, div]
    labels = ['+', '-', 'x', '÷']
    questions = []
    answers = np.zeros((25, 4))

    # 描画
    w_block = 4
    h_block = 25
    h_chunk = h // h_block
    w_chunk = (w - 10 * mm) // w_block
    np.random.seed(nonce)
    for i in range(h_block):
        for j in range(w_block):
            y = i * h_chunk + 11 * mm
            x = j * w_chunk  + 10 * mm

            q1 = q_array[i][2*j]
            q2 = q_array[i][2*j + 1]

            op_i = np.random.randint(0, 4)
            op = op_list[op_i]

            op_label = labels[op_i]
            round_num = 2 if op_i in [2, 3] else 3
            
            q1 = round(q1, round_num)
            q2 = round(q2, round_num)
            result = op(q1, q2)
            digit = Decimal('0.1')**round_num
            
            answers[i, j] = Decimal(str(result)).quantize(digit, rounding=ROUND_HALF_UP)
            paper.drawString(x, h - y, f'({w_block * i + j + 1}) {q1} {op_label} {q2} = ?')

    paper.showPage() 
    paper.showPage() 
    paper.setFont('GenShinGothic', 12)

    np.random.seed(nonce)
    for i in range(h_block):
        for j in range(w_block):
            y = i * h_chunk + 11 * mm
            x = j * w_chunk  + 10 * mm

            q1 = q_array[i][2*j]
            q2 = q_array[i][2*j + 1]
            op_i = np.random.randint(0, 4)
            op = op_list[op_i]
            op_label = labels[op_i]
            if op_i in [2, 3]:
                q1 = round(q1, 2)
                q2 = round(q2, 2)
            else:
                q1 = round(q1, 3)
                q2 = round(q2, 3)
            answer = answers[i, j]
            paper.drawString(x, h - y, f'({w_block * i + j + 1}) {q1} {op_label} {q2} = {answer}')

    paper.save()

if __name__ == '__main__':
    make_question()