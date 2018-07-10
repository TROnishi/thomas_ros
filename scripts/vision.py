#!/usr/bin/env python
# coding:utf-8
import rospy
from thomas_ros.srv import *
import cv2
from sensor_msgs.msg import Image

class ThomasVision:
    def __init__(self):
        self.steam_vision = rospy.ServiceProxy("vision", object_detection)
        self.your_function(arg1)
        self.image_pub = rospy.Publisher("/image", Image)
        self.cap = cv2.VideoCapture(0)



    def read_image(self):
        ret, frame = cap.read()
        imgmsg = cv2_to_imgmsg(frame, "bgr8")
        try:
            self.pub.publish(imgmsg)
        except CvBridgeError as e:
            rospy.logerr(e)
        

def main():
    rospy.init_node("thomas_vision_node", anonymous=True)
    thomas = ThomasVision()
    while(True):
        thomas.read_image()

if __name__ == "__main__":
    main()