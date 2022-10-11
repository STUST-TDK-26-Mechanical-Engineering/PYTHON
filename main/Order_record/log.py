from paho.mqtt import client as mqtt_client
import random
import json
import time
from File_operations import log
import os
broker = 'r201_nx.local'
port = 1883
topic = "/bot/log"
client_id = f'log-{random.randint(0, 1000)}'
File_log=log()
mode_A="/home/r201/Documents/PYTHON/output_A.json"
mode_A_RE="/home/r201/Documents"
mode_B="/home/r201/Documents/PYTHON/output_B.json"
mode_B_RE="/home/r201/Documents/PYTHON/output_B-RES.json" 
        
# 当代理响应订阅请求时被调用。
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("连接成功")
    print("Connected with result code " + str(rc))


# 当代理响应订阅请求时被调用
def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


# 当使用使用publish()发送的消息已经传输到代理时被调用。
def on_publish(client, obj, mid):
    print("OnPublish, mid: " + str(mid))


# 当收到关于客户订阅的主题的消息时调用。 message是一个描述所有消息参数的MQTTMessage。
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    m_in=json.loads(msg.payload.decode()) #decode json data
    print(m_in)
    if(m_in['msg']=="control.log.play"):#啟動記錄模式
        print(m_in['X'],m_in['Y'],m_in['Z'],m_in['s'])
        msg={
         "msg": "log.play",
         "X": m_in['X'],
         "Y": m_in['Y'],
         "Z": m_in['Z'],
         "S": m_in['s']
        }
        msg=json.dumps(msg)
        client.publish(topic="/bot/chassis", payload=msg, qos=2)
        File_log.online(m_in['X'],m_in['Y'],m_in['Z'],m_in['s'])
    elif(m_in['msg']=="log.play"):#啟動紀錄回放模式
        if m_in['mode']=="A":
            FILE=mode_A
        elif m_in['mode']=="A_RE":
            FILE=mode_A_RE
        elif m_in['mode']=="B":
            FILE=mode_B    
        elif m_in['mode']=="B_RE":
            FILE=mode_B_RE    
        
        data,id_len=File_log.read_file(0,FILE) 
        for x in range(1,id_len+1):
            data,id_len=File_log.read_file(x,FILE)
            data=data
            
            data_out=json.dumps(data) # encode object to JSON
            msg = data_out
            # print(data["S"]+0.5)
            if data["msg"]=="i2c.test":

                client.publish(topic="/bot/sensor", payload=msg, qos=0)
            elif data["msg"]=="log.play" :
                client.publish(topic="/bot/chassis", payload=msg, qos=0)
            elif data["msg"]=="pitching.play":
                client.publish(topic="/bot/pitching", payload=msg, qos=0)
            elif data["msg"]=="i2c.teack":    
                client.publish(topic="/bot/sensor/tracking", payload=msg, qos=0)
            client.loop_start()
            time.sleep(data["S"])
        client.loop_forever()    
        print("a")    
        os._exit(0)
# 当客户端有日志信息时调用
def on_log(client, obj, level, string):
    print("Log:" + string)
def run():
    try:    
        client = mqtt_client.Client()
        client.on_connect = on_connect
        client.on_subscribe = on_subscribe
        client.on_message = on_message
        client.on_log = on_log
        client.connect(host=broker, port=port, keepalive=6000)  # 订阅频道\
        time.sleep(1)
        client.subscribe(topic, 0)
            #client.loop_start() 
            # client = connect_mqtt()
            # subscribe(client)
        client.loop_forever()

    except:
        os._exit(0) 
if __name__ == '__main__':
    run()