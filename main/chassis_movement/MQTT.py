from paho.mqtt import client as mqtt_client
from chassis_movement import control 
import random
import time
import threading,os
import json
broker = 'r201_nx.local'
port = 1883
topic = "/bot/chassis"
client_id = f'chassis-{random.randint(0, 1000)}'

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
        m_in=json.loads(msg.payload.decode()) #decode json data
        print(m_in)
        if(m_in['msg']=="control.play"):
            bot.play(m_in['X'],m_in['Y'],m_in['Z'],m_in['s'])
            print(m_in['X'],m_in['Y'],m_in['Z'],m_in['s'])
        elif(m_in['msg']=="log.play"):
            bot.play(m_in['X'],m_in['Y'],m_in['Z'],m_in['S'])    
    client.subscribe(topic)
    client.on_message = on_message

def run():
   
    try:
        client = connect_mqtt()
        subscribe(client)
        client.loop_forever()
    except:
        os._exit(0)    


if __name__ == '__main__':
    bot=control("/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0",115200)
    loop= threading.Thread(target = bot.res)
    loop.start()
    run()