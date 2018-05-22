#!/usr/bin/env python
#coding: utf-8
import rospy
from thomas_ros.srv import *

class ThomasSteam:
    def __init__(self):
        steamSS = rospy.Service("steam", steam, self.output_steam)
    
    def output_steam(self, req):
        """
        動作用関数
        Coreノードからリクエストが来た時に起動

        #steam.srv
        bool command #リクエスト（boolでon offを指令）
        ---
                       #レスポンス（なし）
        """
        """
        リクエストの受け方
        req.<.srvの変数名>でcommandに入ってる値を持ってくる
        """
        if req.command == 1:
            #ぽっぽー
            pass
        return True

def main():
    rospy.init_node("thomas_steam", anonymous=True)
    thomas = ThomasSteam()
    rospy.spin()

if __name__ == "__main__":
    main()