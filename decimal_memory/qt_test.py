import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLabel
from PyQt5.QtGui import QIcon

from .decimal_q import make_question


class ExampleWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(250, 150)
        self.move(300, 300)
        self.setWindowTitle('sample')

        # buttonの設定
        self.button = QPushButton('問題を作成')
        self.label = QLabel('done!')

        # buttonのclickでラベルをクリア
        self.button.clicked.connect(make_question)

        # レイアウト配置
        self.grid = QGridLayout()
        self.grid.addWidget(self.button, 0, 0, 1, 1)
        self.grid.addWidget(self.label, 1, 0, 1, 2)
        self.setLayout(self.grid)

        # 表示
        self.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    path = 'icon.png'
    app.setWindowIcon(QIcon(path))
    ew = ExampleWidget()    
    sys.exit(app.exec_())
