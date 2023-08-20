import serial 
import time
class backend():
    def __init__(self):
        self.mcu = ""
        self.data = ""
        self.x_axis = 0
        
    def connect(self,port,baudrate):
        self.mcu = serial.Serial(port=port,baudrate=baudrate,timeout=0.1)
        self.mcu.write(bytes("1",'utf-8'))
        time.sleep(0.05)

    def getData(self):
        self.data = self.mcu.readline()
        if self.data != bytes("",'utf-8'):
            self.x_axis += 1 
            decoded = ((self.data).decode()).split()
            return decoded
        return 

