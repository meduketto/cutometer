from PySide6 import QtCore, QtGui, QtWidgets


class StreamView(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding
        )

        self.my_data = [1,1,1,2,2,2,2,3,3,3,3]

    def sizeHint(self):
        return QtCore.QSize(120,40)

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
        if datalen >= w:
            data = self.my_data[-w:]
        else:
            data = ([0]*(w-datalen)) + self.my_data[:]
        maxv = max(data)
        f = maxv / (h/2)
        data = [-v/f for v in data]
        for i, v in enumerate(data):
            rect = QtCore.QRect(i, h/2, 1, v)
            painter.fillRect(rect, brush)
