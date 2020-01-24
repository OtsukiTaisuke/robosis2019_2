# robosis2019 課題2

## 実装したこと  
usbcamで撮った画像をmessageとして投げ続け、
subsuliberがそのmessageを受け取って画像を表示。
表示された画像をマウスで左クリックすることでクリックした画像のHSV値を抽出、蓄積する。
リアルタイムで蓄積したHSV値でマスク画像を作成（更新）する。
最後にマスク画像をmessageとしてpublishする。

##実行方法
rosにusb_camをインストール　　
```bash  
sudo apt-get install ros-melodic-usb-cam
```
実行
```bash  
cd ~/catkin_ws/src  
git clone　https://github.com/OtsukiTaisuke/robosis2019_2.git　　
cd ~/catkin_ws
catkin_make
roslaunch usb_cam usb_cam-test.launch 
rosrun  robosis2019_2 opencvmouse.py 
rqt_image_view
```

## demo video
https://youtu.be/QaOt0Skv2pM
