import subprocess,time,sys
import Jetson.GPIO as GPIO
import json
from paho.mqtt import client as mqtt_client
import random
TIME = 1                        #程序状态检测间隔（单位：分钟）
# CMD = "/home/r201/Documents/PYTHON/main/Order_record/log.py"#需要执行程序的绝对路径，支持jar 如：D:\\calc.exe 或者D:\\test.jar
chassis_movement ="/home/r201/Documents/PYTHON/main/chassis_movement/MQTT.py"
log="/home/r201/Documents/PYTHON/main/Order_record/log.py"
tracking_sensor="/home/r201/Documents/PYTHON/main/tracking_sensor/MQTT_I2C_t.py"
sensor="/home/r201/Documents/PYTHON/main/sensor/MQTT_I2C.py"
gpio="/home/r201/Documents/PYTHON/main/gpio/gpio_test.py"
class Auto_Run():
    def __init__(self,sleep_time,chassis_movement,log,tracking_sensor,sensor,gpio):
        self.res_b=7
        self.a1=29
        self.a2=31
        self.led1=15
        self.led2=33
        self.channel=32
        self.mood=False
        self.sleep_time = sleep_time
        self.chassis_movement = chassis_movement
        self.log=log
        self.tracking_sensor=tracking_sensor
        self.sensor=sensor
        self.gpio=gpio

        self.chassis_ext = (chassis_movement[-3:]).lower()        #判断文件的后缀名，全部换成小写
        self.log_ext = (log[-3:]).lower()
        self.tracking_sensor_ext = (tracking_sensor[-3:]).lower()
        self.sensor_ext = (sensor[-3:]).lower()
        self.gpio_ext=(gpio[-3:]).lower()

        self.chassis_movement_p = None                        #self.p为subprocess.Popen()的返回值，初始化为None
        self.log_p = None
        self.tracking_sensor_p = None
        self.sensor_p = None
        self.gpio_p=None
        # self.p = None
        self.chassis_movement_run() 
        self.log_run()
        self.tracking_sensor_run()
        self.sensor_run()
        # self.gpio_run()
        # self.run()                          #启动时先执行一次程序

        try:
            self.gpio_init()
            GPIO.output(self.led1, GPIO.HIGH)
            GPIO.output(self.led2, GPIO.LOW)
            while 1:
                
                print("gpio:",GPIO.input(self.res_b),GPIO.input(self.channel))
                if GPIO.input(self.res_b) and self.mood:
                    print("重起中")
                    GPIO.cleanup()
                    self.gpio_init()
                    GPIO.output(self.led1, GPIO.LOW)
                    GPIO.output(self.led2, GPIO.LOW)
                    self.chassis_movement_p.kill()
                    self.log_p.kill()
                    self.tracking_sensor_p.kill()
                    self.sensor_p.kill()
                    self.mood=False
                    time.sleep(3)
                    # self.gpio_p.kill()
                    # GPIO.cleanup()
                    # GPIO.setmode(GPIO.BOARD)
                    # GPIO.setup(res_b, GPIO.IN)
                if  GPIO.input(self.channel) and not self.mood:
                    modeAB=GPIO.input(self.a2)
                    if modeAB:
                        self.connect_mqtt("A")
                        print("執行A場地")
                    else:
                        self.connect_mqtt("B")  
                        print("執行B場地")  
                    GPIO.cleanup()
                    self.gpio_init()
                    GPIO.output(self.led2, GPIO.HIGH)
                    GPIO.output(self.led1, GPIO.LOW)
                    # self.connect_mqtt()
                    self.mood=True
                    time.sleep(3)
                time.sleep(sleep_time )  #休息10分钟，判断程序状态
                # self.poll = self.p.poll()    #判断程序进程是否存在，None：表示程序正在运行 其他值：表示程序已退出
                good=False
                if self.chassis_movement_p.poll() is None:
                    print ("chassis_movement正常")
                    good=True
                else:
                    print ("chassis_movement 未正常運作 重起中...")
                    good=False
                    self.chassis_movement_run()
                    

                if self.log_p.poll() is None:
                    print ("log正常")
                    good=True
                else:
                    print ("log 未正常運作 重起中...")
                    good=False
                    self.log_run()
                    

                if self.tracking_sensor_p.poll() is None:
                    print ("正常")
                    good=True
                else:
                    print ("tracking_sensor 未正常運作 重起中...")
                    good=False
                    self.tracking_sensor_run()

                if self.sensor_p.poll() is None:
                    print ("sensor 正常")
                    good=True
                else:
                    print ("sensor 未正常運作 重起中...")
                    good=False
                    self.sensor_run()
                if good:
                    GPIO.output(self.led1, GPIO.HIGH)
                else:
                    GPIO.output(self.led1, GPIO.LOW)    
                # if self.gpio_p.poll() is None:
                #     print ("gpio 正常")
                # else:
                #     print ("gpio 未正常運作 重起中...")
                #     GPIO.cleanup()
                #     self.gpio_run()
                    
                #     GPIO.setmode(GPIO.BOARD)
                #     GPIO.setup(res_b, GPIO.IN)                     
        except KeyboardInterrupt as e:
            print ("检测到CTRL+C,准备退出程序!")
            self.chassis_movement_p.kill()
            self.log_p.kill()
            self.tracking_sensor_p.kill()
            self.sensor_p.kill()
            self.gpio_p.kill()
            #self.p.kill()                   #检测到CTRL+C时，kill掉CMD中启动的exe或者jar程序
    def connect_mqtt(self,MODE):#連接伺服器
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
        broker = 'r201_nx.local'
        port = 1883
        client_id = f'gpio-{random.randint(0, 1000)}'
        client = mqtt_client.Client(client_id)
        client.on_connect = on_connect
        client.connect(broker, port)
        client.loop_start()
        client.publish(topic="/bot/log", payload=json.dumps({"msg": "log.play","mode":MODE}), qos=0)
    def gpio_init(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.res_b, GPIO.IN)
        
        # res_b=36
        
        GPIO.setup(self.a1, GPIO.IN)
        # GPIO.setup(res_b, GPIO.IN)
        GPIO.setup(self.led1, GPIO.OUT)
        GPIO.setup(self.led2, GPIO.OUT)
        time.sleep(1)
        GPIO.setup(self.channel, GPIO.IN)
        GPIO.setup(self.a2, GPIO.IN)
    def chassis_movement_run(self):
        if self.chassis_ext == ".py":
            print ('chassis_movement_start OK!')
            self.chassis_movement_p = subprocess.Popen(['sudo','python3','%s' % self.chassis_movement], stdin = sys.stdin,stdout = sys.stdout, stderr = sys.stderr, shell = False)
        else:
            pass
    def log_run(self):
        if self.log_ext == ".py":
            print ('log_start OK!')
            self.log_p = subprocess.Popen(['python3','%s' % self.log], stdin = sys.stdin,stdout = sys.stdout, stderr = sys.stderr, shell = False)
        else:
            pass
    def tracking_sensor_run(self):
        if self.tracking_sensor_ext == ".py":
            print ('tracking_sensor_start OK!')
            self.tracking_sensor_p = subprocess.Popen(['python3','%s' % self.tracking_sensor], stdin = sys.stdin,stdout = sys.stdout, stderr = sys.stderr, shell = False)
        else:
            pass
    def sensor_run(self):
        if self.sensor_ext == ".py":
            print ('sensor_run_start OK!')
            self.sensor_p = subprocess.Popen(['python3','%s' % self.sensor], stdin = sys.stdin,stdout = sys.stdout, stderr = sys.stderr, shell = False)
        else:
            pass
    def gpio_run(self):
        if self.gpio_ext == ".py":
            print ('gpio_run_start OK!')
            self.gpio_p = subprocess.Popen(['python3','%s' % self.gpio], stdin = sys.stdin,stdout = sys.stdout, stderr = sys.stderr, shell = False)
        else:
            pass   
    # def run(self):
    #     if self.ext == ".py":
    #         print ('start OK!')
    #         self.p = subprocess.Popen(['sudo','python3','%s' % self.cmd], stdin = sys.stdin,stdout = sys.stdout, stderr = sys.stderr, shell = False)
    #     else:
    #         pass                
app = Auto_Run(sleep_time=TIME,chassis_movement=chassis_movement,
                log=log,tracking_sensor=tracking_sensor,
                sensor=sensor,gpio=gpio)
