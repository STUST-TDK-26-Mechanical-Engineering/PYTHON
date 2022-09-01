from re import S, X
# import struct
import time
import serial
import threading

import cv2
import numpy as np
import sys

#------------------------------------------------------------------
cap = cv2.VideoCapture(0)                # Capturing video through webcam
# 設定擷取影像的尺寸大小
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

color = ["R", "G", "B"]

# Set range for red color and define mask
red_lower = np.array([136, 87, 111], np.uint8)
red_upper = np.array([180, 255, 255], np.uint8)

# Set range for green color and define mask
green_lower = np.array([25, 52, 72], np.uint8)
green_upper = np.array([102, 255, 255], np.uint8)

# Set range for blue color and define mask
blue_lower = np.array([94, 80, 2], np.uint8)
blue_upper = np.array([120, 255, 255], np.uint8)

kernal = np.ones((5, 5), "uint8")

#------------------------------------------------------------------
class control():
    def __init__(self,portx,bps) -> None:
        self.portx = portx
        self.bps = bps
        self.packet = bytearray()
        self.z_data=0
        self.ser = serial.Serial(self.portx, self.bps)
    def coding(self,X=0,Y=0,Z=0):
        packet = bytearray() #創一個空的陣列 類型是bytearray
        # X=0
        # Y=0
        # Z=0
        X2=X//256
        X1=X%256

        Y2=Y//256
        Y1=Y%256

        Z2=Z//256
        Z1=Z%256

        if(X2<0):
            X2=X2+256

        if(Y2<0):
            Y2=Y2+256

        if(Z2<0):
            Z2=Z2+256  

        # print(X2,X1,Y2,Y1,Z2,Z1)  
        XOR_END=0x7B^0xAA^0xAA^X2^X1^Y2^Y1^Z2^Z1 #計算較驗碼
        # XOR_END=0x7B^0xFF^0xFF
        packet.append(0x7B)  
        packet.append(0xAA)  
        packet.append(0xAA)  
        packet.append(X2)  
        packet.append(X1)  
        packet.append(Y2)  
        packet.append(Y1)
        packet.append(Z2)
        packet.append(Z1)  
        packet.append(XOR_END)  
        packet.append(0x7D)  
        # print(packet)
        self.packet=packet
        return packet
    def play(self,X=0,Y=0,Z=0,s=1):    
        self.packet=self.coding(X,Y,Z)
        time.sleep(s)
        self.packet=self.coding(0,0,0)
    def online(self):
        self.ser.write(self.packet)     
    def bytes2Hex(self,argv):        #十六进制显示 方法1
        try:
            result = ''  
            hLen = len(argv)  
            for i in range(hLen):  
                hvol = argv[i]
                if hvol == 0xfe:    #遇到0xfe换行
                    result += '\r\n'
                hhex = '0x%02x,'%hvol #转为0xff,
                result += hhex
        except:
            pass
        return result
    
    def res(self):
        a=0
        # f = open('test.txt','w') 
        while self.ser.isOpen():
            num = self.ser.inWaiting()   #查询串口接收字节数据，非阻塞
            if num:
                line = self.ser.read(num)  
                self.online() 
                    
    def res2(self):
        while 1:
            datahex = self.ser2.read(33)
            self.DueData(datahex)
            Angle=self.Angle[2]
            z= self.Angle[2]
            if(z<0):
                z= 360-abs(self.Angle[2])
            self.pid.update(z)

            print(round(self.pid.output),"////",z,"///",self.Angle[2])
            self.online()                          
    def go(self):
        self.ser = serial.Serial(self.portx, self.bps)
        t = threading.Thread(target = self.res)
        t.start()
    def stop_serial(self):
        self.ser.close()             # close port


