from paho.mqtt import client as mqtt_client
from chassis_movement import control 
import random
import time
import threading
broker = 'r201_nx.local'
port = 1883
topic = "/python/mqtt"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

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

def subscribe(client: mqtt_client):#訂閱
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        if (msg.payload.decode()=='1'):
            bot.play(X=500,s=3)
            print("ok")
    client.subscribe(topic)
    client.on_message = on_message

def run():
   
    
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    bot=control("COM7",115200)
    loop= threading.Thread(target = bot.res)
    loop.start()
    run()