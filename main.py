import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox
from PyQt5.QtGui import QPainter, QPen, QPixmap
from PyQt5.QtCore import Qt, QPoint


g_map = [[0] * 15 for _ in range(15)]


def init():
    global g_map
    g_map = [[0] * 15 for _ in range(15)]


def regret(row, col):
    global g_map
    g_map[row][col] = 0


class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col


class Chess:
    def __init__(self, position, color):
        self.position = position
        self.color = color

    def record(self):
        # 用来判断游戏结果
        if self.color == 2:
            g_map[self.position.row][self.position.col] = 1
        else:
            g_map[self.position.row][self.position.col] = 2

    def result(self):
        """判断游戏的结局。0为游戏进行中，1为黑棋获胜，2为白棋获胜，3为平局"""
        # 1. 判断是否横向连续五子
        for x in range(11):
            for y in range(15):
                if g_map[x][y] == 1 and g_map[x + 1][y] == 1 and g_map[x + 2][y] == 1 and \
                        g_map[x + 3][y] == 1 and g_map[x + 4][y] == 1:
                    return 1
                if g_map[x][y] == 2 and g_map[x + 1][y] == 2 and g_map[x + 2][y] == 2 and \
                        g_map[x + 3][y] == 2 and g_map[x + 4][y] == 2:
                    return 2

        # 2. 判断是否纵向连续五子
        for x in range(15):
            for y in range(11):
                if g_map[x][y] == 1 and g_map[x][y + 1] == 1 and g_map[x][y + 2] == 1 and \
                        g_map[x][y + 3] == 1 and g_map[x][y + 4] == 1:
                    return 1
                if g_map[x][y] == 2 and g_map[x][y + 1] == 2 and g_map[x][y + 2] == 2 and \
                        g_map[x][y + 3] == 2 and g_map[x][y + 4] == 2:
                    return 2

        # 3. 判断是否有左上-右下的连续五子
        for x in range(11):
            for y in range(11):
                if g_map[x][y] == 1 and g_map[x + 1][y + 1] == 1 and g_map[x + 2][y + 2] == 1 and \
                        g_map[x + 3][y + 3] == 1 and g_map[x + 4][y + 4] == 1:
                    return 1
                if g_map[x][y] == 2 and g_map[x + 1][y + 1] == 2 and g_map[x + 2][y + 2] == 2 and \
                        g_map[x + 3][y + 3] == 2 and g_map[x + 4][y + 4] == 2:
                    return 2

        # 4. 判断是否有右上-左下的连续五子
        for x in range(11):
            for y in range(11):
                if g_map[x + 4][y] == 1 and g_map[x + 3][y + 1] == 1 and g_map[x + 2][y + 2] == 1 and \
                        g_map[x + 1][y + 3] == 1 and g_map[x][y + 4] == 1:
                    return 1
                if g_map[x + 4][y] == 2 and g_map[x + 3][y + 1] == 2 and g_map[x + 2][y + 2] == 2 and \
                        g_map[x + 1][y + 3] == 2 and g_map[x][y + 4] == 2:
                    return 2

        # 5. 判断是否为平局
        for x in range(15):
            for y in range(15):
                if g_map[x][y] == 0:
                    return 0
        return 3


class Chessboard(QWidget):
    def __init__(self):
        super().__init__()
        self.board = [[None] * 15 for _ in range(15)]  # 棋子坐标
        self.current_color = Qt.black  # 当前下棋的颜色，默认为黑棋先手
        self.last_move = []  # 最后一步棋的位置
        self.history = []  # 棋局历史

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.drawPixmap(0, 0, 650, 650, QPixmap('chessboard.png'))
        # self.draw_board(painter)
        self.draw_chess_pieces(painter)

    # def draw_board(self, painter):
    #     # 绘制棋盘网格
    #     painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
    #     for i in range(15):
    #         painter.drawLine(40, (1 + i) * 40, 15 * 40, (1 + i) * 40)
    #         painter.drawLine((1 + i) * 40, 40, (1 + i) * 40, 15 * 40)

    def draw_chess_pieces(self, painter):
        # 绘制棋子
        for row in range(15):
            for col in range(15):
                chess = self.board[row][col]
                if chess is None:
                    continue
                color = chess.color
                x = 40 + col * 40
                y = 40 + row * 40
                painter.setBrush(color)
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(QPoint(x, y), 15, 15)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x = event.x()
            y = event.y()
            if (x % 40 <= 15 or x % 40 >= 25) and (y % 40 <= 15 or y % 40 >= 25):
                row = int((y + 15) // 40) - 1
                col = int((x + 15) // 40) - 1
                if self.board[row][col] is None:
                    position = Position(row, col)
                    chess = Chess(position, self.current_color)
                    self.board[row][col] = chess
                    self.history.append(chess)
                    self.last_move = (row, col)
                    chess.record()
                    i = chess.result()
                    if self.current_color == Qt.black:
                        self.current_color = Qt.white
                    else:
                        self.current_color = Qt.black
                    if i == 1:
                        QMessageBox.information(self, "游戏结束", "黑方胜")
                        self.reset()
                    elif i == 2:
                        QMessageBox.information(self, "游戏结束", "白方胜")
                        self.reset()
                    elif i == 3:
                        QMessageBox.information(self, "游戏结束", "平局")
                        self.reset()
                    self.update()

    def regret(self):
        if len(self.history) > 0:
            chess = self.history.pop()
            self.board[chess.position.row][chess.position.col] = None
            self.last_move = None
            regret(chess.position.row, chess.position.col)
            if self.current_color == Qt.black:
                self.current_color = Qt.white
            else:
                self.current_color = Qt.black
            self.update()

    def reset(self):
        self.board = [[None] * 15 for _ in range(15)]
        self.current_color = Qt.black
        self.last_move = []
        self.history = []
        self.update()
        self.current_color = Qt.black
        init()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("五子棋")
        self.resize(650, 700)

        self.chessboard = Chessboard()
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        regret_button = QPushButton("悔棋")
        regret_button.clicked.connect(self.chessboard.regret)
        reset_button = QPushButton("重置")
        reset_button.clicked.connect(self.chessboard.reset)

        hbox.addWidget(regret_button)
        hbox.addWidget(reset_button)
        hbox.addStretch()

        vbox.addLayout(hbox)
        vbox.addWidget(self.chessboard)
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
