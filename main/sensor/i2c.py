from smbus import *
import time
ARDUINO_ADDR = 0x42
I2C_BUS_NO = 8

i2c_bus = SMBus(I2C_BUS_NO)

#while 1:
   # try:
    #    message = input("Message to be send: ")
   # except:
  #      break
 #   for a in [ord(c) for c in message]:
#        i2c_bus.write_byte(ARDUINO_ADDR, a)
while 1:
    #bus.pec = 1  # Enable PEC
    time.sleep(0.5)
    # i2c_bus.write_byte(ARDUINO_ADDR, a)
    i2c_bus.write_i2c_block_data(ARDUINO_ADDR,0x01, 1)
    # b = i2c_bus.read_byte_data(ARDUINO_ADDR, 1)
    # print(b)
