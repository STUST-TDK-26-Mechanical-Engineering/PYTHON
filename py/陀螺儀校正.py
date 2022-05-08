from JY61 import JY61
from pid import pid_rum
import serial
import time
import math
if __name__=='__main__': 
    port="COM10"
    baud=9600
    ser = serial.Serial(port, baud, timeout=0.5)  # ser = serial.Serial('com7',115200, timeout=0.5) 
    print(ser.is_open)
    Jy61=JY61()
    pid=pid_rum(P=1)
    pid.SetPoint =50
    while(1):
        datahex = ser.read(33)
        Jy61.DueData(datahex)
        z= Jy61.Angle[2]
        if(z<0):
            z= 360-abs(Jy61.Angle[2])

        # z=Jy61.Angle[2]-pid.SetPoint
        # 分叉測試#
           # map()


        pid.update(z)    
        output=round(pid.output)    
        print(output,"\t\t",Jy61.Angle[2],"/////",z)  
            
