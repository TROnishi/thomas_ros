# coding:utf-8
import rospy
from sensor_msgs import Image
from cv_bridge import CvBridge, CvBridgeError

import chainer
from chainercv.datasets import voc_bbox_label_names
from chainercv.links import SSD300
from chainercv.links import SSD512
from chainercv import utils
from chainercv.visualizations import vis_bbox

import voc_bbox_label_names
from lib import visbbox

class ThomasVision:
    def __init__(self):
        self.bridge = CvBridge()
        self.imagesub = rospy.Subscriber("/image", Image, self.imageCB)
        self.model = SSD300(
            n_fg_class=len(voc_bbox_label_names),
            pretrained_model=args.pretrained_model)
        chainer.cuda.get_device_from_id(0).use()
        model.to_gpu()
    
    def imageCB(self, data):
        try:
            img = self.bridge.imgmsg_to_cv2(data, 'bgr8')
        except CvBridgeError as e:
            rospy.logerr(e)

        
        self.detection(img)


    def detection(self, img):
        img = imgnp.asarray(img, dtype=dtype)
        img.transpose((2,0,1))
        bboxes, labels, scores = model.predict([img])
        bbox, label, score = bboxes[0], labels[0], scores[0]

        result = vis_bbox(img, bbox, label, score, label_names=voc_bbox_label_names)

        cv2.imshow("test", result)
        cv2.waitKey(1)

def main():
    rospy.init_node("thomas_vision_node", anonymous=True)
    thomas = ThomasVision()

if __name__ == "__main__":
    main()