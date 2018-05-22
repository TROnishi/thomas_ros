#!/usr/bin/env python
#coding: utf-8
import rospy
from thomas_ros.srv import *

class ThomasMove:
    def __init__(self):
        moveSS = rospy.Service("move", move, self.move_thomas)
    
    def move_thomas(self, req):
        """
        動作用関数
        Coreノードからリクエストが来た時に起動

        #move.srv
        uint32 command #リクエスト（intで指令）
        ---
                       #レスポンス（なし）
        """
        """
        リクエストの受け方
        req.<.srvの変数名>でcommandに入ってる値を持ってくる
        """
        if req.command == 1:
            pass
        return True

def main():
    rospy.init_node("thomas_move", anonymous=True)
    thomas = ThomasMove()
    rospy.spin()

if __name__ == "__main__":
    main()