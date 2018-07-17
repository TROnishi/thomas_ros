#!/usr/bin/env python
# coding:utf-8
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

import chainer

from chainercv.datasets import voc_bbox_label_names
from chainercv.links import SSD300
from chainercv.links import SSD512
from chainercv import utils
import vis_bbox
import copy
import params
# from chainercv.visualizations import vis_bbox

import numpy as np


"""
chainercvのSSDを用いて物体検出及び認識を行う
/imageトピックから
"""
class ThomasVision:
    def __init__(self):
        self.bridge = CvBridge()
        print("モデル読み込み中...")
        self.model = SSD300(
            n_fg_class=len(voc_bbox_label_names),
            pretrained_model="voc0712")
        print("読み込み完了")

        self.imagesub = rospy.Subscriber(params.image_topic, Image, self.imageCB)
        self.image_pub = rospy.Publisher(params.result_topic, Image)
        self.stock_img = np.zeros((300,300,3), np.uint8)
        
        if params.gpu > 0:
            chainer.cuda.get_device_from_id(params.gpu).use()
            model.to_gpu()
   
    def detection_loop(self):
        self.detection(self.stock_img)
    
    def imageCB(self, data):
        try:
            img = self.bridge.imgmsg_to_cv2(data, 'bgr8')
            img = cv2.resize(img, (300,300))
            
            # cv2.imshow("test", img)
            # cv2.waitKey(1)
        except CvBridgeError as e:
            rospy.logerr(e)

        self.stock_img = img
        


    def detection(self, img):
        img_ = copy.deepcopy(img)
        img = np.asarray(img, dtype=np.float32)       
        img = img.transpose(2,0,1)
        bboxes, labels, scores = self.model.predict([img])
        bbox, label, score = bboxes[0], labels[0], scores[0]

        result = vis_bbox.vis_bbox(img_, bbox, label, score, label_names=voc_bbox_label_names)

        imgmsg = self.bridge.cv2_to_imgmsg(result, "bgr8")
        try:
            self.image_pub.publish(imgmsg)
        except CvBridgeError as e:
            rospy.logerr(e)

        print(result.shape)
        cv2.imshow("test", result)
        cv2.waitKey(1)

def main():
    rospy.init_node("thomas_vision_node", anonymous=True)
    thomas = ThomasVision()
    while(True):
        thomas.detection_loop()
    rospy.spin()

if __name__ == "__main__":
    main()
