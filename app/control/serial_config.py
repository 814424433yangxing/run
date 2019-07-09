import serial
import time
import binascii

class Ser():
    def __init__(self):
        self.ser = serial.Serial('/com3',9600)           #串口信息
        self.ser.flush()

    def write(self,data):
        self.ser.write(data)
        self.ser.flush()

    def receive(self):
        data = ""
        if self.ser.inWaiting():
            while self.ser.inWaiting():
                data += bytes(binascii.b2a_hex(self.ser.read())).decode()
                time.sleep(0.002)
            self.ser.flushInput()
            return data
        else:
            return False