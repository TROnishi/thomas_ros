#!/usr/bin/env python
#coding: utf-8
import rospy
from thomas_ros.srv import *

class ThomasCore:
    def __init__(self):
        self.steam_client = rospy.ServiceProxy("steam", steam)
        self.move_client = rospy.ServiceProxy("move", move)
        visionSS = rospy.Service("vision", object_detection, self.commander)
    
    def commander(self, req):
        if req.num_of_object == 1:
            steam_command = steamRequest()
            steam_command.command = 1
            steam_client(steam_command)
        move_command = moveRequest()
        move_command.command = 1
        self.move_client(move_command)
        return True

def main():
    rospy.init_node("thomas_core", anonymous=True)
    thomas = ThomasCore()
    rospy.spin()

if __name__ == "__main__":
    main()