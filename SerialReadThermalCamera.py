import serial
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import struct
import time


fig = plt.figure()


#Serial takes two parameters: serial device and baudrate
ser = serial.Serial('COM6', 115200)
x = 24 
y = 32 
valLength = 6

randomArray = np.random.rand(x,y)*100

def animate(i):
    data = ser.readline()
    delimitedData = data.split(b',')
    
    for i in range(x):
        for j in range(y): 
            if i*x+j<700:
                randomArray[i][j] = float(delimitedData[i*y+j]) 

    plt.imshow(randomArray, cmap='viridis', interpolation='nearest')


ani = animation.FuncAnimation(fig, animate, interval=500)
plt.show()



