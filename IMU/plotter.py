import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import math

def plot_coordinates(Cam, plotting='POSITION', run_time=60, speed =0.2):
    """
    Allows the plotting of coordinates 
​
    :param plotting: Stream image width - for images streams. 
    :type plotting: String
    :param run_time: How long the plot will last for (in seconds)
    :type run_time: int
    :param speed: How long the tracking camera sleeps for before each reading
    :type speed: int
    """
    fig = plt.figure(figsize=(10,10))
    #ax = fig.add_subplot(111, projection='3d') Removed for xy plane only
    ax = fig.add_subplot(111) #added for xy plane only
    #plt.axis([-10, 10, -10, 10])

    time.sleep(2)
    x = []
    y = []
    z = []
    counter = math.ceil(run_time/speed)
    while(counter>0):
        position = Cam.receive_data([plotting], turn_off=False)[0][0]
        time.sleep(speed)
        col = 'black'
        x.append(position[0])
        y.append(-position[2])
        z.append(position[1])
        if(len(z) > 2 and z[-1]<z[-2]):
            col = 'red' 
        # ax.plot(x,y,z, c=col) # plot the point (2,3,4) on the figure
        ax.plot(x,y, c=col) #removed z for xy plane only


        plt.pause(0.05)
        counter -= 1
    plt.show()
        

def plot_YPR(Cam, run_time=60, speed =0.2):
    """
    Allows the plotting of coordinates and orientation 

    :param run_time: How long the plot will last for (in seconds)
    :type run_time: int
    :param speed: How long the tracking camera sleeps for before each reading
    :type speed: int
    """
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    import numpy as np
    from itertools import product, combinations
    fig = plt.figure()
    #ax = fig.gca(projection='3d') #removed for 2d check
    ax = fig.gca() #added for 2D check
    #ax.invert_yaxis()
    #ax.invert_xaxis()

    counter = math.ceil(run_time/speed)
    x = []
    y= []
    z = []
    while(counter>0):
        position = Cam.receive_data(["POSITION"], turn_off=False)[0][0]
        x.append(position[0])
        y.append(-position[2])
        z.append(position[1])
        u, v, w = Cam.pose_to_ypr()
        #ax.plot(x,y,z, color='black') #removed for 2D check
        #ax.plot(x,y, color='black') #added for 2D check
        #S =ax.quiver(x[-1], y[-1], z[-1], math.radians(u), math.radians(v), math.radians(w), length=0.05, color='red') #removed for 2D check
        #S =ax.quiver(0, 0, 0, math.radians(u), math.radians(v), math.radians(w), color='red')
        S =ax.quiver(0, 0, math.radians(u), math.radians(v),  color='red') #added for 2D check
        print(("yaw = %s , pitch = %s, roll = %s")%(u,v,w))
        plt.pause(0.05)
        counter -=1
        time.sleep(speed)
        S.remove()
        
    plt.show()