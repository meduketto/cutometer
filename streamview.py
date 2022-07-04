from PySide6 import QtCore, QtGui, QtWidgets


class StreamView(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding
        )

        self.my_data = []
        self.maxv = 0

    def sizeHint(self):
        return QtCore.QSize(200,40)

    def addData(self, v):
        self.my_data.append(v)
        self.update()
        if len(self.my_data) >= 2000:
            self.my_data = self.my_data[-2000:]

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor('black'))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        w = painter.device().width()
        h = painter.device().height()
        rect = QtCore.QRect(0, 0, w, h)
        painter.fillRect(rect, brush)

        brush.setColor(QtGui.QColor('yellow'))

        datalen = len(self.my_data)
        if datalen == 0:
            return
        if datalen >= w:
            data = self.my_data[-w:]
        else:
            data = ([0]*(w-datalen)) + self.my_data[:]
        self.maxv = max(max(data), self.maxv)
        f = self.maxv / (h/2)
        if f == 0:
            return
        data = [-v/f for v in data]
        for i, v in enumerate(data):
            rect = QtCore.QRect(i, h/2, 1, v)
            painter.fillRect(rect, brush)
