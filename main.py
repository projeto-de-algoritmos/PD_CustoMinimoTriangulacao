# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore
import numpy as np
from math import sqrt
from minimumCostOfConvexPolygonTriangulation import calculateMinimum


class ImageScroller(QtWidgets.QWidget):
    def __init__(self):
        self.chosen_lines = [[]]
        self.lines = 0
        self.points = []
        self.pos = None
        QtWidgets.QWidget.__init__(self)
        self.setMouseTracking(True)

    def paintEvent(self, paint_event):
        painter = QtGui.QPainter(self)

        # pen = QtGui.QPen()
        # pen.setWidth(10)
        painter.setPen(QtGui.QPen())
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setBrush(QtGui.QBrush(QtCore.Qt.black, QtCore.Qt.SolidPattern))

        for line in self.chosen_lines:
            if len(line) == 2:
                painter.drawLine(line[0][0], line[0][1], line[1][0], line[1][1])

        if len(self.chosen_lines[self.lines]) == 1:
            painter.drawLine(
                self.pos.x(),
                self.pos.y(),
                self.chosen_lines[self.lines][0][0],
                self.chosen_lines[self.lines][0][1],
            )
        print(self.points)
        min, p1, p2, p3 = calculateMinimum().mTCDP(self.points, len(self.points))

        if min != 0:
            painter.drawLine(p1[0], p1[1], p2[0], p2[1])
            painter.drawLine(p1[0], p1[1], p3[0], p3[1])
            painter.drawLine(p2[0], p2[1], p3[0], p3[1])
        # painter.setBrush(QtGui.QColor(255, 0, 0, 127))

    def mouseMoveEvent(self, event):
        self.pos = event.pos()
        self.update()

    def mouseReleaseEvent(self, cursor_event):
        pointToAdd = self.chooseFinalPoint(cursor_event.pos())
        if pointToAdd == 0:
            pointToAdd = [cursor_event.pos().x(), cursor_event.pos().y()]
            self.points.append([pointToAdd[0], pointToAdd[1]])

        # print(self.chosen_lines)
        if len(self.chosen_lines[self.lines]) == 0:
            self.chosen_lines[self.lines].append(pointToAdd)
        elif len(self.chosen_lines[self.lines]) == 1:
            print()
            self.chosen_lines[self.lines].append(pointToAdd)
            self.chosen_lines.append([])
            self.lines += 1
        self.update()

    def calculateDist(self, pointA, pointB):
        dist = sqrt((pointB[0] - pointA[0]) ** 2 + (pointB[1] - pointA[1]) ** 2)
        return dist

    def chooseFinalPoint(self, pos):
        if len(self.points) > 0:
            point = [pos.x(), pos.y()]
            points = np.asarray(self.points)
            dist_2 = np.sum((points - point) ** 2, axis=1)

            dist = self.calculateDist(point, self.points[np.argmin(dist_2)])

            if dist < 5:
                return self.points[np.argmin(dist_2)]
            else:
                return 0
        return 0


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = ImageScroller()
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec_())
