from PyQt5.QtGui import QColor, QFont, QPen, QBrush


class Background(object):

    width = 15

    height = 25

    size = 30

    offset = 30

    color = 0x000000

    data = None

    colors = None

    def __init__(self, width, height, size, offset):
        self.width = width
        self.height = height
        self.size = size
        self.offset = offset
        self.data = [[0 for i in range(width)] for j in range(height)]

    def draw(self, painter):
        # 列 y
        for y in range(0, self.height):
            # 行 x
            for x in range(0, self.width):
                self.drawLine(painter, x, y)
                if self.data[y][x] > 0:
                    self.drawBlock(painter, x, y, self.data[y][x])

    def drawLine(self, painter, x, y):
        w = self.size
        h = self.size
        x = x * self.size + self.offset
        y = y * self.size + self.offset
        color = QColor(self.color)
        painter.setPen(color.lighter())
        painter.drawLine(x, y + h, x, y)
        painter.drawLine(x, y, x + w, y)
        painter.drawLine(x, y + h, x + w, y + h)
        painter.drawLine(x + w, y + h, x + w, y)

    def drawBlock(self, painter, x, y, c):
        w = self.size
        h = self.size
        x = self.size * x + self.offset
        y = self.size * y + self.offset
        color = QColor(c)
        painter.fillRect(x + 1, y + 1, w - 2, h - 2, color)

        painter.setPen(color.lighter())
        painter.drawLine(x, y + h - 1, x, y)
        painter.drawLine(x, y, x + w - 1, y)

        painter.setPen(color.darker())
        painter.drawLine(x + 1, y + h - 1, x + w - 1, y + h - 1)
        painter.drawLine(x + w - 1, y + h - 1, x + w - 1, y + 1)

    def isRotate(self, shape):
        type = (shape.type + 1) % len(shape.data)
        shapeData = shape.data[type]
        x = shape.pointX
        y = shape.pointY
        return self.isChange(shapeData, x, y)

    def isLeft(self, shape):
        shapeData = shape.data[shape.type]
        x = shape.pointX - 1
        y = shape.pointY
        return self.isChange(shapeData, x, y)

    def isRight(self, shape):
        shapeData = shape.data[shape.type]
        x = shape.pointX + 1
        y = shape.pointY
        return self.isChange(shapeData, x, y)

    def isDown(self, shape):
        shapeData = shape.data[shape.type]
        x = shape.pointX
        y = shape.pointY + 1
        return self.isChange(shapeData, x, y)

    # 是否可以copy到background
    # 左右、下移动
    def isChange(self, shapeData, x, y):
        for i in range(0, len(shapeData)):
            for j in range(0, len(shapeData[i])):
                if(shapeData[i][j] == 1):
                    if (x + j) < 0 :
                        return False
                    if (x + j) >= self.width:
                        return False
                    if (y + i) >= self.height:
                        return False
                    if(self.data[y + i][x + j] > 0):
                        return False
        return True

    # copy方块到background
    def copyShapeDate(self, shape):
        shapeData = shape.data[shape.type]
        x = shape.pointX
        y = shape.pointY
        for i in range(0, len(shapeData)):
            for j in range(0, len(shapeData[i])):
                if(shapeData[i][j] > 0):
                    self.data[y + i][x + j] = shape.color

    # score
    def scoreShape(self):
        total = 0
        for i in range(0, len(self.data)):
            count = 0
            for j in range(0, len(self.data[i])):
                if self.data[i][j] > 0 :
                    count += 1
            if count  == len(self.data[i]):
                total += 1
                for k in range(i, 1, -1):
                    self.data[k] = self.data[k - 1]
        return total
