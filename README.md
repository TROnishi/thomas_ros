# thomas_ros

## せつめい
とーますを動かすぱっけーじだよ。  
メインのノードにサービスで情報が送られてくるよ。  
情報を受けたら次の行動を決めて各ノードにサービスで指令を出すよ。

## バージョン 
* 0.0.1  
雛形つくったよ
* 0.1.0  
画像認識部分追加したよ  
params.pyを追加したよ

## 各プログラム
* main.py  
情報を受け取り処理し、次の行動を決めるノード  
* move.py  
モータを制御するノード  
main.pyからリクエストを受け、前進、後退、旋回の行動を取る。  
* steam.py  
蒸気を制御するノード  
main.pyからリクエストを受け、蒸気を発する。  
* image_publisher.py   
カメラから取得した画像をトピックに配信する。
* find_object.py  
トピックから画像を読み込んで物体検出と認識を行う。
* params.py  
変更しがちな変数をここに記入(GPUIDやトピックなど)

## 実行
* 画像認識部分  
```$ rosrun thomas_ros image_publisher.py```  
```$ rosrun thomas_ros find_object.py```

## いるもの
chainer v4.x.x  
chainercv vなんでも
