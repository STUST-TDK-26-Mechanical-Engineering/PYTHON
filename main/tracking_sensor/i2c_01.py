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
    def ress(self,mode=0x21,data=0):
       
        self.i2c_bus.write_i2c_block_data(self.ARDUINO_ADDR,mode,[data])
            # print("1")
            # b = self.i2c_bus.read_byte_data(self.ARDUINO_ADDR,0x02)
            # print(b)
        print("res")
                
         
    def send_test(self,mode=0xff,data=0):

        try:
            #bus.pec = 1  # Enable PEC
            time.sleep(0.1)
            # i2c_bus.write_byte(ARDUINO_ADDR, a)
            self.i2c_bus.write_i2c_block_data(self.ARDUINO_ADDR,mode,[data])
            # print("1")
            # b = self.i2c_bus.read_byte_data(self.ARDUINO_ADDR,0x01,4)
            b=self.i2c_bus.read_i2c_block_data(self.ARDUINO_ADDR,0x01, 4)
            ext1=b[1]
            ext2=b[2]
            ouput=(ext1*16**2)+ext2
            if b[1]>128:
                ext1=255-ext1
                ext2=256-ext2
                ouput=-((ext1*16**2)+ext2)
                
            print(ouput)
            return ouput
        except OSError:
            print("OSError")    
# while 1:
#     a=master()
#     a.send_test(0x01)