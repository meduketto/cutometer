
#!/usr/bin/python

import sys
import random

from PySide6 import QtCore, QtWidgets, QtGui

import sensor


class Signaller(QtCore.QObject):
    sensor_signal = QtCore.Signal(float, float, float)


class MyWidget(QtWidgets.QWidget):
    def __init__(self, mac_addr):
        super().__init__()

        self.my_signaller = Signaller()
        self.my_sensor = sensor.Sensor(mac_addr, self.my_signaller)
        self.my_sensor.connect()
        self.my_signaller.sensor_signal.connect(self.sensor_update)

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def sensor_update(self, y, p, r):
        self.text.setText(str(round(y,4)))
        #print(y,p,r)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))
        self.my_sensor.disconnect()
        sys.exit(0)


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
