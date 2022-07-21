import serial
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

fig = plt.figure()

#Serial takes two parameters: serial device and baudrate
ser = serial.Serial('COM6', 9600)
x = 24
y = 32 
valLength = 6

randomArray = np.random.rand(x,y)*100

def animate(i):
    data = ser.readline()
    delimitedData = data.split(b',')
    randomArray = (np.reshape(delimitedData[:-1],(x,y))).astype(float)
    plt.imshow(randomArray, cmap='viridis', interpolation='none')


ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()