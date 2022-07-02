import sys
import time
from threading import Event
from math import asin,fabs,atan2

from mbientlab.metawear import MetaWear, libmetawear, parse_value
from mbientlab.metawear.cbindings import *

from pyquaternion import Quaternion



def euler(q):
    uq = q.normalised
    s = uq.transformation_matrix
    g = s[0, 2]
    a = s[0, 0]
    f = s[0, 1]
    n = s[2, 1]
    k = s[1, 1]
    e = s[2, 2]
    pitch = asin(g)
    if .99999 > fabs(g):
        roll = atan2(-1, e)
        yaw = atan2(-f, a)
    else:
        roll = atan2(n, k)
        yaw = 0
    return yaw, pitch, roll


class State:
    def __init__(self, device, signaller):
        self.device = device
        self.callback = FnVoid_VoidP_DataP(self.data_handler)
        self.signaller = signaller

    def data_handler(self, ctx, data):
        d = parse_value(data)
        q1 = Quaternion(d.w, d.x, d.y, d.z)
        y,p,r = euler(q1)
        self.signaller.sensor_signal.emit(y,p,r)
        #print(y,p,r)
        #print("%s\t%s\t%s\t%s\n" % (str(d.w), str(d.x), str(d.y), str(d.z)))


class Sensor:
    def __init__(self, mac_addr, signaller):
        self.dev = MetaWear(mac_addr)
        self.s = State(self.dev, signaller)


    def connect(self):
        self.dev.connect()

        libmetawear.mbl_mw_settings_set_connection_parameters(self.s.device.board, 7.5, 7.5, 0, 6000)
        time.sleep(1.5)

        libmetawear.mbl_mw_sensor_fusion_set_mode(self.s.device.board, SensorFusionMode.NDOF);
        libmetawear.mbl_mw_sensor_fusion_set_acc_range(self.s.device.board, SensorFusionAccRange._8G)
        libmetawear.mbl_mw_sensor_fusion_set_gyro_range(self.s.device.board, SensorFusionGyroRange._2000DPS)
        libmetawear.mbl_mw_sensor_fusion_write_config(self.s.device.board)

        signal = libmetawear.mbl_mw_sensor_fusion_get_data_signal(self.s.device.board, SensorFusionData.QUATERNION);
        libmetawear.mbl_mw_datasignal_subscribe(signal, None, self.s.callback)

        libmetawear.mbl_mw_sensor_fusion_enable_data(self.s.device.board, SensorFusionData.QUATERNION);
        libmetawear.mbl_mw_sensor_fusion_start(self.s.device.board);

    def disconnect(self):
        libmetawear.mbl_mw_sensor_fusion_stop(self.s.device.board);

        signal = libmetawear.mbl_mw_sensor_fusion_get_data_signal(self.s.device.board, SensorFusionData.QUATERNION);
        libmetawear.mbl_mw_datasignal_unsubscribe(signal)
        libmetawear.mbl_mw_debug_disconnect(self.s.device.board)