#------------------------------------------------------------------
def get_edge(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    # 灰階處理
    blur = cv2.GaussianBlur(gray, (5, 5), 0)        # 高斯模糊
    # canny = cv2.Canny(blur, 18, 51, 5)                # 邊緣偵測 
    # cv2.Canny(blur_gray, low_threshold, high_threshold)    
    canny = cv2.Canny(blur, threshold, threshold * ratio, apertureSize=3)   #low_threshold, high_threshold 
    
    return canny

#------------------------------------------------------------------
def draw_lines(img, lines):                 # 建立自訂函式
    for line in lines:
        points = line.reshape(4,)       # 降成一維 shape = (4,)
        x1, y1, x2, y2 = points         # 取出直線座標
        cv2.line(img,                   # 繪製直線
                 (x1, y1), (x2, y2),
                 (0, 0, 255), 3)
    return img

#------------------------------------------------------------------
def Color_recognition(img):
    # Convert the imageFrame in BGR to HSV (hue-saturation-value) color space
    hsvFrame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper) # define mask for red color
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper) # define mask for green color
    blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper) # define mask for blue color
    
    # Dilation, bitwise_and between img and mask to detect only the particular color  
    # For red color
    red_mask = cv2.dilate(red_mask, kernal)
    res_red = cv2.bitwise_and(img, img, mask = red_mask)
    # For green color
    green_mask = cv2.dilate(green_mask, kernal)
    res_green = cv2.bitwise_and(img, img, mask = green_mask)
    # For blue color
    blue_mask = cv2.dilate(blue_mask, kernal)
    res_blue = cv2.bitwise_and(img, img, mask = blue_mask)
    
    xmin = [1000, 1000, 1000]
    ymin = [1000, 1000, 1000]

    # Creating contour to track red color
    contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 500):
            x, y, w, h = cv2.boundingRect(contour) 
            if (x < xmin[0] and y < ymin[0]):
                xmin[0] = x
                ymin[0] = y
            imageFrame = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(img, "Red Color", (x, y),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))

    # Creating contour to track green color
    contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)	
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 500):
            x, y, w, h = cv2.boundingRect(contour)
            if (x < xmin[1] and y < ymin[1]):
                xmin[1] = x
                ymin[1] = y
            imageFrame = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, "Green Color", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0))

    # Creating contour to track blue color
    contours, hierarchy = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 500):
            x, y, w, h = cv2.boundingRect(contour)
            if (x < xmin[2] and y < ymin[2]):
                xmin[2] = x
                ymin[2] = y
            imageFrame = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(img, "Blue Colour", (x, y),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0))

    color = ["R", "G", "B"]
    #顏色排序由小(最左)到大(最右)排序，indx是排序指標 
    indx = sorted(range(len(xmin)), key=lambda k: xmin[k])
    color_pred = ["N", "N", "N"]
    for j in range(3):
        if (xmin[indx[j]] == 1000):
            color_pred[j] = "N"
        else:
            color_pred[j] = color[indx[j]]

    return color_pred

#------------------------------------------------------------------
COM_PORT = 'COM3'  # 請自行修改序列埠名稱
BAUD_RATES = 38400
# ser = serial.Serial(COM_PORT, BAUD_RATES)

bot = control(COM_PORT,BAUD_RATES)
# bot = control("/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0",115200)
 
#------------------------------------------------------------------
loop = threading.Thread(target = bot.res)
loop.start()


i = 0
while True:
    bot.play(X=100,Z=0,s=0.1)   #X = 100 cm, Z = 0, s = 0.1 sec
    bot.play(X=-100,Z=0,s=0.1)
    time.sleep(0.1)

    i += 1      
    ret, img = cap.read()                       # Reading image from the webcam
    if not ret:
        print("Cannot receive frame ......")
        break
    
    color_pred = Color_recognition(img)         # 顏色辨識
    print('\ni = {}   color prediction = {}'.format(i, color_pred))

    cv2.imshow('image', img)

    if cv2.waitKey(10) & 0xFF == ord("q"):
        bot.stop_serial()                       # 結束串列傳輸
        break

print('\n結束 ......')
cv2.destroyAllWindows()

