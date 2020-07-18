import sys, random
import shape as vo
import background as bg
import shapeFactory as sf
from PyQt5.QtWidgets import QWidget, QLabel, QLCDNumber, QDesktopWidget, QApplication
from PyQt5.QtGui import QPainterPath, QPainter, QColor, QFont, QPen, QBrush
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal

class Main(QWidget):

    started = False
    speed = 1000
    backWidth = 10
    backHeight = 20
    blockOffset = 35
    blockSize = 30

    background = None
    currentShape = None
    nextShape = None
    factory = sf.ShapeFactory()

    score = 0

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(560, 700)
        self.center()
        self.setWindowTitle('Teris')


        nextLabel = QLabel('下一个方块：', self)
        nextLabel.setFont(QFont("Roman times", 16, QFont.Bold))
        nextLabel.move((self.backWidth + 3 ) * self.blockSize, 30)

        scoreLabel = QLabel('当前得分：', self)
        scoreLabel.setFont(QFont("Roman times", 16, QFont.Bold))
        scoreLabel.move((self.backWidth + 3 ) * self.blockSize, 230)

        self.scoreNumber = QLCDNumber(self)
        self.scoreNumber.move((self.backWidth + 3 ) * self.blockSize, 260)
        self.scoreNumber.setSegmentStyle(QLCDNumber.Flat)
        self.scoreNumber.setStyleSheet("font-size: 30px; color: red; border: 1px solid black; height: 100px; width: 100px;")

        self.timer = QBasicTimer()
        self.background = bg.Background(self.backWidth, self.backHeight, self.blockSize, self.blockOffset)
        self.productShape()
        self.startHandler()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.background.draw(qp)
        self.currentShape.draw(qp)
        self.nextShape.draw(qp)
        qp.end()

    def reDraw(self):
        self.update()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Left:
            self.leftHandler()
        elif key == Qt.Key_Right:
            self.rightHandler()
        elif key == Qt.Key_Down:
            self.downHandler()
        elif key == Qt.Key_Up:
            self.upHandler()
        elif key == Qt.Key_P:
            self.startHandler()
        elif key == Qt.Key_Space:
            self.downoverHandler()

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.downHandler()
        else:
            super(QWidget, self).timerEvent(event)

    def upHandler(self):
        if self.background.isRotate(self.currentShape): 
            self.currentShape.changeType()
            self.reDraw()

    def leftHandler(self):
        if self.background.isLeft(self.currentShape):
            self.currentShape.changeX(-1);
            self.reDraw()

    def rightHandler(self):
        if self.background.isRight(self.currentShape):
            self.currentShape.changeX(1);
            self.reDraw()

    def downHandler(self):
        if self.background.isDown(self.currentShape):
            self.currentShape.changeY(1);
            self.reDraw()
        else:
            self.scoreShape()
            self.productShape()

    def downoverHandler(self):
        while self.background.isDown(self.currentShape):
            self.currentShape.changeY(1)
        self.scoreShape()
        self.productShape()

    # 计算得分
    def scoreShape(self):
        self.background.copyShapeDate(self.currentShape)
        self.score += self.background.scoreShape();
        self.reDraw()
        self.scoreNumber.display(self.score)
        print('score = %d' % self.score)

    def productShape(self):
        if self.nextShape:
            self.currentShape = self.factory.next(self.nextShape.color, self.nextShape.data, self.blockSize, self.blockOffset)
        else:
            self.currentShape = self.factory.product(self.blockSize, self.blockOffset)
        self.nextShape = self.factory.product(self.blockSize, 0)
        self.nextShape.offsetX = (self.backWidth + 3) * self.blockSize
        self.nextShape.offsetY = 2 * self.blockSize
        self.nextShape.border = 0x000000

    def startHandler(self):
        print('pauseHandler %s' % self.started)
        if self.started:
            self.timer.stop()
            self.started = False
        else:
            self.timer.start(self.speed, self)
            self.started = True
        self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())