# coding:utf-8
import rospy
from thomas_ros.srv import *

class ThomasVision:
    def __init__(self):
        self.steam_vision = rospy.ServiceProxy("vision", object_detection)
        self.your_function(arg1)
    def your_function(self, arg1):
        vision_srv = object_detectionRequest()
        vision_srv.num_of_object = 1
        steam_vision(vision_srv)

def main():
    rospy.init_node("thomas_vision_node", anonymous=True)
    thomas = ThomasVision()

if __name__ == "__main__":
    main()