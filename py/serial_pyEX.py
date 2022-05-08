import serial
import multiprocessing as mp
def bytes2Hex(argv):        #十六进制显示 方法1
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

def read_com():
    portx = "COM3"
    bps = 115200
    try:
        ser = serial.Serial(portx, bps)
        print("串口详情参数：", ser)
        f = open('test.txt','w') 
        begin = b'\x7B\x00\x00\x00\x10\x00\x00\x00\x00\x6B\x7D' #发送内容
        ser.write(begin)                #串口写数据
        while ser.isOpen():
            num = ser.inWaiting()   #查询串口接收字节数据，非阻塞
            if num:
                line = ser.read(num)
                content = bytes2Hex(line)
                f.write(content)
                print(content)
    except:
        pass
    finally:
        end = b'\x7B\x00\x00\x00\x10\x00\x00\x00\x00\x6B\x7D'
        ser.write(end)
        ser.close()
        f.close()

if __name__ == "__main__":
    read_com()