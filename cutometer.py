
#!/usr/bin/python

import sys
import random

from PySide6 import QtCore, QtWidgets, QtGui

import sensor
import streamview


class Signaller(QtCore.QObject):
    sensor_signal = QtCore.Signal(float, float, float)


class MyWidget(QtWidgets.QWidget):
    def __init__(self, mac_addr):
        super().__init__()

        self.my_signaller = Signaller()
        self.my_sensor = sensor.Sensor(mac_addr, self.my_signaller)
        self.my_sensor.connect()
        self.my_signaller.sensor_signal.connect(self.sensor_update)

        self.my_speed = streamview.StreamView()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.my_speed)
        self.layout.addWidget(self.text)


    @QtCore.Slot()
    def sensor_update(self, y, p, r):
        self.text.setText(str(round(y,4)))
        s = self.my_speed
        s.my_data.append(y)
        s.update()
        if len(s.my_data) >= 2000:
            s.my_data = s.my_data[-2000:]
        #print(y,p,r)

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
