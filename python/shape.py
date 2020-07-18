#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtGui import QColor, QFont, QPen, QBrush


class Shape(object):
    # 类型
    type = 0

    # 数据
    data = [
        [[1, 1, 0, 0],
         [1, 0, 0, 0],
         [1, 0, 0, 0],
         [0, 0, 0, 0]],
        [[0, 1, 1, 1],
         [0, 0, 0, 1],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        [[0, 0, 0, 0],
         [0, 0, 0, 1],
         [0, 0, 0, 1],
         [0, 0, 1, 1]],
        [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [1, 0, 0, 0],
         [1, 1, 1, 0]],
    ]

    # 颜色
    color = 0x000000

    size = 30

    offsetX = 30

    offsetY = 30

    pointX = 0

    pointY = 0

    border = None

    def __init__(self, color, data, size, offset):
        self.color = color
        self.data = data
        self.size = size
        self.offsetX = offset
        self.offsetY = offset
        self.type = 0
        self.pointX = 0
        self.pointY = 0

    def changeType(self):
        self.type = (self.type + 1) % len(self.data)

    def changeX(self, i):
        self.pointX += i

    def changeY(self, i):
        self.pointY += i

    def draw(self, painter):
        # 列 y
        for y in range(0, len(self.data[self.type])):
            # 行 x
            for x in range(0, len(self.data[self.type][y])):
                if(self.data[self.type][y][x] == 1):
                    qcolor = QColor(self.color)
                    self.drawBlock(painter, x, y, qcolor)
        self.drawLine(painter)


    def drawBlock(self, painter, x, y, qcolor):
        w = self.size
        h = self.size

        x = self.size * (x + self.pointX) + self.offsetX
        y = self.size * (y + self.pointY) + self.offsetY

        painter.fillRect(x + 1, y + 1, w - 2, h - 2, qcolor)

        painter.setPen(qcolor.lighter())
        painter.drawLine(x, y + h - 1, x, y)
        painter.drawLine(x, y, x + w - 1, y)

        painter.setPen(qcolor.darker())
        painter.drawLine(x + 1, y + h - 1, x + w - 1, y + h - 1)
        painter.drawLine(x + w - 1, y + h - 1, x + w - 1, y + 1)

    # 四个点的坐标
    def drawLine(self, painter):
        if self.border == None :
            return
        w = self.size * 4
        h = self.size * 4
        x = self.offsetX + self.size * self.pointX
        y = self.offsetY + self.size * self.pointY
        color = QColor(self.border)
        painter.setPen(color.lighter())
        painter.drawLine(x, y, x + w, y)
        painter.drawLine(x, y + h, x, y)
        painter.drawLine(x, y + h, x + w, y + h)
        painter.drawLine(x + w, y + h, x + w, y)