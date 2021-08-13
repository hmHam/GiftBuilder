import sys
import os
import sqlite3
from subprocess import call
from datetime import datetime

import japanize_matplotlib

from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QSizePolicy, QVBoxLayout, QHBoxLayout,
    QGroupBox, QLineEdit, QFormLayout
)
from PyQt5.QtGui import QIcon
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from decimal_q import make_question
from table import fetchall, record_result

con = sqlite3.connect('history.db')
cur = con.cursor()

class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig, self.axes = plt.subplots(2, 2, figsize=(16, 16))
        self.fig.suptitle('今日までの記録')
        self.axes[0][0].set_title('タイム/週')
        self.axes[0][1].set_title('スコア/週')
        self.axes[1][0].set_title('タイム/日')
        self.axes[1][1].set_title('スコア/日')

        self.history_view()

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(
            self,
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )
        FigureCanvas.updateGeometry(self)

    def history_view(self):
        '''今日までの記録の推移を可視化する
        '''
        # TODO: dbから結果を取ってきて可視化する。
        pass

    def change_view(self, minute, second, score):
        date = datetime.now().strftime('%Y/%m/%d')
        # TODO: minute, second, scoreの内容をdbに保存
        record_result(cur, now, minute, second, score)
        today_idx = 100  # FIXME: 仮
        # TODO: 元のグラフにscatterで点を追加, 横軸はインデックス, 縦軸は秒
        # TODO: TEXTで(分, 秒)を表示
        self.axes[0][0].scatter(today_idx, 60 * minute + second)
        # TODO: TEXTで(スコア)を表示
        self.axes[0][1].scatter(today_idx, score)
        print('change view!')
        pass


class DecimalWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(1000, 1200)
        self.setWindowTitle('sample')

        # TODO: 
        #  (1) 現在までの記録のグラフ
        #  (2) 過去の最高得点
        # の表示

        # buttonの設定
        self.go_button = QPushButton('問題を作成')

        # buttonのclickでラベルをクリア
        self.go_button.clicked.connect(self._wrap_make_question)

        # レイアウト配置
        self.body = QVBoxLayout()
        self.canvas = MyMplCanvas(self)
        self.body.addWidget(self.canvas)

        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.go_button)
        hbox.addStretch()
        self.body.addLayout(hbox)

        self.setLayout(self.body)
        # 表示
        self.show()

    def _wrap_make_question(self):
        make_question()
        # フォルダを開く
        if call(['open', os.path.dirname(os.path.abspath(__file__))]) == 1:
            print('error occurr')
        self.go_button.hide()
        self.create_form()
    
    def create_form(self):
        # TODO: 今日のタイムとスコアを記録する。Formの作成
        self.formLayout = QFormLayout()
        self.timeLineEdit = QLineEdit()
        self.formLayout.addRow(QLabel('タイム'), self.timeLineEdit)
        self.scoreLineEdit = QLineEdit()
        self.formLayout.addRow(QLabel('スコア'), self.scoreLineEdit)
        self.body.addLayout(self.formLayout)

        self.done_button = QPushButton('完了')
        self.done_button.clicked.connect(self._change_view)
        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.done_button)
        hbox.addStretch()
        self.body.addLayout(hbox)

    def _change_view(self):
        dt = datetime.strptime(self.timeLineEdit.text(), '%M,%S')
        score = int(self.scoreLineEdit.text())
        self.canvas.change_view(dt.minute, dt.second, score)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    path = 'icon.png'
    app.setWindowIcon(QIcon(path))
    ew = DecimalWidget()    
    sys.exit(app.exec_())
    cur.close()