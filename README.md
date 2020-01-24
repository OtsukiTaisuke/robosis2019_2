# robosis2019 課題2

## 実装したこと  
usbcamで撮った画像をmessageとして投げ続け、
subsuliberがそのmessageを受け取って画像を表示。
表示された画像をマウスで左クリックすることでクリックした画像のHSV値を抽出、蓄積する。
リアルタイムで蓄積したHSV値でマスク画像を作成（更新）する。
最後にマスク画像をmessageとしてpublishする。

```bash
git clone https://github.com/OtsukiTaisuke/robosys2019.git
cd robosys2019
make
sudo insmod kadai.ko
sudo chmod 666 /dev/myled0
echo 1 > /dev/myled0
echo 0 > /dev/myled0
sudo rmmod kadai.ko
```

## demo video
https://youtu.be/QaOt0Skv2pM
