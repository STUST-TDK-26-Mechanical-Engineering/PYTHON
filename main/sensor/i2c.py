from smbus import *
import time
ARDUINO_ADDR = 0x42
I2C_BUS_NO = 8



#while 1:
   # try:
    #    message = input("Message to be send: ")
   # except:
  #      break
 #   for a in [ord(c) for c in message]:
#        i2c_bus.write_byte(ARDUINO_ADDR, a)
class master:
    def __init__(self) -> None:
        self.ARDUINO_ADDR = 0x42
        self.I2C_BUS_NO = 8
        self.i2c_bus = SMBus(I2C_BUS_NO)
    def send_test(self,mode,data=0):

        try:
            #bus.pec = 1  # Enable PEC
            time.sleep(0.5)
            # i2c_bus.write_byte(ARDUINO_ADDR, a)
            self.i2c_bus.write_i2c_block_data(self.ARDUINO_ADDR,mode,[data])
            # print("1")
            b = self.i2c_bus.read_byte_data(self.ARDUINO_ADDR,0x01)
            print(b)
        except OSError:
            print("OSError")    

