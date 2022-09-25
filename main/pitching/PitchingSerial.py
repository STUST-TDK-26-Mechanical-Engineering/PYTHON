import serial

class main :
    def __init__(self) -> None:
        try:
            self.ser = serial.Serial("/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0", 19200)
        except:
            print("串口無法連接!")
    def origin(self):
        #01 10 00 16 00 02 04 00 01 00 00 23 49 
        packet = bytearray()
        packet.append(0x01)  
        packet.append(0x10)
        packet.append(0x00)
        packet.append(0x16)
        packet.append(0x00)
        packet.append(0x02)
        packet.append(0x04)
        packet.append(0x00)
        packet.append(0x01)
        packet.append(0x00)
        packet.append(0x00)
        packet.append(0x23)
        packet.append(0x49) 
        self.ser.write(packet)
    def run_90_degrees(self):
        #01 10 00 16 00 02 04 61 A8 00 00 EC 95
        packet = bytearray()
        packet.append(0x01)  
        packet.append(0x10)
        packet.append(0x00)
        packet.append(0x16)
        packet.append(0x00)
        packet.append(0x02)
        packet.append(0x04)
        packet.append(0x61)
        packet.append(0xA8)
        packet.append(0x00)
        packet.append(0x00)
        packet.append(0xEC)
        packet.append(0x95) 
        self.ser.write(packet)