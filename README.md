# robosis2019 課題2

## 実装したこと  
usbcamで撮った画像をmessageとして投げ続け、  
subsuliberがそのmessageを受け取って画像を表示  
表示された画像をマウスで左クリックすることでクリックした画像のHSV値を抽出、蓄積  
リアルタイムで蓄積したHSV値でマスク画像を作成（更新）  
最後にマスク画像をmessageとしてpublish  

## 実行方法
rosにusb_camをインストール　　
```bash  
sudo apt-get install ros-melodic-usb-cam
```
コンパイル
```bash  
cd ~/catkin_ws/src  
git clone　https://github.com/OtsukiTaisuke/robosis2019_2.git　　
cd ~/catkin_ws
catkin_make
```
usb_camの実行
```bash  
roslaunch usb_cam usb_cam-test.launch  
```
or  
```bash  
roscore
rosrun usb_cam usb_cam_node
```
プログラムの実行
```bash  
rosrun  robosis2019_2 opencvmouse.py 
```
publishされた画像の可視化
```bash  
rqt_image_view
```
## demo video
https://youtu.be/QaOt0Skv2pM
