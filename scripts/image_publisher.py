#!/usr/bin/env python
# coding:utf-8
import rospy
from thomas_ros.srv import *
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

import params

"""
カメラの情報を読み取って[/image]トピックに配信するノード
カメラIDを変更する場合はparams.pyのcamera_idを変更する
"""

class ThomasVision:
    def __init__(self):
        self.steam_vision = rospy.ServiceProxy("vision", object_detection)
        self.image_pub = rospy.Publisher(params.image_topic, Image)
        self.cap = cv2.VideoCapture(params.camera_id)
        self.bridge = CvBridge()



    def read_image(self):
        ret, frame = self.cap.read()
        imgmsg = self.bridge.cv2_to_imgmsg(frame, "bgr8")
        try:
            self.image_pub.publish(imgmsg)
        except CvBridgeError as e:
            rospy.logerr(e)
        

def main():
    rospy.init_node("thomas_vision_node", anonymous=True)
    thomas = ThomasVision()
    while(True):
        thomas.read_image()

if __name__ == "__main__":
    main()