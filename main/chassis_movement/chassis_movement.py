from re import S, X
# import struct
import time,os
import serial
import threading
class control():
    def __init__(self,portx,bps) -> None:
        try:
            self.portx = portx
            self.bps = bps
            self.packet = bytearray()
            self.z_data=0
            self.ser = serial.Serial(self.portx, self.bps)
        except:
            os._exit(0)    
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
        try:
            self.ser.write(self.packet)     
        except:
            os._exit(0)    
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
        # a=0
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
           
# bot=control("/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0",115200)
# bot=control("/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0",115200)

  
# loop= threading.Thread(target = bot.res)
# loop.start()
# bot.play(X=0,Z=0,s=3)
# while 1:
#     bot.play(X=500,Z=0,s=3)
#     bot.play(X=-500,Z=0,s=3)