import time
from T265 import T265
from navigation import Navigation
from plotter import plot_coordinates, plot_YPR


def main():   
    TrackingCam = T265()   
    TrackingCam.start_stream()    
    time.sleep(2)        
    # Nav = Navigation(None, None)    
    # Nav.add_camera(TrackingCam)    
    # Nav.travel_rotation()


def main7():
    TrackingCam = T265()   
    TrackingCam.start_stream()    
    time.sleep(2)   
    #plot_coordinates(TrackingCam)
    plot_YPR(TrackingCam)

if __name__ == "__main__":
    main7() 