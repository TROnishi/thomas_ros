#!/usr/bin/env python
#coding: utf-8
import sys
import rospy
import rosparam
from std_msgs.msg import String
from sensor_msgs.msg import Image
from dynamic_reconfigure.srv import *
from recog_object_2d.srv import *
import recog_object_2d.msg as mydef_msg
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
import chainer.functions as F
from chainer import optimizers
from chainer import cuda
from chainer import Variable
from chainer import serializers
import time
import cPickle
import cv2 as cv
import math
import argparse
from glob import glob
from os import path
import os

import datetime

import common_params
import mbox_labels
import calc_sand_point
import change_params_mod
import time
import datetime
import random
import time

class SSDMod:
    def to_CPU(self, Loc, Cls)
        Loc = cuda.to_cpu(Loc.data)
        Cls = cuda.to_cpu(Cls.data)
        return Loc, Cls

    def mbox_softmax(self, confidence_maps, num_classes, num_boxes, normalization):
        s = np.zeros((confidence_maps.shape[0], confidence_maps.shape[1], confidence_maps.shape[2]), np.float32)

        bs = 0
        be = num_classes
        for b in xrange(0, num_boxes):
            t = confidence_maps[bs : be, :, :]

            mt = t > 50
            t[mt] = 50

            total = 0
            for i in xrange(0, t.shape[0]):
                total += np.exp(t[i, :, :])
            for i in xrange(0, t.shape[0]):
                if normalization == 1:
                    s[bs + i, :, :] = np.exp(t[i, :, :]) / total
                else:
                    s[bs + i, :, :] = t[i, :, :]
            
            bs = be
            be += num_classes
        
        return s

    def multi_box_detection(self, localization_maps, cls_score_maps, num_dbox, min_size, max_size, step, aspect_ratio, Lcls_raw):
        box_offsets = []
        default_boxes = []
        class_labels = []
        class_scores = []

        num_class = common_params.num_of_class
        offset_dim = common_params.num_of_offset_dims

        img_width = common_params.insize
        img_height = common_params.insize

        map_size = class_score_maps.shape[1] * class_score_maps.shape[2]
        for i in xrange(0, map_size):
            c = int(i % class_score_maps.shape[1])
            r = int(i / class_score_maps.shape[1])

            mbox_max_val = 0
            mbox_max_idx = 0
            mbox_num = 0

            bs_cls = 0
            be_cls= num_class
            for b in xrange(0, num_dbox):
                cls_max_val = np.max(lcls_score_maps[bs_cls : be_cls, r, c])
                cls_max_idx = int(np.argmax(lcls_score_maps[bs_cls : be_cls, r, c]))
                cls_val = cls_score_maps[bs_cls : be_cls, r, c]

                if cls_max_val > mbox_max_val and cls_max_idx != 0:
                    mbox_max_val = cls_max_val
                    mbox_max_idx = cls_max_idx
                    mbox_num = b
                    # cls_max_val = np.max(cls_score_maps[bs_cls : be_cls, r, c])
                    # cls_max_idx = int(np.argmax(cls_score_maps[bs_cls : be_cls, r, c]))
                    # lcls_max_val = np.max(lcls_score_maps[bs_lcls : be_lcls, r, c])
                    cls_max_val = np.max(cls_score_maps[bs_cls : be_cls, r, c])
                    cls_val = cls_score_maps[bs_cls : be_cls, r, c]
                    cls_max_idx = int(np.argmax(cls_score_maps[bs_cls : be_cls, r, c]))

                bs_cls = be_cls
                be_cls += num_class

            b_offset = localization_maps[bs_cls : be_cls, r, c]
            bs_cls = mbox_num * num_class
            be_cls = bs_cls + num_class
            cls_score_val = cls_score_maps[bs_cls : be_cls, r, c]
            # lcls_score_val = Lcls_raw[bs_lcls : be_lcls, r, c]
            # lcls_score_val = lcls_score_maps[bs_lcls : be_lcls, r, c]
            offset_ = 0.5

            if mbox_max_val >= 0.5:
                center_x = float((c + offset_) * step)
                center_y = float((r + offset_) * step)

                if mbox_num == 0:
                    box_width = box_height = min_size
                    xmin = (center_x - box_width / 2.) / img_width
                    ymin = (center_y - box_height / 2.) / img_height
                    xmax = (center_x + box_width / 2.) / img_width
                    ymax = (center_y + box_height / 2.) / img_height
                elif mbox_num == 1:
                    box_width = box_height = np.sqrt(min_size * max_size)
                    xmin = (center_x - box_width / 2.) / img_width
                    ymin = (center_y - box_height / 2.) / img_height
                    xmax = (center_x + box_width / 2.) / img_width
                    ymax = (center_y + box_height / 2.) / img_height
                elif mbox_num == 2:
                    box_width = min_size * np.sqrt(float(aspect_ratio[0]))
                    box_height = min_size / np.sqrt(float(aspect_ratio[0]))
                    xmin = (center_x - box_width / 2.) / img_width
                    ymin = (center_y - box_height / 2.) / img_height
                    xmax = (center_x + box_width / 2.) / img_width
                    ymax = (center_y + box_height / 2.) / img_height
                elif mbox_num == 3:
                    box_width = min_size * np.sqrt(1. / float(aspect_ratio[0]))
                    box_height = min_size / np.sqrt(1. / float(aspect_ratio[0]))
                    xmin = (center_x - box_width / 2.) / img_width
                    ymin = (center_y - box_height / 2.) / img_height
                    xmax = (center_x + box_width / 2.) / img_width
                    ymax = (center_y + box_height / 2.) / img_height
                elif mbox_num == 4:
                    box_width = min_size * np.sqrt(float(aspect_ratio[1]))
                    box_height = min_size / np.sqrt(float(aspect_ratio[1]))
                    xmin = (center_x - box_width / 2.) / img_width
                    ymin = (center_y - box_height / 2.) / img_height
                    xmax = (center_x + box_width / 2.) / img_width
                    ymax = (center_y + box_height / 2.) / img_height
                elif mbox_num == 5:
                    box_width = min_size * np.sqrt(1. / float(aspect_ratio[1]))
                    box_height = min_size / np.sqrt(1. / float(aspect_ratio[1]))
                    xmin = (center_x - box_width / 2.) / img_width
                    ymin = (center_y - box_height / 2.) / img_height
                    xmax = (center_x + box_width / 2.) / img_width
                    ymax = (center_y + box_height / 2.) / img_height

                box_offsets.append(b_offset)
                default_boxes.append([min(max(xmin, 0.), 1.), min(max(ymin, 0.), 1.), min(max(xmax, 0.), 1.), min(max(ymax, 0.), 1.), mbox_num])
                class_labels.append(mbox_max_idx)
                class_scores.append(mbox_max_val)
                class_all_score.append(cls_score_val)
        return (box_offsets, default_boxes, class_labels, class_scores, object_scores, class_all_score)

    def candidates_detection(self, offsets, default_boxes, class_labels, class_scores, color_img):
        img_width = color_img.shape[1]
        img_height = color_img.shape[0]

        candidates = []

        for det in xrange(0, len(lclass_labels)):

            pred_xmin = (default_boxes[det][0] + offsets[det][0] * common_params.loc_var)
            pred_ymin = (default_boxes[det][1] + offsets[det][1] * common_params.loc_var)
            pred_xmax = (default_boxes[det][2] + offsets[det][2] * common_params.loc_var)
            pred_ymax = (default_boxes[det][3] + offsets[det][3] * common_params.loc_var)

            pred_xmin = min(max(pred_xmin, 0.), 1.) * img_width
            pred_ymin = min(max(pred_ymin, 0.), 1.) * img_height
            pred_xmax = min(max(pred_xmax, 0.), 1.) * img_width
            pred_ymax = min(max(pred_ymax, 0.), 1.) * img_height
            candidates.append([pred_xmin, pred_ymin, pred_xmax, pred_ymax, class_scores[det], class_labels[det]])


        return candidates