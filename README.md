# thomas_ros

## せつめい
とーますを動かすぱっけーじだよ。  
メインのノードにサービスで情報が送られてくるよ。  
情報を受けたら次の行動を決めて各ノードにサービスで指令を出すよ。

## バージョン
* 0.0.1 
雛形つくったよ

## 各プログラム
* main.py  
情報を受け取り処理し、次の行動を決めるノード  
* move.py  
モータを制御するノード  
main.pyからリクエストを受け、前進、後退、旋回の行動を取る。  
* steam.py  
蒸気を制御するノード  
main.pyからリクエストを受け、蒸気を発する。  
* vision.py  
物体認識ノード  
カメラから得た画像から物体を検出し、大まかな距離をmain.pyに伝える。
