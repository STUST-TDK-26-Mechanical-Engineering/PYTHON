from smbus import *
import time
# ARDUINO_ADDR = 0x42
# I2C_BUS_NO = 8



#while 1:
   # try:
    #    message = input("Message to be send: ")
   # except:
  #      break
 #   for a in [ord(c) for c in message]:
#        i2c_bus.write_byte(ARDUINO_ADDR, a)
class master:
    def __init__(self) -> None:
        self.ARDUINO_ADDR = 0x50
        self.I2C_BUS_NO = 1
        self.i2c_bus = SMBus(self.I2C_BUS_NO)
    def ress(self,mode=0x03,data=0):
       
        self.i2c_bus.write_i2c_block_data(self.ARDUINO_ADDR,mode,[data])
            # print("1")
            # b = self.i2c_bus.read_byte_data(self.ARDUINO_ADDR,0x02)
            # print(b)
        print("res")
                
    def init(self,mode=0xff,y_data=0,z_data=0):
        Y2=y_data//256
        Y1=y_data%256
        if(Y2<0):
            Y2=Y2+256
        Z2=z_data//256
        Z1=z_data%256
        if(Z2<0):
            Z2=Z2+256    
        self.i2c_bus.write_i2c_block_data(self.ARDUINO_ADDR,mode,[Y2,Y1,Z2,Z1]) 
    def send_test(self,mode=0xff,data=0):

        try:
            #bus.pec = 1  # Enable PEC
            time.sleep(0.1)
            # i2c_bus.write_byte(ARDUINO_ADDR, a)
            # self.i2c_bus.write_i2c_block_data(self.ARDUINO_ADDR,mode,[data])
            # print("1")
            # b = self.i2c_bus.read_byte_data(self.ARDUINO_ADDR,0x01,4)
            data1=self.i2c_bus.read_i2c_block_data(self.ARDUINO_ADDR,0x01, 4)
            y1=data1[0]
            y2=data1[1]
            z1=data1[2]
            z2=data1[3]
            # print(y1,y2,z1,z2)
            y_ouput=(y1*16**2)+y2#y校正參數
            if y1>128:
                y1=255-y1
                y2=256-y2
                y_ouput=-((y1*16**2)+y2)
            ## 16進位轉10進位    
            z_ouput=(z1*16**2)+z2#z旋轉校正參數
            if z1>128:
                z1=255-z1
                z2=256-z2
                z_ouput=-((z1*16**2)+z2)   
            print("y:",y_ouput,"\tz:",z_ouput)
            return y_ouput,z_ouput
        except OSError:
            print("OSError")    
# while 1:
#     a=master()
#     a.send_test(0x01)