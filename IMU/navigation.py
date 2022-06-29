import threading
import asyncio


class Navigation():
    def __init__(self, SerQueue, Mode):
        self.SerQueue = SerQueue
        self.Mode = Mode
        self.TrackingCam = None 
        self.thread = True
        self.rotation_lock = False
        
        # Manager controls 
        self.manager_direction = "S"
        self.call_flag = 0
        self.asynch_check_flag = False 
        self.last_manager_command = None 
        self.navigation_mode = ""
    
    def start_navigation(self):
        self.navigation_mode = 'M'
    
    
    def add_camera(self, Cam):
        self.TrackingCam = Cam
    
    
    def send_response(self, response):
        print(response)
        # self.SerQueue.put(response) 
    
    
    def receive_position(self):
        position = (self.TrackingCam.receive_data(["POSITION"]))[0][0]
        x = position[0]
        y = position[1]
        z = position[2]
        return x, y, z 
    
    
    def receive_ypr(self):
        # (self.TrackingCam.receive_data(["POSITION"]))[0][0]
        y, p, r = self.TrackingCam.pose_to_ypr()
        return y, p, r
      
    
    def create_connection(self):
        self.start_navigation()
        
        
    def update_manager_direction(self, direction):
        print("Updated Direction to: "+str(direction))
        self.manager_direction = direction 
        self.call_flag += 1 
        
            
    def manager_call_flag_check(self, time =60):
        if(self.asynch_check_flag == False):
            self.asynch_check_flag = True 
            asyncio.run(self.manager_safety_call(time, self.call_flag))
        
        
    
    async def manager_safety_call(self, time, call_flag):
        await asyncio.sleep(time) 
        if(self.call_flag == call_flag):
            if(self.navigation_mode == 'M'):
                self.stop_navigation()
                print("STOPPED NAVIGATION USING HARD STOP")
        else:
            self.asynch_check_flag = False 
        
        
    def manager_controlled_move(self, type=None, update_time=1):
        self.start_navigation()
        self.manager_direction = "P" 
        # self.send_response("NAV-ON")
        self.timer_call(self.__manager_controlled_move__, update_time, 0)
        self.manager_call_flag_check(time=120)
    
    
    
    def __manager_controlled_move__(self, arg_ = 0):
        self.manager_call_flag_check() 
        type = self.manager_direction
        # print(type)
        if(type == 'L'):
            self.send_response("NAV-L")
        elif(type == 'R'):
            self.send_response("NAV-R")
        elif(type == 'U'):
            self.send_response("NAV-F")
        elif(type == 'D'):
            self.send_response("NAV-B") 
        elif(type == 'S'):
            self.send_response("NAV-STOP") 
        elif(type == 'N'):
            if(self.last_manager_command != 'N'):
                self.send_response("NAV-ON")     
        elif(type == 'P'):
            pass 
        else:
            self.stop_navigation() 
        
        self.last_manager_command = type 
    
      
    def __travel_any_distance__(self, distance=1.0):
        try:
            x, y, z = self.receive_position()
        except:
            print("TRACKING CAMERA NOT READING")
            self.stop_navigation()
        if(x > distance or y > distance or z >distance or x < -distance or y < -distance or z < -distance):
            print("ROBOT NAVIGATION COMPLETED")
            self.stop_navigation() 
        else:
            self.send_response("NAV-F")
           
            
    def stop_navigation(self):
        self.navigation_mode = 'O'
        self.send_response("NAV-OFF")
    
    
    def timer_call(self, function, time, *args):
        if(self.navigation_mode == 'M'):
            threading.Timer(time, self.timer_call, [function, time, args[0]]).start()
            function(args[0]) 
            
            
    async def safety_timer_call(self, max_time):
        await asyncio.sleep(max_time)
        if(self.navigation_mode == 'M'):
            self.stop_navigation()
            print("STOPPED NAVIGATION USING HARD STOP")
            
            
    def travel_any_distance(self, distance=1.0, update_time=1):
        self.start_navigation() 
        self.timer_call(self.__travel_any_distance__, update_time, distance)
        asyncio.run(self.safety_timer_call(distance*10))
        
        
    def travel_rotation(self, rotation=350, update_time=1, direction="left"):
        try:
            _, r , _ = self.receive_ypr()
            print(r)
            self.r = r
            print("Target Rotation Set to %s" % (self.r))
        except:
            print("TRACKING CAMERA NOT READING")
            self.stop_navigation()
            
        if(rotation > 270):
            self.rotation_lock = True
            
        self.start_navigation() 
        self.timer_call(self.__travel_rotation__, update_time, rotation, direction)
        asyncio.run(self.safety_timer_call(500))
        
        
    def __travel_rotation__(self, rotation=350, update_time = 0, direction="left"):
        try:
            # FIX THIS LATER, JUST FOR TESTING RN
            y, p, r = self.receive_ypr()
        except:
            print("TRACKING CAMERA NOT READING")
            self.stop_navigation()
        
        # Set the target to be in the minuses 
        target = self.find_new_target(self.r, rotation)
        target_lock = self.find_new_target(self.r, (rotation+180))
        
            
        
        #Rotation lock avoids the trigger being automatically reached for values around 360 degrees       
        if(self.rotation_lock  == True):
            if(r <=(target_lock+20) and r >= (target_lock -20) ):
                self.rotation_lock = False
                print("Turning OFF THE LOCK") 
        
        print(("R: %s, Target_lock: %s, %s, target: %s, Y:%s, P:%s, R:%s")% (r, target_lock, self.rotation_lock, target, y, p, r))
        
        if((r <= (target+10) and r >= (target-10)) and self.rotation_lock  == False):
            print("ROBOT NAVIGATION COMPLETED")
            self.stop_navigation() 
        else:
            if(direction == "left"):
                self.send_response("NAV-L") 
            else:
                self.send_response("NAV-R")
                
                
    def find_new_target(self, r, new_target):
        rot_n = r+float(new_target)
        if(rot_n  > 180):
            target = -(360-rot_n)
            if(target>180):
                target = -360+(target)
            elif(target < -180):
                    target = 380+target
        else:
            target = rot_n
        return target