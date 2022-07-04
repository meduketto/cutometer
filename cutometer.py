
#!/usr/bin/python

import random
import sys
import time

from PySide6 import QtCore, QtWidgets, QtGui

import sensor
import streamview


def get_msec():
    return time.clock_gettime_ns(time.CLOCK_MONOTONIC) * 1000000


class Signaller(QtCore.QObject):
    sensor_signal = QtCore.Signal(float, float, float)


class MyWidget(QtWidgets.QWidget):
    def __init__(self, mac_addr):
        super().__init__()

        self.my_signaller = Signaller()
        self.my_sensor = sensor.Sensor(mac_addr, self.my_signaller)
        self.my_sensor.connect()
        self.my_signaller.sensor_signal.connect(self.sensor_update)

        self.grid = QtWidgets.QGridLayout(self)

        self.L1 = QtWidgets.QLabel("Cut speed", alignment=QtCore.Qt.AlignRight)
        self.grid.addWidget(self.L1, 0, 0)
        self.my_speed = streamview.StreamView()
        self.grid.addWidget(self.my_speed, 0, 1)

        self.last_t = get_msec()
        self.last_v = 0

        self.L2 = QtWidgets.QLabel("Edge", alignment=QtCore.Qt.AlignRight)
        self.grid.addWidget(self.L2, 1, 0)
        self.my_edge = streamview.StreamView()
        self.grid.addWidget(self.my_edge, 1, 1)

        self.last_edge = 0

    @QtCore.Slot()
    def sensor_update(self, y, p, r):
        t = get_msec()
        speed = (y-self.last_v) / (t - self.last_t)
        self.my_speed.addData(speed)
        self.last_t = t
        self.last_v = y
        self.my_edge.addData(p - self.last_edge)
        self.last_edge = p
        print(y,p,r)

    def closeEvent(self, event):
        self.my_sensor.disconnect()


def main(args):
    mac_addr = args[0]
    args = args[1:]
    app = QtWidgets.QApplication(args)

    widget = MyWidget(mac_addr)
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main(sys.argv[1:])
