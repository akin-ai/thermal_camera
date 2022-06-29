import pyrealsense2 as rs
import math
import numpy as np
class T265:
    """
    This is a class which controls the Intel Realsense Tracking Camera T265
    """
    def __init__(self):
        self.pipeline = 0
        self.config = 0
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.pose)
        self.pose = None
        self.data = None 
    def start_stream(self):
        """
        Starts the stream of the tracking camera. 
        """
        self.pipeline.start(self.config)
    def stop_stream(self):
        """
        Stops the stream of the tracking camera. 
        """
        self.pipeline.stop()
    def receive_stereo(self):
        """
        Receives the stereo images from the camera 
        :return: two stereo images
        :rtype: np array, np array      
        """
        pass
    def receive_data(self, datatypes, turn_off=False):
        """
        Receives the specified data
        :param datatypes: List of datatypes wanted 
        :type datatypes: List of Strings
        :param turn_off: Whether or not the camera turns off at receiving data
        :type turn_off: boolean
        :return: list of datatypes specified
        :rtype: list
        """
        data_returned = []
        try:
            while(1):
                frames = self.pipeline.wait_for_frames()
                self.pose = frames.get_pose_frame()
                if self.pose:
                    self.data = self.pose.get_pose_data()
                    # Receive the specific 
                    for i in datatypes:
                        if(i == "VELOCITY"):
                            velocity = self.receive_velocity()
                            data_returned.append([velocity])
                        elif(i == "ACCELERATION"):
                            acceleration = self.receive_acceleration()
                            data_returned.append([acceleration])
                        elif(i == "POSITION"):
                            position = self.receive_position()
                            print(position)
                            data_returned.append([position])
                        elif(i == "STEREO"):
                            stereo = self.receive_stereo
                            data_returned.append([stereo])
                    return data_returned
        except:
            print("error")
            return None
            
        finally:
            if(turn_off == True):
                self.stop_stream()
            if(data_returned is []):
                return None
            else:
                return data_returned
        
    def pose_to_ypr(self):
        """
        | Converts pose to yaw, pitch and role.
        | Use receive_data before this function to update the pose
        """
        try:
            frames = self.pipeline.wait_for_frames()
            self.pose = frames.get_pose_frame()
            if self.pose:
                self.data = self.pose.get_pose_data()
            
     
                # w = self.data.rotation.w
                # x = -self.data.rotation.z
                # y = self.data.rotation.x
                # z = -self.data.rotation.y
                # pitch =  -math.asin(2.0 * (x*z - w*y)) * 180.0 / math.pi
                # roll  =  math.atan2(2.0 * (w*x + y*z), w*w - x*x - y*y + z*z) * 180.0 / math.pi
                # yaw   =  math.atan2(2.0 * (w*z + x*y), w*w + x*x - y*y - z*z) * 180.0 / math.pi #Previous 

                w = self.data.rotation.w
                x = self.data.rotation.x
                z = self.data.rotation.y
                y = self.data.rotation.z

                if z > 0.5 or z < -0.5:
                    yaw =  -math.asin(2.0 * (z*w - y*x)) * 180.0 / math.pi
                else :
                    yaw = 180 + math.asin(2.0 * (z*w - y*x)) * 180.0 / math.pi 
                pitch  =  -math.atan2(2.0 * (w*x + y*z), w*w - x*x - y*y + z*z) * 180.0 / math.pi
                roll  =  math.atan2(2.0 * (w*z + x*y), w*w + x*x - y*y - z*z) * 180.0 / math.pi
                if yaw < 0: yaw += 360.0
                if pitch < 0: pitch += 360.0
                if roll < 0: roll += 360.0

        except:
            return None
        return yaw, pitch, roll      
    def receive_position(self):
        """
        Returns the position of the device
        :return: position of device in x, y, z 
        :rtype: int, int, int
        """
        position = self.data.translation.x, self.data.translation.y, self.data.translation.z
        return position
    
    def receive_velocity(self):
        """
        Returns the velocity of the device
        :return: velocity of device in x, y, z 
        :rtype: int, int, int
        """
        velocity = self.data.velocity.x, self.data.velocity.y, self.data.velocity.z
        return velocity
    def receive_acceleration(self):
        """
        Returns the acceleration of the device
        
        :return: acceleration of device in x, y, z 
        :rtype: int, int, int
        """
        acceleration = self.data.acceleration.x, self.data.acceleration.y, self.data.acceleration.z 
        return acceleration