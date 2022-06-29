import time
from T265 import T265
from navigation import Navigation
from plotter import plot_coordinates

def main7():
    TrackingCam = T265()   
    TrackingCam.start_stream()    
    time.sleep(2)   
    plot_coordinates(TrackingCam)