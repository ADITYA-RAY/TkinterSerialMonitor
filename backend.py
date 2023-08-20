import serial 
import time
import numpy as np
import matplotlib.pyplot as plt
import threading
import numpy



class backend():
    def __init__(self,port,baudrate):
        self.mcu = serial.Serial(port=port,baudrate=baudrate,timeout=0.1)
        self.data = ""
        self.x_axis = 0
        plt.ion()
        self.fig = plt.figure()
        self.numx = [[0]*2]*2
        self.numy = [[0]*2]*2
        self.colors=["r-","b-"]
  
    def connect(self):
        self.mcu.write(bytes("1",'utf-8'))
        time.sleep(0.05)

    def getData(self):
        self.data = self.mcu.readline()
        if self.data != bytes("",'utf-8'):
            self.x_axis += 1 
            decoded = ((self.data).decode()).split()
            return decoded
        return 
            
    def plot(self):
        while True:
            graphs = self.getData()
            if graphs:
                for i in range(len(graphs)):
                    self.numx[i] = [self.numx[i][1],self.x_axis]
                    self.numy[i] = [self.numy[i][1],int(graphs[i])]
                    plt.plot(self.numx[i],self.numy[i],self.colors[i])
                    self.fig.canvas.draw()     
                    self.fig.canvas.flush_events()             

if __name__ == "__main__":
    process = backend('/dev/ttyACM0','115200')
    process.connect()
    process.plot()

