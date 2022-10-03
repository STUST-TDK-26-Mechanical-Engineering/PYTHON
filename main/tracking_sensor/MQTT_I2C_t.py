from paho.mqtt import client as mqtt_client
from i2c_01 import master
import random
import time
import threading
import json
broker = 'r201_nx.local'
port = 1883
topic = "/bot/sensor/tracking"
client_id = f'sensor-{random.randint(0, 1000)}'
i2c=master()
def connect_mqtt():#連接伺服器
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
def text(client: mqtt_client):
    while 1:

        y_data,z_data=i2c.send_test(mode=0x05)
        client.publish(topic="/bot/chassis", payload=json.dumps({"msg": "log.play","X": 0,"Y": y_data,"Z": z_data,"S": 0.08}), qos=0)
def subscribe(client: mqtt_client):#訂閱
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        m_in=json.loads(msg.payload.decode()) #decode json data
        print(m_in["msg"])
        
        # if m_in["msg"]=="i2c.test":
        #     mode=m_in["mode"] 
        #     if mode == "0x01":
        #         i2c.send_test(0x01)
        #     elif mode=="0x02":
        #         i2c.send_test(0x02)  
        #     elif mode=="0x03":
        #         i2c.send_test(0x03,m_in["data"]) 
        #     elif mode=="0x04":
        #         i2c.send_test(0x04,m_in["data"])
        #     elif mode=="0x05":
        #         i2c.send_test(0x05)          
            
    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    text(client)
    
    client.loop_forever()
if __name__ == '__main__':
    i2c.ress()
    run()  


