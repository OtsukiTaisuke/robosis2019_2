#!/usr/bin/env python
import cv2
import sys
import colorsys
import numpy as np
import sys
from os import system

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class ImagePub():
    def __init__(self):
        print("set image pub class")
        self.pub = rospy.Publisher('opencvmouse/image', Image, queue_size=10)
        self.bridge = CvBridge()

    def publish(self,img):
        msg = self.bridge.cv2_to_imgmsg(img,encoding="8UC1")
        self.pub.publish(msg)

class BallDetect():
    def __init__(self):

        print("push: red or yellow or blue")
        self.s = raw_input()
        if(self.s=="red"):
            print("OK,Please trace red")
        elif(self.s=="yellow"):
            print("OK,Please trace yellow")
        elif(self.s=="blue"):
            print("OK,Please trace blue")
        else:
            raise("name Error")

        windowName="origin"
        cv2.namedWindow(windowName)
        cv2.setMouseCallback(windowName,self.onMouse)
        windowName="mask"
        cv2.namedWindow(windowName)
        cv2.setMouseCallback(windowName,self.onMouse)
        self.isClick = False;
        self.red_upcon=[]
        self.red_downcon=[]
        self.flag=0
        self.mask = []


    def __del__(self):
        cv2.destroyAllWindows()
    def input_param(self,img):
        self.img = img

    def output(self):

        #cv2.imshow(self.windowName,self.img)
        if(self.red_upcon):
            self.color_track()
        cv2.imshow("origin",self.img)
        cv2.waitKey(1)

    def create_con(self,h,s,v):
        if(self.red_upcon):
            system("clear")
            if(self.s=="red"):
                if(self.red_upcon[0]<=90):
                    if(h<=90):
                        self.red_upcon[0]=max([self.red_upcon[0],h])
                        self.red_downcon[0]=0
                    if(h>90):
                        self.red_upcon2=179
                        if(self.flag==0):
                            self.red_downcon2=h
                            self.flag=1
                        else:
                            self.red_downcon2=min([self.red_downcon2,h])
                if(self.red_upcon[0]>90):
                    if(h>90):
                        self.red_upcon[0]=179
                        self.red_downcon[0]=min([self.red_downcon[0],h])
                    if(h<=90):
                        if(self.flag==0):
                            self.red_upcon2=h
                            self.flag=1
                        else:
                            self.red_upcon2=max([self.red_upcon2,h])
                        self.red_downcon2=0
            else:

                self.red_upcon[0]=max([self.red_upcon[0],h])
                self.red_downcon[0]=min([self.red_downcon[0],h])
            if(self.flag):
                print('HSV_UP2: %d' % (self.red_upcon2))
                print('HSV_Down2: %d' % (self.red_downcon2))
            self.red_upcon[1]=max([self.red_upcon[1],s])
            self.red_upcon[2]=max([self.red_upcon[2],v])
            self.red_downcon[1]=min([self.red_downcon[1],s])
            self.red_downcon[2]=min([self.red_downcon[2],v])

            print("*****************************************")
            print('HSV_Now: %d,%d,%d' % (h,s,v))
            print('HSV_UP: %d,%d,%d' % (self.red_upcon[0],self.red_upcon[1],self.red_upcon[2]))
            print('HSV_Down: %d,%d,%d' % (self.red_downcon[0],self.red_downcon[1],self.red_downcon[2]))
            print("*****************************************")
        else:
            self.red_upcon.append(h)
            self.red_upcon.append(s)
            self.red_upcon.append(v)
            self.red_downcon.append(h)
            self.red_downcon.append(s)
            self.red_downcon.append(v)


    def onMouse(self,event, x, y, flags, param):
        """
        if event == cv2.EVENT_FLAG_LBUTTON:
        """   
        if (event == cv2.EVENT_LBUTTONDOWN):
            self.isClick = True;
        if (event == cv2.EVENT_LBUTTONUP):
            self.isClick = False;
        if (self.isClick==True) :
            color = self.img[y,x]
            center=(x,y)
            radius=1
            #cv2.circle(self.img,center,radius,color)
            r = color[2]
            g = color[1]
            b = color[0]
            #print("rgb=%d,%d,%d" %(r,g,b))
            hsv = colorsys.rgb_to_hsv(r/255.0,g/255.0,b/255.0)
            h = int(hsv[0]*180)
            s = int(hsv[1]*255)
            v = int(hsv[2]*255)
            #print('HSV: %d,%d,%d' % (h,s,v))
            self.create_con(h,s,v)
    def color_track(self):
        im_h = cv2.cvtColor(self.img,cv2.COLOR_BGR2HSV) 
        mask = cv2.inRange(im_h,np.array(self.red_downcon),np.array(self.red_upcon))       
        self.mask = cv2.medianBlur(mask,7)             
        if(self.flag):
            mask2 = cv2.inRange(im_h,np.array([self.red_downcon2, self.red_downcon[1],self.red_downcon[2]]),np.array([self.red_upcon2,self.red_upcon[1],self.red_upcon[2]]))       
            mask2=cv2.medianBlur(mask2,7)
            self.mask +=mask2
        cv2.imshow("mask",self.mask)
        #mask = cv2.dilate(mask,k,iterations=2)   
        #im_c = cv2.bitwise_and(im,im,mask=mask)  
        #return mask#,im_c
class Ros :
    def __init__(self):
        rospy.init_node("ball_", anonymous=True)

        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/usb_cam/image_raw",Image,self.callback)


        self.img_org=[]
    def callback(self,data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

#cv2.imshow("Image window", cv_image)
        self.img_org = cv_image.copy()



def main():
    balldetector=BallDetect()
    publisher = ImagePub()
    ros=Ros()
    #cap = cv2.VideoCapture(1)
    #cap.set(cv2.CAP_PROP_FPS,60)
    #cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
    #cap.set(cv2.CAP_PROP_FRAME_HEIGHT,570)
    #if cap.isOpened() is False:
    #    raise("IO Error")
    rate = rospy.Rate(100)
    while not rospy.is_shutdown():
        #ret, img = cap.read()
        img = ros.img_org
        if(img!=[]):
            balldetector.input_param(img)
            balldetector.output()
        if(balldetector.mask !=[]):
            publisher.publish(balldetector.mask)
        rate.sleep()

if __name__ =='__main__':
    main()
