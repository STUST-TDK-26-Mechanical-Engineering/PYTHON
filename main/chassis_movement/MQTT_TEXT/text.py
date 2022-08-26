from paho.mqtt import client as mqtt_client
import random
import time
import json

broker = 'r201_nx.local'
port = 1883
topic = "/bot/log"
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
        m_in=json.loads(msg.payload.decode()) #decode json data
        print(m_in)
        if(m_in['msg']=="control.play"):
            # bot.play(m_in['X'],m_in['Y'],m_in['Z'],m_in['s'])
            print(m_in['X'],m_in['Y'],m_in['Z'],m_in['s'])
    client.subscribe(topic)
    client.on_message = on_message  
def publish(client):#發送訊息
    
    brokers_out={"msg": "control.log.play",
                "X":500,
                "Y":0,
                "Z":0,
                "s":2
                }
    brokers_out2={"msg": "control.log.play",
                "X":-500,
                "Y":0,
                "Z":0,
                "s":2
                }
    for x in range(1,10):
        if x%2:
            data_out=json.dumps(brokers_out2) # encode object to JSON
        else:
            data_out=json.dumps(brokers_out) # encode object to JSON    
        msg = data_out
        result = client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
            
    
def run():


    client = connect_mqtt()
    publish(client)
   


if __name__ == '__main__':
    run()